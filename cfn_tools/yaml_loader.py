"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from .odict import ODict
import six
import yaml

TAG_MAP = "tag:yaml.org,2002:map"
UNCONVERTED_SUFFIXES = ["Ref", "Condition"]
FN_PREFIX = "Fn::"


class CfnYamlLoader(yaml.SafeLoader):
    pass


def multi_constructor(loader, tag_suffix, node):
    """
    Deal with !Ref style function format
    """

    if tag_suffix not in UNCONVERTED_SUFFIXES:
        tag_suffix = "{}{}".format(FN_PREFIX, tag_suffix)

    constructor = None

    if tag_suffix == "Fn::GetAtt":
        constructor = construct_getatt
    elif isinstance(node, yaml.ScalarNode):
        constructor = loader.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.construct_mapping
    else:
        raise Exception("Bad tag: !{}".format(tag_suffix))

    return ODict((
        (tag_suffix, constructor(node)),
    ))


def construct_getatt(node):
    """
    Reconstruct !GetAtt into a list
    """

    if isinstance(node.value, six.text_type):
        return node.value.split(".", 1)
    elif isinstance(node.value, list):
        return [s.value for s in node.value]
    else:
        raise ValueError("Unexpected node type: {}".format(type(node.value)))


def construct_mapping(self, node, deep=False):
    """
    Use ODict for maps
    """

    mapping = ODict()

    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        value = self.construct_object(value_node, deep=deep)

        mapping[key] = value

    return mapping


# Customise our loader
CfnYamlLoader.add_constructor(TAG_MAP, construct_mapping)
CfnYamlLoader.add_multi_constructor("!", multi_constructor)
