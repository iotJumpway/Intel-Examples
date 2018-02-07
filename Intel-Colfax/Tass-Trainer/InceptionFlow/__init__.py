# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# *****************************************************************************
# InceptionFlow
# Copyright (c) 2018 Adam Milton-Barker - AdamMiltonBarker.com
# Based on Google's Tensorflow Imagenet Inception V3
# *****************************************************************************

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import glob
import hashlib
import os.path
import random
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat

import struct
FLAGS = tf.app.flags.FLAGS

# Input and output file flags.
tf.app.flags.DEFINE_string('image_dir', 'training/human',
                           """Path to folders of labeled images.""")
tf.app.flags.DEFINE_string('output_graph', 'model/TASS.pb',
                           """Where to save the trained graph.""")
tf.app.flags.DEFINE_string('output_labels', 'model/TASS.txt',
                           """Where to save the trained graph's labels.""")
tf.app.flags.DEFINE_string('summaries_dir', 'model/retrain_logs',
                          """Where to save summary logs for TensorBoard.""")

# Details of the training configuration.
tf.app.flags.DEFINE_integer('how_many_training_steps', 4000,
                            """How many training steps to run before ending.""")
tf.app.flags.DEFINE_float('learning_rate', 0.01,
                          """How large a learning rate to use when training.""")
tf.app.flags.DEFINE_integer(
    'testing_percentage', 10,
    """What percentage of images to use as a test set.""")
tf.app.flags.DEFINE_integer(
    'validation_percentage', 10,
    """What percentage of images to use as a validation set.""")
tf.app.flags.DEFINE_integer('eval_step_interval', 10,
                            """How often to evaluate the training results.""")
tf.app.flags.DEFINE_integer('train_batch_size', 100,
                            """How many images to train on at a time.""")
tf.app.flags.DEFINE_integer('test_batch_size', 500,
                            """How many images to test on at a time. This"""
                            """ test set is only used infrequently to verify"""
                            """ the overall accuracy of the model.""")
tf.app.flags.DEFINE_integer(
    'validation_batch_size', 100,
    """How many images to use in an evaluation batch. This validation set is"""
    """ used much more often than the test set, and is an early indicator of"""
    """ how accurate the model is during training.""")

# File-system cache locations.
tf.app.flags.DEFINE_string('model_dir', 'model/imagenet',
                           """Path to classify_image_graph_def.pb, """
                           """imagenet_synset_to_human_label_map.txt, and """
                           """imagenet_2012_challenge_label_map_proto.pbtxt.""")
tf.app.flags.DEFINE_string(
    'bottleneck_dir', 'model/bottleneck',
    """Path to cache bottleneck layer values as files.""")
tf.app.flags.DEFINE_string('final_tensor_name', 'final_result',
                           """The name of the output classification layer in"""
                           """ the retrained graph.""")

# Controls the distortions used during training.
tf.app.flags.DEFINE_boolean(
    'flip_left_right', False,
    """Whether to randomly flip half of the training images horizontally.""")
tf.app.flags.DEFINE_integer(
    'random_crop', 0,
    """A percentage determining how much of a margin to randomly crop off the"""
    """ training images.""")
tf.app.flags.DEFINE_integer(
    'random_scale', 0,
    """A percentage determining how much to randomly scale up the size of the"""
    """ training images by.""")
tf.app.flags.DEFINE_integer(
    'random_brightness', 0,
    """A percentage determining how much to randomly multiply the training"""
    """ image input pixels up or down by.""")



class InceptionFlow():

    def __init__(self):	

        self.DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
        self.BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
        self.BOTTLENECK_TENSOR_SIZE = 2048
        self.MODEL_INPUT_WIDTH = 299
        self.MODEL_INPUT_HEIGHT = 299
        self.MODEL_INPUT_DEPTH = 3
        self.JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
        self.RESIZED_INPUT_TENSOR_NAME = 'ResizeBilinear:0'
        self.MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M


    def create_image_lists(self, image_dir, testing_percentage, validation_percentage):
        if not gfile.Exists(image_dir):
            print("Image directory '" + image_dir + "' not found.")
            return None
        result = {}
        sub_dirs = [x[0] for x in os.walk(image_dir)]
        # The root directory comes first, so skip it.
        is_root_dir = True
        for sub_dir in sub_dirs:
            if is_root_dir:
                is_root_dir = False
                continue
            extensions = ['jpg', 'Jpg', 'jpeg', 'JPG', 'JPEG']
            file_list = []
            dir_name = os.path.basename(sub_dir)
            if dir_name == ".ipynb_checkpoints":
                continue
            if dir_name == image_dir:
                continue
            print("Looking for images in '" + dir_name + "'")
            for extension in extensions:
                file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
                file_list.extend(glob.glob(file_glob))
            if not file_list:
                print('No files found')
                continue
            if len(file_list) < 20:
                print('WARNING: Folder has less than 20 images, which may cause issues.')
            elif len(file_list) > self.MAX_NUM_IMAGES_PER_CLASS:
                print('WARNING: Folder {} has more than {} images. Some images will ' 'never be selected.'.format(dir_name, self.MAX_NUM_IMAGES_PER_CLASS))
            label_name = re.sub(r'[^a-z0-9]+', ' ', dir_name.lower())
            training_images = []
            testing_images = []
            validation_images = []
            for file_name in file_list:
                base_name = os.path.basename(file_name)
                hash_name = re.sub(r'_nohash_.*$', '', file_name)
                hash_name_hashed = hashlib.sha1(compat.as_bytes(hash_name)).hexdigest()
                percentage_hash = ((int(hash_name_hashed, 16) %
                                    (self.MAX_NUM_IMAGES_PER_CLASS + 1)) *
                                    (100.0 / self.MAX_NUM_IMAGES_PER_CLASS))
                if percentage_hash < validation_percentage:
                    validation_images.append(base_name)
                elif percentage_hash < (testing_percentage + validation_percentage):
                    testing_images.append(base_name)
                else:
                    training_images.append(base_name)
            result[label_name] = {
                'dir': dir_name,
                'training': training_images,
                'testing': testing_images,
                'validation': validation_images,
            }
        return result


    def get_image_path(self, image_lists, label_name, index, image_dir, category):
        if label_name not in image_lists:
            tf.logging.fatal('Label does not exist %s.', label_name)
        label_lists = image_lists[label_name]
        if category not in label_lists:
            tf.logging.fatal('Category does not exist %s.', category)
        category_list = label_lists[category]
        if not category_list:
            tf.logging.fatal('Label %s has no images in the category %s.',
                            label_name, category)
        mod_index = index % len(category_list)
        base_name = category_list[mod_index]
        sub_dir = label_lists['dir']
        full_path = os.path.join(image_dir, sub_dir, base_name)
        return full_path


    def get_bottleneck_path(self, image_lists, label_name, index, bottleneck_dir,
                            category):
        return self.get_image_path(image_lists, label_name, index, bottleneck_dir,category) + '.txt'


    def create_inception_graph(self):
        with tf.Session() as sess:
            model_filename = os.path.join(
                FLAGS.model_dir, 'classify_image_graph_def.pb')
            with gfile.FastGFile(model_filename, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                bottleneck_tensor, jpeg_data_tensor, resized_input_tensor = (
                    tf.import_graph_def(graph_def, name='', return_elements=[
                        self.BOTTLENECK_TENSOR_NAME, self.JPEG_DATA_TENSOR_NAME,
                        self.RESIZED_INPUT_TENSOR_NAME]))
        return sess.graph, bottleneck_tensor, jpeg_data_tensor, resized_input_tensor


    def run_bottleneck_on_image(self, sess, image_data, image_data_tensor,
                                bottleneck_tensor):
        bottleneck_values = sess.run(
            bottleneck_tensor,
            {image_data_tensor: image_data})
        bottleneck_values = np.squeeze(bottleneck_values)
        return bottleneck_values


    def maybe_download_and_extract(self):
        dest_directory = FLAGS.model_dir
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)
        filename = self.DATA_URL.split('/')[-1]
        filepath = os.path.join(dest_directory, filename)
        if not os.path.exists(filepath):

            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' %
                                (filename,
                                    float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()

            filepath, _ = urllib.request.urlretrieve(self.DATA_URL,
                                                        filepath,
                                                        _progress)
            print()
            statinfo = os.stat(filepath)
            print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)


    def ensure_dir_exists(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


    def write_list_of_floats_to_file(self, list_of_floats , file_path):

        s = struct.pack('d' * self.BOTTLENECK_TENSOR_SIZE, *list_of_floats)
        with open(file_path, 'wb') as f:
            f.write(s)


    def read_list_of_floats_from_file(self, file_path):

        with open(file_path, 'rb') as f:
            s = struct.unpack('d' * self.BOTTLENECK_TENSOR_SIZE, f.read())
            return list(s)


        bottleneck_path_2_bottleneck_values = {}


    def get_or_create_bottleneck(self, sess, image_lists, label_name, index, image_dir,
                                category, bottleneck_dir, jpeg_data_tensor,
                                bottleneck_tensor):
        label_lists = image_lists[label_name]
        sub_dir = label_lists['dir']
        sub_dir_path = os.path.join(bottleneck_dir, sub_dir)
        self.ensure_dir_exists(sub_dir_path)
        bottleneck_path = self.get_bottleneck_path(image_lists, label_name, index,
                                                bottleneck_dir, category)
        if not os.path.exists(bottleneck_path):
            print('Creating bottleneck at ' + bottleneck_path)
            image_path = self.get_image_path(image_lists, label_name, index, image_dir,
                                        category)
            if not gfile.Exists(image_path):
                tf.logging.fatal('File does not exist %s', image_path)
            image_data = gfile.FastGFile(image_path, 'rb').read()
            bottleneck_values = self.run_bottleneck_on_image(sess, image_data,
                                                        jpeg_data_tensor,
                                                        bottleneck_tensor)
            bottleneck_string = ','.join(str(x) for x in bottleneck_values)
            with open(bottleneck_path, 'w') as bottleneck_file:
                bottleneck_file.write(bottleneck_string)

        with open(bottleneck_path, 'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read()
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
        return bottleneck_values


    def cache_bottlenecks(self, sess, image_lists, image_dir, bottleneck_dir,
                        jpeg_data_tensor, bottleneck_tensor):
        how_many_bottlenecks = 0
        self.ensure_dir_exists(bottleneck_dir)
        for label_name, label_lists in image_lists.items():
            for category in ['training', 'testing', 'validation']:
                category_list = label_lists[category]
                for index, unused_base_name in enumerate(category_list):
                    self.get_or_create_bottleneck(sess, image_lists, label_name, index,
                                            image_dir, category, bottleneck_dir,
                                            jpeg_data_tensor, bottleneck_tensor)
                    how_many_bottlenecks += 1
                    if how_many_bottlenecks % 100 == 0:
                        print(str(how_many_bottlenecks) + ' bottleneck files created.')


    def get_random_cached_bottlenecks(self, sess, image_lists, how_many, category,
                                    bottleneck_dir, image_dir, jpeg_data_tensor,
                                    bottleneck_tensor):
        class_count = len(image_lists.keys())
        bottlenecks = []
        ground_truths = []
        for unused_i in range(how_many):
            label_index = random.randrange(class_count)
            label_name = list(image_lists.keys())[label_index]
            image_index = random.randrange(self.MAX_NUM_IMAGES_PER_CLASS + 1)
            bottleneck = self.get_or_create_bottleneck(sess, image_lists, label_name,image_index, image_dir, category, bottleneck_dir, jpeg_data_tensor,bottleneck_tensor)
            ground_truth = np.zeros(class_count, dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)
        return bottlenecks, ground_truths


    def get_random_distorted_bottlenecks(
        self, sess, image_lists, how_many, category, image_dir, input_jpeg_tensor,
        distorted_image, resized_input_tensor, bottleneck_tensor):
        class_count = len(image_lists.keys())
        bottlenecks = []
        ground_truths = []
        for unused_i in range(how_many):
            label_index = random.randrange(class_count)
            label_name = list(image_lists.keys())[label_index]
            image_index = random.randrange(self.MAX_NUM_IMAGES_PER_CLASS + 1)
            image_path = self.get_image_path(image_lists, label_name, image_index, image_dir,
                                        category)
            if not gfile.Exists(image_path):
                tf.logging.fatal('File does not exist %s', image_path)
            jpeg_data = gfile.FastGFile(image_path, 'rb').read()
            # Note that we materialize the distorted_image_data as a numpy array before
            # sending running inference on the image. This involves 2 memory copies and
            # might be optimized in other implementations.
            distorted_image_data = sess.run(distorted_image,
                                            {input_jpeg_tensor: jpeg_data})
            bottleneck = self.run_bottleneck_on_image(sess, distorted_image_data,
                                                resized_input_tensor,
                                                bottleneck_tensor)
            ground_truth = np.zeros(class_count, dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)
        return bottlenecks, ground_truths


    def should_distort_images(self, flip_left_right, random_crop, random_scale,
                            random_brightness):
        return (flip_left_right or (random_crop != 0) or (random_scale != 0) or (random_brightness != 0))


    def add_input_distortions(self, flip_left_right, random_crop, random_scale,
                            random_brightness):

        jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
        decoded_image = tf.image.decode_jpeg(jpeg_data, channels=self.MODEL_INPUT_DEPTH)
        decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
        decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
        margin_scale = 1.0 + (random_crop / 100.0)
        resize_scale = 1.0 + (random_scale / 100.0)
        margin_scale_value = tf.constant(margin_scale)
        resize_scale_value = tf.random_uniform(tensor_shape.scalar(),
                                                minval=1.0,
                                                maxval=resize_scale)
        scale_value = tf.mul(margin_scale_value, resize_scale_value)
        precrop_width = tf.mul(scale_value, self.MODEL_INPUT_WIDTH)
        precrop_height = tf.mul(scale_value, self.MODEL_INPUT_HEIGHT)
        precrop_shape = tf.pack([precrop_height, precrop_width])
        precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
        precropped_image = tf.image.resize_bilinear(decoded_image_4d,
                                                    precrop_shape_as_int)
        precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
        cropped_image = tf.random_crop(precropped_image_3d,
                                        [self.MODEL_INPUT_HEIGHT, self.MODEL_INPUT_WIDTH,
                                        self.MODEL_INPUT_DEPTH])
        if flip_left_right:
            flipped_image = tf.image.random_flip_left_right(cropped_image)
        else:
            flipped_image = cropped_image
        brightness_min = 1.0 - (random_brightness / 100.0)
        brightness_max = 1.0 + (random_brightness / 100.0)
        brightness_value = tf.random_uniform(tensor_shape.scalar(),
                                            minval=brightness_min,
                                            maxval=brightness_max)
        brightened_image = tf.mul(flipped_image, brightness_value)
        distort_result = tf.expand_dims(brightened_image, 0, name='DistortResult')
        return jpeg_data, distort_result


    def variable_summaries(self, var, name):
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            tf.scalar_summary('mean/' + name, mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.scalar_summary('stddev/' + name, stddev)
            tf.scalar_summary('max/' + name, tf.reduce_max(var))
            tf.scalar_summary('min/' + name, tf.reduce_min(var))
            tf.histogram_summary(name, var)


    def add_final_training_ops(self, class_count, final_tensor_name, bottleneck_tensor):
        with tf.name_scope('input'):
            bottleneck_input = tf.placeholder_with_default(
                bottleneck_tensor, shape=[None, self.BOTTLENECK_TENSOR_SIZE],
                name='BottleneckInputPlaceholder')

            ground_truth_input = tf.placeholder(tf.float32,
                                                [None, class_count],
                                                name='GroundTruthInput')

        layer_name = 'final_training_ops'
        with tf.name_scope(layer_name):
            with tf.name_scope('weights'):
                layer_weights = tf.Variable(tf.truncated_normal([self.BOTTLENECK_TENSOR_SIZE, class_count], stddev=0.001), name='final_weights')
                self.variable_summaries(layer_weights, layer_name + '/weights')
            with tf.name_scope('biases'):
                layer_biases = tf.Variable(tf.zeros([class_count]), name='final_biases')
                self.variable_summaries(layer_biases, layer_name + '/biases')
            with tf.name_scope('Wx_plus_b'):
                logits = tf.matmul(bottleneck_input, layer_weights) + layer_biases
                tf.histogram_summary(layer_name + '/pre_activations', logits)

        final_tensor = tf.nn.sigmoid(logits, name=final_tensor_name)
        tf.histogram_summary(final_tensor_name + '/activations', final_tensor)

        with tf.name_scope('cross_entropy'):
            cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            logits, ground_truth_input)
            with tf.name_scope('total'):
                cross_entropy_mean = tf.reduce_mean(cross_entropy)
            tf.scalar_summary('cross entropy', cross_entropy_mean)

        with tf.name_scope('train'):
            train_step = tf.train.GradientDescentOptimizer(FLAGS.learning_rate).minimize(
                cross_entropy_mean)

        return (train_step, cross_entropy_mean, bottleneck_input, ground_truth_input,
                final_tensor)


    def add_evaluation_step(self, result_tensor, ground_truth_tensor):
        with tf.name_scope('accuracy'):
            with tf.name_scope('correct_prediction'):
                correct_prediction = tf.equal(tf.argmax(result_tensor, 1), \
                tf.argmax(ground_truth_tensor, 1))
            with tf.name_scope('accuracy'):
                evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            tf.scalar_summary('accuracy', evaluation_step)
        return evaluation_step


    def trainModel(self):
        # Setup the directory we'll write summaries to for TensorBoard
        if tf.gfile.Exists(FLAGS.summaries_dir):
            tf.gfile.DeleteRecursively(FLAGS.summaries_dir)
        tf.gfile.MakeDirs(FLAGS.summaries_dir)

        # Set up the pre-trained graph.
        self.maybe_download_and_extract()
        graph, bottleneck_tensor, jpeg_data_tensor, resized_image_tensor = (
            self.create_inception_graph())

        # Look at the folder structure, and create lists of all the images.
        image_lists = self.create_image_lists(FLAGS.image_dir, FLAGS.testing_percentage,
                                        FLAGS.validation_percentage)
        class_count = len(image_lists.keys())
        if class_count == 0:
            print('No valid folders of images found at ' + FLAGS.image_dir)
            return -1
        if class_count == 1:
            print('Only one valid folder of images found at ' + FLAGS.image_dir +
                ' - multiple classes are needed for classification.')
            return -1

        # See if the command-line flags mean we're applying any distortions.
        do_distort_images = self.should_distort_images(
            FLAGS.flip_left_right, FLAGS.random_crop, FLAGS.random_scale,
            FLAGS.random_brightness)
        sess = tf.Session()

        if do_distort_images:
            # We will be applying distortions, so setup the operations we'll need.
            distorted_jpeg_data_tensor, distorted_image_tensor = self.add_input_distortions(
                FLAGS.flip_left_right, FLAGS.random_crop, FLAGS.random_scale,
                FLAGS.random_brightness)
        else:
            # We'll make sure we've calculated the 'bottleneck' image summaries and
            # cached them on disk.
            self.cache_bottlenecks(sess, image_lists, FLAGS.image_dir, FLAGS.bottleneck_dir,
                            jpeg_data_tensor, bottleneck_tensor)

        # Add the new layer that we'll be training.
        (train_step, cross_entropy, bottleneck_input, ground_truth_input,
        final_tensor) = self.add_final_training_ops(len(image_lists.keys()),
                                                FLAGS.final_tensor_name,
                                                bottleneck_tensor)

        # Create the operations we need to evaluate the accuracy of our new layer.
        evaluation_step = self.add_evaluation_step(final_tensor, ground_truth_input)

        # Merge all the summaries and write them out to /tmp/retrain_logs (by default)
        merged = tf.merge_all_summaries()
        train_writer = tf.train.SummaryWriter(FLAGS.summaries_dir + '/train',
                                                sess.graph)
        validation_writer = tf.train.SummaryWriter(FLAGS.summaries_dir + '/validation')

        # Set up all our weights to their initial default values.
        init = tf.initialize_all_variables()
        sess.run(init)

        # Run the training for as many cycles as requested on the command line.
        for i in range(FLAGS.how_many_training_steps):
            # Get a batch of input bottleneck values, either calculated fresh every time
            # with distortions applied, or from the cache stored on disk.
            if do_distort_images:
                train_bottlenecks, train_ground_truth = self.get_random_distorted_bottlenecks(
                sess, image_lists, FLAGS.train_batch_size, 'training',
                FLAGS.image_dir, distorted_jpeg_data_tensor,
                distorted_image_tensor, resized_image_tensor, bottleneck_tensor)
            else:
                train_bottlenecks, train_ground_truth = self.get_random_cached_bottlenecks(
                sess, image_lists, FLAGS.train_batch_size, 'training',
                FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor,
                bottleneck_tensor)
            # Feed the bottlenecks and ground truth into the graph, and run a training
            # step. Capture training summaries for TensorBoard with the `merged` op.
            train_summary, _ = sess.run([merged, train_step],
                    feed_dict={bottleneck_input: train_bottlenecks,
                                ground_truth_input: train_ground_truth})
            train_writer.add_summary(train_summary, i)

            # Every so often, print out how well the graph is training.
            is_last_step = (i + 1 == FLAGS.how_many_training_steps)
            if (i % FLAGS.eval_step_interval) == 0 or is_last_step:
                train_accuracy, cross_entropy_value = sess.run(
                [evaluation_step, cross_entropy],
                feed_dict={bottleneck_input: train_bottlenecks,
                            ground_truth_input: train_ground_truth})
            print('%s: Step %d: Train accuracy = %.1f%%' % (datetime.now(), i,
                                                            train_accuracy * 100))
            print('%s: Step %d: Cross entropy = %f' % (datetime.now(), i,
                                                        cross_entropy_value))
            validation_bottlenecks, validation_ground_truth = (
                self.get_random_cached_bottlenecks(
                    sess, image_lists, FLAGS.validation_batch_size, 'validation',
                    FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor,
                    bottleneck_tensor))
            # Run a validation step and capture training summaries for TensorBoard
            # with the `merged` op.
            validation_summary, validation_accuracy = sess.run(
                [merged, evaluation_step],
                feed_dict={bottleneck_input: validation_bottlenecks,
                            ground_truth_input: validation_ground_truth})
            validation_writer.add_summary(validation_summary, i)
            print('%s: Step %d: Validation accuracy = %.1f%%' %
                    (datetime.now(), i, validation_accuracy * 100))

        # We've completed all our training, so run a final test evaluation on
        # some new images we haven't used before.
        test_bottlenecks, test_ground_truth = self.get_random_cached_bottlenecks(
            sess, image_lists, FLAGS.test_batch_size, 'testing',
            FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor,
            bottleneck_tensor)
        test_accuracy = sess.run(
            evaluation_step,
            feed_dict={bottleneck_input: test_bottlenecks,
                        ground_truth_input: test_ground_truth})
        print('Final test accuracy = %.1f%%' % (test_accuracy * 100))

        # Write out the trained graph and labels with the weights stored as constants.
        output_graph_def = graph_util.convert_variables_to_constants(
            sess, graph.as_graph_def(), [FLAGS.final_tensor_name])
        with gfile.FastGFile(FLAGS.output_graph, 'wb') as f:
            f.write(output_graph_def.SerializeToString())
        with gfile.FastGFile(FLAGS.output_labels, 'w') as f:
            f.write('\n'.join(image_lists.keys()) + '\n')