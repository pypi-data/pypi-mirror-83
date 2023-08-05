#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.

import sys
sys.path.append('..')
sys.path.append('.')

import time
import json
import os
import joblib
import random
import string
from shutil import copyfile
import tensorflow as tf
import numpy

import easierSDK.classes.constants as constants
from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata

class Model():
    metadata = None
    tf_model = None
    scaler = None
    label_encoder = None
    feature_encoder = None
    tf_lite_model_path = ''
    tpu_model_path = ''
    gpu_model_path = ''
    tf_model_dir = ''
    samples = None

    def __init__(self, metadata:ModelMetadata=None):
        self.metadata = metadata

    def set_metadata(self, metadata):
        self.metadata = metadata
    def get_metadata(self):
        return self.metadata

    def set_tf_model(self, tf_model):
        self.tf_model = tf_model
    def get_tf_model(self):
        return self.tf_model
    
    def set_scaler(self, scaler):
        self.scaler = scaler
    def get_scaler(self):
        return self.scaler
    
    def set_label_encoder(self, label_encoder):
        self.label_encoder = label_encoder
    def get_label_encoder(self):
        return self.label_encoder
    
    def set_feature_encoder(self, feature_encoder):
        self.feature_encoder = feature_encoder
    def get_feature_encoder(self):
        return self.feature_encoder
    
    def set_tf_lite_model_path(self, tf_lite_model_path):
        self.tf_lite_model_path = tf_lite_model_path
    def get_tf_lite_model_path(self):
        return self.tf_lite_model_path

    def set_tpu_model_path(self, tpu_model_path):
        self.tpu_model_path = tpu_model_path
    def get_tpu_model_path(self):
        return self.tpu_model_path
    
    def set_gpu_model_path(self, gpu_model_path):
        self.gpu_model_path = gpu_model_path
    def get_gpu_model_path(self):
        return self.gpu_model_path

    def set_representative_data(self, samples):
        self.samples = samples
    def get_representative_data(self):
        return self.samples
    
    def __get_random_string(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(0, 16))) 

    def store(self, model_path:str=None, print_files=True):
        files_print = ""
        if model_path is None:
            path = '/tmp/' + self.__get_random_string()
            os.mkdir(path)
        else:
            path = model_path
        self.metadata.dump_to_file(path)
        self.tf_model.save(path + self.metadata.name + '.h5')
        if self.scaler: 
            joblib.dump(self.scaler, '/tmp' + model_path + 'scaler.pkl')
            files_print += "\n\t- scaler.pkl"
        if self.label_encoder: 
            joblib.dump(self.label_encoder, '/tmp' + model_path + 'label_encoder.pkl')
            files_print += "\n\t- label_encoder.pkl"
        if self.feature_encoder: 
            joblib.dump(self.feature_encoder, '/tmp' + model_path + 'feature_encoder.pkl')
            files_print += "\n\t- feature_encoder.pkl"
        if self.tf_lite_model_path: 
            copyfile(self.tf_lite_model_path, path + self.tf_lite_model_path.split('/')[-1])
            files_print += "\n\t- " + self.tf_lite_model_path.split('/')[-1]
        if self.tpu_model_path: 
            copyfile(self.tpu_model_path, path + self.tpu_model_path.split('/')[-1])
            files_print += "\n\t- " + self.tpu_model_path.split('/')[-1]
        if self.gpu_model_path: 
            copyfile(self.gpu_model_path, path + self.gpu_model_path.split('/')[-1])
            files_print += "\n\t- " + self.gpu_model_path.split('/')[-1]
        
        if print_files:
            print("Stored files in " + path + ":\n\t- metadata.json" + ":\n\t- " + self.metadata.name + '.h5' + files_print)
        return path

    def representative_dataset_gen(self):
        for i in range(len(self.samples)):
            data = numpy.array(self.samples[i: i + 1], dtype=numpy.float32)
            yield [data]
