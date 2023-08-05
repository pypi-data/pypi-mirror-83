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

from .categories import Categories

class ModelMetadata():
    category = ''
    name = ''
    last_modified = ''
    description = ''
    version = 0
    features = {}


    def __init__(self, f=None, minio_obj=None):
        if f is not None:
            if 'category' in f: self.category = Categories(f['category'])
            if 'name' in f: self.name = f['name']
            if 'last_modified' in f: self.last_modified = time.strftime('%H:%M:%S - %d/%m/%Y', f['last_modified'])
            if 'description' in f: self.description = f['description']
            if 'version' in f: self.version = f['version']
            if 'features' in f: self.features = f['features']
        else:
            pass

    # def seria
    def pretty_print(self):
        row_format ="{:<30}" * 2
        print(row_format.format(*['Category:', self.category.value]))
        print(row_format.format(*['Name:', self.name]))
        print(row_format.format(*['Description:', self.description]))
        print(row_format.format(*['Last modified:', str(self.last_modified)]))
        print(row_format.format(*['Version:', self.version]))
        print(row_format.format(*['Features:', str(self.features)]))

    def dump_to_file(self, path):
        with open(path+'/metadata.json', 'w') as f:
            f.write(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))

