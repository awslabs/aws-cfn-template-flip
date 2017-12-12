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
TAG_STRING = "tag:yaml.org,2002:str"


class CfnYamlDumper(yaml.Dumper):
    """
    Indent block sequences from parent using more common style
    ("  - entry"  vs "- entry").
    Causes fewer problems with validation and tools.
    """

    def increase_indent(self, flow=False, indentless=False):
            return super(CfnYamlDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
            if isinstance(value, six.text_type):
                if "\n" in value and style is None:
                    style = "\""

                # return super(CfnYamlDumper, self).represent_scalar(TAG_STRING, value, style)

            return super(CfnYamlDumper, self).represent_scalar(tag, value, style)


def string_representer(dumper, value):
    style = None

    if "\n" in value:
        style = "\""

    return dumper.represent_scalar(TAG_STRING, value, style=style)


def map_representer(dumper, value):
    """
    Map ODict into ODict to prevent sorting
    """

    return dumper.represent_mapping(TAG_MAP, value)


# Customise the dumper
CfnYamlDumper.add_representer(ODict, map_representer)
CfnYamlDumper.add_representer(six.text_type, string_representer)
