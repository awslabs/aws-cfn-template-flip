"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import imp
import six
import collections

custom_yaml = imp.load_module("custom_yaml", *imp.find_module("yaml"))

TAG_MAP = "tag:yaml.org,2002:map"
TAG_STRING = "tag:yaml.org,2002:str"
UNCONVERTED_SUFFIXES = ["Ref", "Condition"]

def multi_constructor(loader, tag_suffix, node):
    """
    Deal with !Ref style function format
    """

    if tag_suffix not in UNCONVERTED_SUFFIXES:
        tag_suffix = "Fn::{}".format(tag_suffix)

    constructor = None

    if tag_suffix == "Fn::GetAtt":
        constructor = construct_getatt
    elif isinstance(node, custom_yaml.ScalarNode):
        constructor = loader.construct_scalar
    elif isinstance(node, custom_yaml.SequenceNode):
        constructor = loader.construct_sequence
    elif isinstance(node, custom_yaml.MappingNode):
        constructor = loader.construct_mapping
    else:
        raise "Bad tag: !{}".format(tag_suffix)

    return  {
        tag_suffix: constructor(node)
    }

def construct_getatt(node):
    """
    Reconstruct !GetAtt into a list
    """

    return node.value.split(".")

def construct_mapping(self, node, deep=False):
    """
    Use OrderedDict for maps
    """

    mapping = collections.OrderedDict()

    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        value = self.construct_object(value_node, deep=deep)

        mapping[key] = value

    return mapping

class odict_items(list):
    """
    Helper class to ensure ordering is preserved
    """

    def __init__(self, items):
        new_items = []

        for item in items:
            class C(type(item)):
                def __lt__(self, *args, **kwargs):
                    return False

            new_items.append(C(item))

        return super(odict_items, self).__init__(new_items)

    def sort(self):
        pass

class ODict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        super(ODict, self).__init__(*args, **kwargs)

        items = odict_items(self.items())
        self.items = lambda: items

def representer(dumper, data):
    """
    Deal with !Ref style function format and OrderedDict
    """

    if len(data.keys()) != 1:
        data = ODict(data)

        return dumper.represent_mapping(TAG_MAP, data, flow_style=False)

    key = list(data)[0]
    tag = key

    if key not in UNCONVERTED_SUFFIXES and not key.startswith("Fn::"):
        return dumper.represent_mapping(TAG_MAP, data, flow_style=False)

    if key.startswith("Fn::"):
        tag = key[4:]

    tag = "!{}".format(tag)

    data = data[key]

    if tag == "!GetAtt":
        data = "{}.{}".format(data[0], data[1])

    if isinstance(data, dict):
        return dumper.represent_mapping(tag, data, flow_style=False)
    elif isinstance(data, list):
        return dumper.represent_sequence(tag, data, flow_style=True)

    return dumper.represent_scalar(tag, data)

# Customise our yaml
custom_yaml.add_representer(six.text_type, lambda dumper, value: dumper.represent_scalar(TAG_STRING, value))
custom_yaml.add_constructor(TAG_MAP, construct_mapping)
custom_yaml.add_multi_constructor("!", multi_constructor)
custom_yaml.add_representer(collections.OrderedDict, representer)
custom_yaml.add_representer(dict, representer)
