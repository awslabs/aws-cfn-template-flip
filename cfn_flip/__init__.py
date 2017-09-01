"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from .clean import clean
from .custom_json import DateTimeAwareJsonEncoder
from .custom_yaml import custom_yaml
import collections
import json

class MyDumper(custom_yaml.Dumper):
  """
  Indent block sequences from parent using more common style
  ("  - entry"  vs "- entry").  
  Causes fewer problems with validation and tools.
  """
  def increase_indent(self,flow=False, indentless=False):
    return super(MyDumper,self).increase_indent(flow, False)

def _load(template, clean_up):
    try:
        fmt, data = "json", json.loads(template, object_pairs_hook=collections.OrderedDict)
    except Exception:
        try:
            fmt, data = "yaml", custom_yaml.load(template)
        except Exception as e:
            raise Exception("Could not determine the input format: {}", e, template)
    if clean_up:
        data = clean(data)
    return fmt, data

def _json(template):
    return json.dumps(template, indent=4, cls=DateTimeAwareJsonEncoder)

def _yaml(template):
    return custom_yaml.dump(template, Dumper=MyDumper, default_flow_style=False)

def to_json(template, clean_up=False):
    """
    Convert the data to json
    undoing yaml short syntax where detected
    """
    fmt, data = _load(template, clean_up)
    if fmt == "json":
        raise ValueError("Expected to_json() input to be non-JSON")
    return _json(data)

def to_yaml(template, clean_up=False):
    """
    Convert the data to yaml
    using yaml short syntax for functions where possible
    """
    fmt, data = _load(template, clean_up)
    if fmt == "yaml":
        raise ValueError("Expected to_yaml() input to be non-YAML")
    return _yaml(data)

def flip(template, output_json=False, output_yaml=False, clean_up=False):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    fmt, data = _load(template, clean_up)
    flip = not output_json and not output_yaml

    if output_json or (flip and fmt == "yaml"):
        return _json(data)
    elif output_yaml or (flip and fmt == "json"):
        return _yaml(data)
