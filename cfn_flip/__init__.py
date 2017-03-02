"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from .clean import clean
from .custom_json import DateTimeAwareJsonEncoder
from .custom_yaml import yaml
import collections
import json

def to_json(template, clean_up=False):
    """
    Convert the data to json
    undoing yaml short syntax where detected
    """

    data = yaml.load(template)

    if clean_up:
        data = clean(data)

    return json.dumps(data, indent=4, cls=DateTimeAwareJsonEncoder)

def to_yaml(template, clean_up=False):
    """
    Convert the data to yaml
    using yaml short syntax for functions where possible
    """

    data = json.loads(template, object_pairs_hook=collections.OrderedDict)

    if clean_up:
        data = clean(data)

    return yaml.dump(data, default_flow_style=False)

def flip(template, clean_up=False):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    try:
        return to_yaml(template, clean_up)
    except ValueError:
        pass  # Hand over to the yaml parser

    try:
        return to_json(template, clean_up)
    except Exception as e:
        raise Exception("Could not determine the input format: {}", e)
