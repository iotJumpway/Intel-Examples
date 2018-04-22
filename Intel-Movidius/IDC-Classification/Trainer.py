from __future__ import print_function

############################################################################################
# Title: IDC Classification Trainer
# Description: Trains a custom Inception V3 model for classification of invasive ductal carcinoma (IDC).
# Acknowledgements: Uses code from chesterkuo imageclassify-movidius (https://github.com/chesterkuo/imageclassify-movidius)
#                   Uses data from paultimothymooney Predict IDC in Breast Cancer Histology Images (Kaggle)
# Last Modified: 2018-04-21
############################################################################################

############################################################################################
#
#    CLASSIFIER MODE:
#
#    Classifier configuration can be found in model/confs.json
#
#    Commandline Arguments:
#
#        - DataSort: Loads and prepares training data from model/train/1 & model/train/0
#        - Train: Trains the model
#
#    Usage:
#
#        $ python3.5 Trainer.py DataSort
#        $ python3.5 Trainer.py Train
#
############################################################################################

print("")
print("")
print("!! Welcome to the IDC Classification Trainer, please wait while the program initiates !!")
print("")

import os, sys

print("-- Running on Python "+sys.version)
print("")

import time, math, random, json, glob
import tools.inception_preprocessing

from sys import argv
from datetime import datetime

import tensorflow as tf
import numpy as np

from builtins import range
from tools.inception_v3 import inception_v3, inception_v3_arg_scope
from tools.DataSort import DataSort

from tensorflow.contrib.framework.python.ops.variables import get_or_create_global_step
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.framework import graph_util

slim = tf.contrib.slim

print("-- Imported Required Modules")
print("")

config = tf.ConfigProto(intra_op_parallelism_threads=12, inter_op_parallelism_threads=2, allow_soft_placement=True,  device_count = {'CPU': 12})

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["KMP_BLOCKTIME"] = "30"
os.environ["KMP_SETTINGS"] = "1"
os.environ["KMP_AFFINITY"]= "granularity=fine,verbose,compact,1,0"

print("-- Setup Environment Settings")
print("")

class Trainer():

    def __init__(self):

        self._confs = {}
        self.labelsToName = {}

        with open('model/confs.json') as confs:

            self._confs = json.loads(confs.read())

    #Creates a Dataset class providing TFRecord files to feed in the examples into a queue in parallel.
    def getSplit(self, split_name):

        '''
            Obtains the split - training or validation - to create a Dataset class for feeding the examples into a queue later on. This function will
            set up the decoder and dataset information all into one Dataset class so that you can avoid the brute work later on.
            Your file_pattern is very important in locating the files later.

            INPUTS:
                - split_name(str): 'train' or 'validation'. Used to get the correct data split of tfrecord files

            OUTPUTS:
                - dataset (Dataset): A Dataset class object where we can read its various components for easier batch creation later.
        '''

        #Check whether the split_name is train or validation
        if split_name not in ['train', 'validation']:

            raise ValueError('The split_name %s is not recognized. Please input either train or validation as the split_name' % (split_name))

        #Create the full path for a general file_pattern to locate the tfrecord_files
        file_pattern_path = os.path.join(self._confs["ClassifierSettings"]["dataset_dir"], self._confs["ClassifierSettings"]["file_pattern"] % (split_name))

        #Count the total number of examples in all of these shard
        num_samples = 0
        file_pattern_for_counting = '200label_' + split_name
        tfrecords_to_count = [os.path.join(self._confs["ClassifierSettings"]["dataset_dir"], file) for file in os.listdir(self._confs["ClassifierSettings"]["dataset_dir"]) if file.startswith(file_pattern_for_counting)]

        #print(tfrecords_to_count)
        for tfrecord_file in tfrecords_to_count:

            for record in tf.python_io.tf_record_iterator(tfrecord_file):

                num_samples += 1

        #Create a reader, which must be a TFRecord reader in this case
        reader = tf.TFRecordReader

        #Create the keys_to_features dictionary for the decoder
        keys_to_features = {
            'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/format': tf.FixedLenFeature((), tf.string, default_value='jpg'),
            'image/class/label': tf.FixedLenFeature(
                [], tf.int64, default_value=tf.zeros([], dtype=tf.int64)),
        }

        #Create the items_to_handlers dictionary for the decoder.
        items_to_handlers = {
            'image': slim.tfexample_decoder.Image(),
            'label': slim.tfexample_decoder.Tensor('image/class/label'),
        }

        #Start to create the decoder
        decoder = slim.tfexample_decoder.TFExampleDecoder(keys_to_features, items_to_handlers)

        #Create the labels_to_name file
        labels_to_name_dict = self.labelsToName

        #Actually create the dataset
        dataset = slim.dataset.Dataset(
            data_sources = file_pattern_path,
            decoder = decoder,
            reader = reader,
            num_readers = 4,
            num_samples = num_samples,
            num_classes = self._confs["ClassifierSettings"]["num_classes"],
            labels_to_name = labels_to_name_dict,
            items_to_descriptions = self.items_to_descriptions)

        return dataset

    def loadBatch(self, dataset, is_training=True):

        '''
            Loads a batch for training.

            INPUTS:
                - dataset(Dataset): a Dataset class object that is created from the get_split function
                - batch_size(int): determines how big of a batch to train
                - height(int): the height of the image to resize to during preprocessing
                - width(int): the width of the image to resize to during preprocessing
                - is_training(bool): to determine whether to perform a training or evaluation preprocessing

            OUTPUTS:
                - images(Tensor): a Tensor of the shape (batch_size, height, width, channels) that contain one batch of images
                - labels(Tensor): the batch's labels with the shape (batch_size,) (requires one_hot_encoding).

        '''

        #First create the data_provider object
        data_provider = slim.dataset_data_provider.DatasetDataProvider(
            dataset,
            common_queue_capacity = 24 + 3 * self._confs["ClassifierSettings"]["batch_size"],
            common_queue_min = 24)

        #Obtain the raw image using the get method
        raw_image, label = data_provider.get(['image', 'label'])

        #Perform the correct preprocessing for this image depending if it is training or evaluating
        image = tools.inception_preprocessing.preprocess_image(raw_image, self._confs["ClassifierSettings"]["image_size"], self._confs["ClassifierSettings"]["image_size"], is_training)

        #As for the raw images, we just do a simple reshape to batch it up
        raw_image = tf.image.resize_image_with_crop_or_pad(raw_image, self._confs["ClassifierSettings"]["image_size"], self._confs["ClassifierSettings"]["image_size"])

        #Batch up the image by enqueing the tensors internally in a FIFO queue and dequeueing many elements with tf.train.batch.
        images, raw_images, labels = tf.train.batch(
            [image, raw_image, label],
            batch_size = self._confs["ClassifierSettings"]["batch_size"],
            num_threads = 4,
            capacity = 4 * self._confs["ClassifierSettings"]["batch_size"],
            allow_smaller_final_batch = True)

        return images, raw_images, labels

    def sort(self):

        humanStart = datetime.now()
        clockStart = time.time()

        print("-- Loading & Preparing Training Data ")
        print("-- STARTED: ", humanStart)
        print("")
        photoPaths, classes = DataSort.processFilesAndClasses()

        class_id = [int(i) for i in classes]
        class_names_to_ids = dict(zip(classes, class_id))

        num_validation = int(self._confs["ClassifierSettings"]["validation_size"] * len(photoPaths))
        print('\n Checking ')
        print((class_names_to_ids))
        print(len(class_names_to_ids))

        sys.stdout.write('\n num_validation: %d, num class number %d \n' % ( num_validation, len(classes) ))
        sys.stdout.flush()

        # Divide the training datasets into train and test:
        random.seed(self._confs["ClassifierSettings"]["random_seed"])
        random.shuffle(photoPaths)
        training_filenames = photoPaths[num_validation:]
        validation_filenames = photoPaths[:num_validation]

        #print(training_filenames)
        #print(validation_filenames)
        #print(class_names_to_ids)

        # First, convert the training and validation sets.
        DataSort.convertToTFRecord('train', training_filenames, class_names_to_ids)
        DataSort.convertToTFRecord('validation', validation_filenames, class_names_to_ids)

        # Finally, write the labels file:
        labels_to_class_names = dict(zip(class_id, classes))
        #print(labels_to_class_names)
        #labels_to_class_names = dict(zip(range(len(class_names)), class_names))
        DataSort.writeLabels(labels_to_class_names)

        humanEnd = datetime.now()
        clockEnd = time.time()

        print('\nFinished converting the %s dataset!' % (self._confs["ClassifierSettings"]["tfrecord_filename"]))

        print("")
        print("-- Loaded & Prepared Training Data ")
        print("-- ENDED: ", humanEnd)
        print("-- TIME: {0}".format(clockEnd - clockStart))
        print("")

Trainer = Trainer()
DataSort = DataSort()

def run():

    humanStart = datetime.now()
    clockStart = time.time()

    print("-- Training Starting ")
    print("-- STARTED: ", humanStart)
    print("")

    #Open the labels file
    Trainer.labels = open(Trainer._confs["ClassifierSettings"]["labels_file"], 'r')

    #Create a dictionary to refer each label to their string name
    for line in Trainer.labels:

        label, string_name = line.split(':')
        string_name = string_name[:-1] #Remove newline
        Trainer.labelsToName[int(label)] = string_name

    #Create a dictionary that will help people understand your dataset better. This is required by the Dataset class later.
    Trainer.items_to_descriptions = {
        'image': 'A 3-channel RGB coloured  image that is ex: office, people',
        'label': 'A label that ,start from zero'
    }

    #Create the log directory here. Must be done here otherwise import will activate this unneededly.
    if not os.path.exists(Trainer._confs["ClassifierSettings"]["log_dir"]):
        os.mkdir(Trainer._confs["ClassifierSettings"]["log_dir"])

    #======================= TRAINING PROCESS =========================
    #Now we start to construct the graph and build our model
    with tf.Graph().as_default() as graph:

        tf.logging.set_verbosity(tf.logging.INFO) #Set the verbosity to INFO level

        #First create the dataset and load one batch
        dataset = Trainer.getSplit('train')

        images, _, labels = Trainer.loadBatch(dataset)

        #Know the number steps to take before decaying the learning rate and batches per epoch
        num_batches_per_epoch = dataset.num_samples // Trainer._confs["ClassifierSettings"]["batch_size"]
        num_steps_per_epoch = num_batches_per_epoch #Because one step is one batch processed
        decay_steps = int(Trainer._confs["ClassifierSettings"]["num_epochs_before_decay"] * num_steps_per_epoch)

        #Create the model inference
        with slim.arg_scope(inception_v3_arg_scope()):
            logits, end_points = inception_v3(images, num_classes = dataset.num_classes, is_training = True)

        #Perform one-hot-encoding of the labels (Try one-hot-encoding within the load_batch function!)
        one_hot_labels = slim.one_hot_encoding(labels, dataset.num_classes)

        #Performs the equivalent to tf.nn.sparse_softmax_cross_entropy_with_logits but enhanced with checks
        loss = tf.losses.softmax_cross_entropy(onehot_labels = one_hot_labels, logits = logits)
        total_loss = tf.losses.get_total_loss()    #obtain the regularization losses as well

        #Create the global step for monitoring the learning_rate and training.
        global_step = get_or_create_global_step()

        #Define your exponentially decaying learning rate
        lr = tf.train.exponential_decay(
            learning_rate = Trainer._confs["ClassifierSettings"]["initial_learning_rate"],
            global_step = global_step,
            decay_steps = decay_steps,
            decay_rate = Trainer._confs["ClassifierSettings"]["learning_rate_decay_factor"],
            staircase = True)

        #Now we can define the optimizer that takes on the learning rate
        optimizer = tf.train.AdamOptimizer(learning_rate = lr)
        #optimizer = tf.train.RMSPropOptimizer(learning_rate = lr, momentum=0.9)

        #Create the train_op.
        train_op = slim.learning.create_train_op(total_loss, optimizer)

        #State the metrics that you want to predict. We get a predictions that is not one_hot_encoded.
        predictions = tf.argmax(end_points['Predictions'], 1)
        probabilities = end_points['Predictions']
        accuracy, accuracy_update = tf.contrib.metrics.streaming_accuracy(predictions, labels)
        metrics_op = tf.group(accuracy_update, probabilities)

        #Now finally create all the summaries you need to monitor and group them into one summary op.
        tf.summary.scalar('losses/Total_Loss', total_loss)
        tf.summary.scalar('accuracy', accuracy)
        tf.summary.scalar('learning_rate', lr)
        my_summary_op = tf.summary.merge_all()

        #Now we need to create a training step function that runs both the train_op, metrics_op and updates the global_step concurrently.
        def train_step(sess, train_op, global_step, epochCount):
            '''
            Simply runs a session for the three arguments provided and gives a logging on the time elapsed for each global step
            '''
            #Check the time for each sess run
            start_time = time.time()
            total_loss, global_step_count, _ = sess.run([train_op, global_step, metrics_op])
            time_elapsed = time.time() - start_time

            #Run the logging to print some results
            logging.info(' Epch %.2f Glb Stp %s: Loss: %.4f (%.2f sec/step)', epochCount, global_step_count, total_loss, time_elapsed)

            return total_loss, global_step_count

        #Define your supervisor for running a managed session. Do not run the summary_op automatically or else it will consume too much memory
        sv = tf.train.Supervisor(logdir = Trainer._confs["ClassifierSettings"]["log_dir"], summary_op = None)

        #Run the managed session
        with sv.managed_session() as sess:
            for step in range(num_steps_per_epoch * Trainer._confs["ClassifierSettings"]["num_epochs"]):
                #At the start of every epoch, show the vital information:
                if step % num_batches_per_epoch == 0:
                    logging.info('Epoch %s/%s', step/num_batches_per_epoch + 1, Trainer._confs["ClassifierSettings"]["num_epochs"])
                    learning_rate_value, accuracy_value = sess.run([lr, accuracy])
                    logging.info('Current Learning Rate: %s', learning_rate_value)
                    logging.info('Current Streaming Accuracy: %s', accuracy_value)

                    # optionally, print your logits and predictions for a sanity check that things are going fine.
                    logits_value, probabilities_value, predictions_value, labels_value = sess.run([logits, probabilities, predictions, labels])
                    print('logits: \n', logits_value[:5])
                    print('Probabilities: \n', probabilities_value[:5])
                    print('predictions: \n', predictions_value[:100])
                    print('Labels:\n:', labels_value[:100])

                #Log the summaries every 10 step.
                if step % 10 == 0:
                    loss, _ = train_step(sess, train_op, sv.global_step, step/num_batches_per_epoch + 1)
                    summaries = sess.run(my_summary_op)
                    sv.summary_computed(sess, summaries)

                #If not, simply run the training step
                else:
                    loss, _ = train_step(sess, train_op, sv.global_step, step/num_batches_per_epoch + 1)

            #We log the final training loss and accuracy
            logging.info('Final Loss: %s', loss)
            logging.info('Final Accuracy: %s', sess.run(accuracy))

            #Once all the training has been done, save the log files and checkpoint model
            logging.info('Finished training! Saving model to disk now.')

    checkpoint_file = tf.train.latest_checkpoint(Trainer._confs["ClassifierSettings"]["log_dir"])

    with tf.Graph().as_default() as graph:

        #images = tf.placeholder(shape=[None, image_size, image_size, 3], dtype=tf.float32, name = 'Placeholder_only')
        images = tf.placeholder("float", [1, Trainer._confs["ClassifierSettings"]["image_size"], Trainer._confs["ClassifierSettings"]["image_size"], 3], name="input")

        with slim.arg_scope(inception_v3_arg_scope()):

            logits, end_points = inception_v3(images, num_classes = Trainer._confs["ClassifierSettings"]["num_classes"], is_training = False)

        probabilities = tf.nn.softmax(logits)

        saver = tf.train.Saver(slim.get_variables_to_restore())

        #Setup graph def
        input_graph_def = graph.as_graph_def()
        output_node_names = "InceptionV3/Predictions/Softmax"
        output_graph_name = "model/IDC.pb"

        with tf.Session(config=config) as sess:

            saver.restore(sess, checkpoint_file)

            #Exporting the graph
            print ("Exporting graph...")
            output_graph_def = graph_util.convert_variables_to_constants(
                sess,
                input_graph_def,
                output_node_names.split(","))

            with tf.gfile.GFile(output_graph_name, "wb") as f:

                f.write(output_graph_def.SerializeToString())

        humanEnd = datetime.now()
        clockEnd = time.time()

        print("")
        print("-- Training Ending ")
        print("-- ENDED: ", humanEnd)
        print("-- TIME: {0}".format(clockEnd - clockStart))
        print("")

def main(argv):

    if argv[0] == "Train":

        run()

    elif argv[0] == "DataSort":

        Trainer.sort()

    else:

        print("**ERROR** Check Your Parameters")

if __name__ == "__main__":

	main(sys.argv[1:])