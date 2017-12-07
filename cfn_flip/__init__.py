"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from .clean import clean
from .custom_json import DateTimeAwareJsonEncoder
from .custom_yaml import CustomDumper, CustomLoader
import collections
import json
import yaml

def _load_json(template):
    """
    We've decided it's JSON, so let's try to load it
    """

    try:
        return json.loads(template, object_pairs_hook=collections.OrderedDict)
    except ValueError:
        raise Exception("Invalid JSON")

def _load_yaml(template):
    """
    We've decided it's YAML, so let's try to load it
    """

    try:
        return yaml.load(template, Loader=CustomLoader)
    except:
        raise Exception("Invalid YAML")

def _load(template):
    """
    Try to guess the input format
    """

    try:
        data = _load_json(template)
        return data, "json"
    except:
        data = _load_yaml(template)
        return data, "yaml"

def _dump_json(data):
    """
    Output some JSON
    """

    return json.dumps(data, indent=4, cls=DateTimeAwareJsonEncoder)

def _dump_yaml(data):
    """
    Output some YAML
    """

    return yaml.dump(data, Dumper=CustomDumper, default_flow_style=False)

def to_json(template, clean_up=False):
    """
    Assume the input is YAML and convert to JSON
    """

    data = _load_yaml(template)

    if clean_up:
        data = clean(data)

    return _dump_json(data)

def to_yaml(template, clean_up=False):
    """
    Assume the input is JSON and convert to YAML
    """

    data = _load_json(template)

    if clean_up:
        data = clean(data)

    return _dump_yaml(data)

def flip(template, out_format=None, clean_up=False, no_flip=False):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    data = None
    in_format = None

    if no_flip:
        in_format = out_format
    elif out_format == "json":
        in_format = "yaml"
    elif out_format == "yaml":
        in_format = "json"

    if in_format == "json":
        data = _load_json(template)
    elif in_format == "yaml":
        data = _load_yaml(template)
    else:
        try:
            data, in_format = _load(template)
        except Exception as e:
            raise Exception("Could not determine the input format")

    if no_flip:
        out_format = in_format
    elif in_format == "json":
        out_format = "yaml"
    else:
        out_format = "json"

    if clean_up:
        data = clean(data)

    if out_format == "json":
        return _dump_json(data)

    return _dump_yaml(data)
