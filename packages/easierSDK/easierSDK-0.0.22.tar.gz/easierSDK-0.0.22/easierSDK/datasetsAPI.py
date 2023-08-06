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

from easierSDK.classes.categories import Categories
from easierSDK.classes.dataset_metadata import DatasetMetadata

import json
class DatasetsAPI():
    GLOBAL = 'global'
    DATASETS = 'datasets'
    BASE_DATASET_PATH = './datasets/'
    MAX_FOLDER_SIZE = 2000 # Kbytes = 2M
    MAX_FOLDER_SIZE_STR = '2MB'

    def __init__(self, minio_url: str, minio_user:str, minio_password:str):
        # JCA: Need to catch exceptions
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
        # JCA: Could be useful to also show number of datasets, size...

    def show_datasets(self, category:Categories=None):
        if category:
            objects = self.minio_client.list_objects(self.GLOBAL, prefix=self.DATASETS + '/' + category.value, recursive=True)
        else:
            objects = self.minio_client.list_objects(self.GLOBAL, prefix=self.DATASETS, recursive=True)
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

    def show_dataset_info(self, repo_name:str, category:Categories, dataset_name:str):
        # 1. Check bucket exists
        if not self.minio_client.bucket_exists(repo_name):
            print('ERROR: Repository name does not exist. Please check and try again')
            return None
        # 2. Download file

        # 3. Check file has been downloaded

        filename = self.DATASETS + '/' + category.value + '/' + dataset_name + '/' + 'metadata.json'
        print(filename)
        local_path = './datasets/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_path)
        except minio.error.NoSuchKey as ex:
            print('ERROR: Wrong dataset name or category, please check and try again.')
            return None
        # 4. Read file and format metadata
        with open(local_path, 'r') as f:
            metadata = DatasetMetadata(json.load(f), minio_obj)
            metadata.pretty_print()

    def download(self, category:Categories, dataset_name:str, path_to_download:str, repo=GLOBAL) -> bool:
        # 1. Check if bucket exists
        if not self.minio_client.bucket_exists(repo):
            print('ERROR: Wrong repo name. Please check and try again')
            return False
        # 2. Check if dataset exists
        filename = self.DATASETS + '/' + category.value + '/' + dataset_name + '/'
        object_list = self.minio_client.list_objects(repo, prefix=filename, recursive=True)
        has_items = False
        # 3. Download
        for obj in object_list:
            if not obj.is_dir:
                has_items = True
                self.minio_client.fget_object(repo, obj.object_name, path_to_download+'/'+obj.object_name)
        if not has_items:
            print('ERROR: Could not find file. Please check parameters and try again.')
            return False
        # 4. If there are no problems, return True
        return True

    def upload(self, category:Categories, dataset_name:str, local_path:str, metadata:DatasetMetadata=None, public:bool=False) -> bool:
        '''
            @local_path refers to the root folder for the dataset. All the files under it will be uploaded
            returns True if all files have uploaded correctly, False if some file gave error.
        '''
        # 1. Check path exists
        if not os.path.isdir(local_path):
            print('ERROR: Path does not exist. Please save it and then upload again.')
            return False
        # 2. Check folder size is not too big (parametrized)
        size = subprocess.check_output(['du','-sx', local_path]).split()[0].decode('utf-8')
        if int(size) > self.MAX_FOLDER_SIZE:
            print('ERROR: Folder size too big. Current folder size is {}KB and max upload size is {}'.format(size, self.MAX_FOLDER_SIZE_STR))
            return False
        # 3. Dump metadata into file
        metadata.dump_to_file(local_path)
        # 4. Upload all files in the path
        minio_path = 'datasets/' + category.value + '/' + dataset_name
        error = False
        for root, subdirs, files in os.walk(local_path):
            for f in files:
                file_path = (minio_path + root.replace(local_path, '/') + f).replace('//', '/')
                try:
                    if public:
                       bucket = self.minio_bucket_public
                    else:
                       bucket = self.minio_bucket_private
                    a, b =self.minio_client.fput_object(bucket, file_path, root+'/'+f)
                except Exception as ex:
                    print('ERROR: Unknown error uploading file {}: {}'.format(f, ex))
                    error = True

        if error: 
            print('Finished uploading dataset with some errors.')
            return False
        else:
            print('Finished uploading dataset with no errors.')
            return True

