"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from .custom_yaml import yaml
import collections
import json

def to_json(data):
    """
    Convert the data to json
    undoing yaml short syntax where detected
    """

    return json.dumps(data, indent=4)

def to_yaml(data):
    """
    Convert the data to yaml
    using yaml short syntax for functions where possible
    """

    return yaml.dump(data)

def flip(template):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    try:
        data = json.loads(template, object_pairs_hook=collections.OrderedDict)
        return to_yaml(data)
    except ValueError:
        pass  # Hand over to the yaml parser

    try:
        data = yaml.load(template)
        return to_json(data)
    except Exception as e:
        raise Exception("Could not determine the input format. Perhaps it's malformed?")
