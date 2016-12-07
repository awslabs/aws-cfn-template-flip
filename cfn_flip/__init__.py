"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from .custom_yaml import yaml
import collections
import json

def to_json(template):
    """
    Convert the data to json
    undoing yaml short syntax where detected
    """

    data = yaml.load(template)

    return json.dumps(data, indent=4)

def to_yaml(template):
    """
    Convert the data to yaml
    using yaml short syntax for functions where possible
    """

    data = json.loads(template, object_pairs_hook=collections.OrderedDict)

    return yaml.dump(data)

def flip(template):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    try:
        return to_yaml(template)
    except ValueError:
        pass  # Hand over to the yaml parser

    try:
        return to_json(template)
    except Exception:
        raise Exception("Could not determine the input format. Perhaps it's malformed?")
