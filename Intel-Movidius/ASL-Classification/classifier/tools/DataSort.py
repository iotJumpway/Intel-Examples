############################################################################################
# Title: IDC Detection Data Sorter
# Description: Sorts data for ready to train a custom Inception V3 model for classification of invasive ductal carcinoma (IDC).
# Acknowledgements: Uses code from chesterkuo imageclassify-movidius (https://github.com/chesterkuo/imageclassify-movidius)
#                   Uses data from paultimothymooney Predict IDC in Breast Cancer Histology Images (Kaggle)
# Last Modified: 2018-04-06
############################################################################################

import os, sys, time, math, random, json, glob

import tensorflow as tf
import numpy as np

from sys import argv
from datetime import datetime

class ImageReader(object):

    """Helper class that provides TensorFlow image coding utilities."""

    def __init__(self):
        # Initializes function that decodes RGB JPEG data.
        self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
        self._decode_jpeg = tf.image.decode_image(self._decode_jpeg_data, channels=3)
        #self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

    def read_image_dims(self, sess, image_data):
        image = self.decode_jpeg(sess, image_data)
        return image.shape[0], image.shape[1]

    def decode_jpeg(self, sess, image_data):
        image = sess.run(self._decode_jpeg,
                        feed_dict={self._decode_jpeg_data: image_data})
        assert len(image.shape) == 3
        assert image.shape[2] == 3
        return image

class DataSort():

    def __init__(self):

        self._confs = {}
        with open('model/confs.json') as confs:

            self._confs = json.loads(confs.read())

    def processFilesAndClasses(self):

        """

        Returns a list of filenames and inferred class names.

        Returns:

            A list of image file paths, relative to `dataset_dir` and the list of
            subdirectories, representing class names.

        """

        class_names = [
            name for name in os.listdir(self._confs["ClassifierSettings"]["dataset_dir"]) if os.path.isdir(os.path.join(self._confs["ClassifierSettings"]["dataset_dir"],name))]

        directories = []

        for dirName in os.listdir(self._confs["ClassifierSettings"]["dataset_dir"]):

            path = os.path.join(self._confs["ClassifierSettings"]["dataset_dir"], dirName)
            ##print(path)

            if os.path.isdir(path):

                #print("APPENDING")
                directories.append(path)

        #print(class_names)
        #print(directories)

        photoPaths = []

        for directory in directories:

            for filename in os.listdir(directory):

                if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.gif'):

                    path = os.path.join(directory, filename)
                    photoPaths.append(path)
                    print(filename)
                    print("-- Image Added")
                    print("")

                else:

                    print(filename)
                    print("-- Invalid Image Skipped")
                    print("")
                    continue

        #print(sorted(class_names))

        return photoPaths, sorted(class_names)

    def convertToTFRecord(self, split_name, filenames, class_names_to_ids):

        """

        Converts the given filenames to a TFRecord dataset.

        Args:

            split_name: The name of the dataset, either 'train' or 'validation'.
            filenames: A list of absolute paths to png or jpg images.
            class_names_to_ids: A dictionary from class names (strings) to ids
            (integers).

        """
        assert split_name in ['train', 'validation']

        num_per_shard = int(math.ceil(len(filenames) / float(self._confs["ClassifierSettings"]["num_shards"])))
        print("-- NUMBER FILES ", len(filenames))
        print("-- NUMBER PER SHARD ", num_per_shard)

        with tf.Graph().as_default():

            image_reader = ImageReader()

            with tf.Session('') as sess:

                for shard_id in range(self._confs["ClassifierSettings"]["num_shards"]):

                    output_filename = self.getDatasetFilename(split_name, shard_id)
                    print("-- SAVING ", output_filename)
                    print("")

                    with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:

                        start_ndx = shard_id * num_per_shard
                        end_ndx = min((shard_id+1) * num_per_shard, len(filenames))

                        for i in range(start_ndx, end_ndx):

                            sys.stdout.write('\r>> Converting image %d/%d shard %d' % (
                                i+1, len(filenames), shard_id))
                            sys.stdout.flush()
                            print("")

                            # Read the filename:
                            image_data = tf.gfile.FastGFile(filenames[i], 'rb').read()

                            height, width = image_reader.read_image_dims(sess, image_data)

                            class_name = os.path.basename(os.path.dirname(filenames[i]))
                            class_id = class_names_to_ids[class_name]

                            print("class_name", class_name)
                            print("class_id", class_id)
                            print("")

                            example = self.imageToTFExample(
                                image_data, b'jpg', height, width, class_id)

                            tfrecord_writer.write(example.SerializeToString())

        sys.stdout.write('\n')
        sys.stdout.flush()

    def getDatasetFilename(self, split_name, shard_id):

        output_filename = '%s_%s_%05d-of-%05d.tfrecord' % (
            self._confs["ClassifierSettings"]["tfrecord_filename"], split_name, shard_id, self._confs["ClassifierSettings"]["num_shards"])

        return os.path.join(self._confs["ClassifierSettings"]["dataset_dir"], output_filename)

    def int64Feature(self, values):

        """

        Returns a TF-Feature of int64s.

        Args:

            values: A scalar or list of values.

        Returns:

            a TF-Feature.

        """
        if not isinstance(values, (tuple, list)):

            values = [values]

        return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

    def bytesFeature(self, values):

        """

        Returns a TF-Feature of bytes.

        Args:

            values: A string.

        Returns:

            a TF-Feature.

        """
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

    def imageToTFExample(self, image_data, image_format, height, width, class_id):

        return tf.train.Example(features=tf.train.Features(feature={
            'image/encoded': self.bytesFeature(image_data),
            'image/format': self.bytesFeature(image_format),
            'image/class/label': self.int64Feature(class_id),
            'image/height': self.int64Feature(height),
            'image/width': self.int64Feature(width)
        }))

    def writeLabels(self, labels_to_class_names):

        """

        Writes a file with the list of class names.

        Args:

            labels_to_class_names: A map of (integer) labels to class names.
            filename: The filename where the class names are written.

        """

        labels_filename = os.path.join(self._confs["ClassifierSettings"]["dataset_dir"], self._confs["ClassifierSettings"]["labels"])

        with tf.gfile.Open(self._confs["ClassifierSettings"]["classes"], 'w') as f:

            for label in labels_to_class_names:

                f.write('%s\n' % (label))

        with tf.gfile.Open(labels_filename, 'w') as f:

            for label in labels_to_class_names:

                class_name = labels_to_class_names[label]

                f.write('%d:%s\n' % (label, class_name))