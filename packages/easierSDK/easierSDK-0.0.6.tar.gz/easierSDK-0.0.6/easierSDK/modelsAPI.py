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

import minio
from minio import Minio
import urllib3
import os
import subprocess
import tensorflow as tf
import joblib
from shutil import rmtree
import json
import tensorflow.keras.backend as K

from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.model import Model
import easierSDK.classes.constants as constants


class ModelsAPI():
    GLOBAL = 'global'
    MODELS = 'models'
    BASE_MODELS_PATH = './models'
    MAX_FOLDER_SIZE = 2000 # Kbytes = 2M
    MAX_FOLDER_SIZE_STR = '2MB'

    def __init__(self, minio_url: str, minio_user:str, minio_password:str):
        if not os.path.isdir(self.BASE_MODELS_PATH): os.mkdir(self.BASE_MODELS_PATH)
        self.minio_bucket = minio_user
        self.minio_client = Minio(minio_url, access_key=minio_user, secret_key=minio_password, secure=True, region='es')
        self.minio_bucket_public = minio_user + '-public'
        self.minio_bucket_private = minio_user + '-private' 

    def show_available_repos(self):
        ob_list = self.minio_client.list_buckets()
        for ob in ob_list:
            print(ob)

    def show_categories(self):
        print("CATEGORIES:")
        [print("- ", category.value) for category in Categories]

    def show_models(self, category:Categories=None):
        if category:
            objects = self.minio_client.list_objects(self.GLOBAL, prefix=self.MODELS + '/' + category.value, recursive=True)
        else:
            objects = self.minio_client.list_objects(self.GLOBAL, prefix=self.MODELS, recursive=True)
        already_printed = []
        row_format ="{:<30}" * 4
        print(row_format.format(*['Repository', 'Category', 'Name', 'Size']))
        for item in objects:
            repo_name = item.bucket_name
            name = item.object_name.split('/')[1]
            cat = item.object_name.split('/')[0]
            if [name, cat] in already_printed:
                continue
            already_printed.append([name, cat])
            size = item.size            
            print(row_format.format(*[repo_name, cat, name, size]))

    def show_model_info(self, repo_name:str, category:Categories, model_name:str):

        if not self.minio_client.bucket_exists(repo_name):
            print('ERROR: Repository name does not exist. Please check and try again')
            return None

        filename = self.MODELS + '/' + category.value + '/' + model_name + '/' + 'metadata.json'
        local_path = './models/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_path)
        except minio.error.NoSuchKey as ex:
            print('ERROR: Wrong dataset name or category, please check and try again.')
            return None
        
        with open(local_path, 'r') as f:
            metadata = ModelMetadata(json.load(f), minio_obj)
            metadata.pretty_print()

    def download(self, model_name:str, repo_name:str, category:Categories, path_to_download:str):
        if not self.minio_client.bucket_exists(repo_name):
            print('ERROR: Repository name does not exist. Please check and try again')
            return None
        
        # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
        minio_path = self.MODELS + '/' + category.value + '/' + model_name
        local_path = path_to_download + '/' + minio_path
        try:
            objects = self.minio_client.list_objects(minio_path)
            for minio_object in objects:
                minio_obj = self.minio_client.fget_object(repo_name, minio_path + minio_object.object_name, local_path + "/" + minio_object.object_name)
        except minio.error.NoSuchKey as ex:
            print('ERROR: Wrong model name or category, please check and try again.')
            return None
        return local_path

    def load_from_local(self, path:str):
        model = Model()
        for obj in os.listdir(path):
            extension = obj.split(".")[1:]
            # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
            if extension == constants.MODEL_EXTENSION:
                model.set_tf_model(tf.keras.models.load_model(path + '/' + obj))
            elif extension == constants.SCALER_EXTENSION:
                model.set_scaler(joblib.load(path + '/' + obj))
            elif extension == constants.LABELENCODER_EXTENSION:
                model.set_label_encoder(joblib.load(path + '/' + obj))
            elif extension == constants.ONEHOTENCODER_EXTENSION:
                model.set_feature_encoder(joblib.load(path + '/' + obj))
            elif extension == constants.JSON_EXTENSION:
                metadata = ModelMetadata(f=json.load(path + '/' + obj))
                model.set_metadata(metadata)
            elif extension == constants.TF_LITE_EXTENSION: 
                model.set_tf_lite_model_path(path + '/' + obj)
            elif extension == constants.TPU_EXTENSION:
                model.set_tpu_model_path(path + '/' + obj)
            else:
                print("File extension not known: ." + extension)
        
        return model

    def load_from_repository(self, model_name:str, repo_name:str, category:Categories):
        # TODO revise experiment_id
        if not os.path.isdir('/tmp/download'): os.mkdir('/tmp/download')
        path = self.download(model_name, repo_name, self.MODELS + '/' + category.value, path_to_download='/tmp/download')
        model = Model()
        for obj in os.listdir(path):
            extension = obj.split(".")[1:]
            # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
            if extension == constants.MODEL_EXTENSION:
                model.set_tf_model(tf.keras.models.load_model(path + '/' + obj))
            elif extension == constants.SCALER_EXTENSION:
                model.set_scaler(joblib.load(path + '/' + obj))
            elif extension == constants.LABELENCODER_EXTENSION:
                model.set_label_encoder(joblib.load(path + '/' + obj))
            elif extension == constants.ONEHOTENCODER_EXTENSION:
                model.set_feature_encoder(joblib.load(path + '/' + obj))
            elif extension == constants.JSON_EXTENSION:
                metadata = ModelMetadata(f=json.load(path + '/' + obj))
                model.set_metadata(metadata)
            elif extension == constants.TF_LITE_EXTENSION: 
                model.set_tf_lite_model_path(path + '/' + obj)
            elif extension == constants.TPU_EXTENSION:
                model.set_tpu_model_path(path + '/' + obj)
            else:
                print("File extension not known: ." + extension)
        
        return model

    def upload(self, category:Categories, model:Model, public=False, remove_dir=True):
        path = model.store(print_files=False)
        minio_path = self.MODELS + '/' + category.value + '/' + model.metadata.name
        # TODO revise experiment_id
        try:
            for obj in os.listdir(path):
                if public:
                    bucket = self.minio_bucket_public
                else:
                    bucket = self.minio_bucket_private
                # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
                self.minio_client.fput_object(bucket, minio_path + '/' + obj, path + '/' + obj)
            if remove_dir: rmtree(path)
        except Exception as ex:
            print("ERROR: Error during upload to MINIO.")
            return False
        return True

    def compile_tflite(self, model:Model, calibration_data, path:str=BASE_MODELS_PATH + "/storage/"):
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path
        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        model.set_representative_data(samples = calibration_data)

        if model.tf_model is None and model.tf_model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(model.tf_model_dir)
        elif model.tf_model is not None:
            if tf.__version__.split(".")[0] == '1':
                model.tf_model.save("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
                # Clear graph in prep for next step.
                try:
                    K.clear_session()
                except Exception as e:
                    pass                
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(model.tf_model)

        converter.representative_dataset = model.representative_dataset_gen
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return False

        if model.tf_model_dir != '':
            tf_lite_model_path = path + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            print("Converted tf model " + str(model.tf_model_dir) + " to tf lite")
        else:
            tf_lite_model_path = path + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            # Clear graph in prep for next step.
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted keras model " + model.metadata.name + " to tf lite")

        model.set_tf_lite_model_path(tf_lite_model_path)

    def compile_tpu(self,  model:Model, calibration_data, path:str=BASE_MODELS_PATH + "/storage/"):
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path

        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        model.set_representative_data(samples = calibration_data)

        if model.tf_model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(model.tf_model_dir)
        else:
            if tf.__version__.split(".")[0] == '1':
                if not os.path.isfile("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION):
                    model.tf_model.save("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(model.tf_model)

        if tf.__version__.split(".")[0] == '1':
            converter.target_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]        
        else:
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.representative_dataset = model.representative_dataset_gen
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return

        if model.tf_model_dir is not None:
            open('/tmp/storage/' + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                tflite_model)
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted tf model " + str(model.tf_model_dir) + " to tf lite specific for TPU")
            tpu_model_path = "/tmp/storage/" + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', tpu_model_path, '-o', '/tmp/storage']
            tpu_model_path = "/tmp/storage/" + model.tf_model_dir + "/" + model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        else:
            try:
                open('/tmp/storage/' + model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                    tflite_model)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                print("Converted keras model " + model.metadata.name + " to tf lite specific for TPU")
            except Exception as e:
                print("Error saving tf lite model to file: " + str(e))
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                return False
            tpu_model_path = "/tmp/storage/" +  model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', '-o', '/tmp/storage', tpu_model_path]
            tpu_model_path = "/tmp/storage/" +  model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            model.set_tpu_model_path(tpu_model_path)
        except FileNotFoundError as e:
            print('The edge tpu complier is not installed: ' + str(e))
            return False
        except Exception as e:
            print('The edge tpu complier throwed an error: ' + str(e))
            return False
        return True

    # TODO check if necessary
    def compile_gpu(self):
        pass      
    