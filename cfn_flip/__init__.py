"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import six
import collections
import json
import yaml

yaml.add_representer(six.text_type, lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))

def multi_constructor(loader, tag_suffix, node):
    """
    Deal with !Ref style function format
    """

    if tag_suffix != "Ref":
        tag_suffix = "Fn::{}".format(tag_suffix)

    constructor = None

    if isinstance(node, yaml.ScalarNode):
        constructor = loader.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.construct_mapping
    else:
        raise "Bad tag: !{}".format(tag_suffix)

    return {
        tag_suffix: constructor(node)
    }

yaml.add_multi_constructor("!", multi_constructor)

def construct_mapping(self, node, deep=False):
    """
    Ensure mappings are vanilla
    """

    mapping = collections.OrderedDict()

    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        value = self.construct_object(value_node, deep=deep)

        mapping[key] = value

    return mapping

yaml.add_constructor("tag:yaml.org,2002:map", construct_mapping)

class odict_items(list):
    def sort(self):
        pass

def representer(dumper, data):
    """
    Deal with !Ref style function format
    """

    if len(data.keys()) != 1:
        items = odict_items(data.items())
        data.items = lambda: items

        return dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=False)

    key = list(data)[0]
    tag = key

    if key != "Ref" and not key.startswith("Fn::"):
        return dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=False)

    if key.startswith("Fn::"):
        tag = key[4:]

    tag = "!{}".format(tag)

    data = data[key]

    if isinstance(data, dict):
        return dumper.represent_mapping(tag, data, flow_style=False)
    elif isinstance(data, list):
        return dumper.represent_sequence(tag, data, flow_style=True)

    return dumper.represent_scalar(tag, data)

yaml.add_representer(collections.OrderedDict, representer)

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

    return yaml.dump(data, encoding="utf-8")

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
