"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from .odict import ODict
import collections
import six
import yaml

TAG_MAP = "tag:yaml.org,2002:map"
CONVERTED_SUFFIXES = ["Ref", "Condition"]

FN_PREFIX = "Fn::"

class BaseDumper(yaml.Dumper):
    """
    Indent block sequences from parent using more common style
    ("  - entry"  vs "- entry").
    Causes fewer problems with validation and tools.
    """
  
    def increase_indent(self, flow=False, indentless=False):
        return super(BaseDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
        if "\n" in value and style is None:
            style = "\""

        return super(BaseDumper, self).represent_scalar(tag, value, style)

class BaseCleanDumper(BaseDumper):
    """
    Format multi-line strings with |
    """

    def represent_scalar(self, tag, value, style=None):
        if "\n" in value:
            style = "|"

        return super(BaseCleanDumper, self).represent_scalar(tag, value, style)

class Dumper(BaseDumper):
    """
    The standard dumper
    """

class CleanDumper(BaseCleanDumper):
    """
    Cleans up strings
    """

class LongDumper(BaseDumper):
    """
    Preserves long-form function syntax
    """

class LongCleanDumper(BaseCleanDumper):
    """
    Preserves long-form function syntax
    """

def fn_representer(dumper, fn_name, value):
    tag = "!{}".format(fn_name)

    if tag == "!GetAtt" and isinstance(value, list):
        value = ".".join(value)

    if isinstance(value, list):
        return dumper.represent_sequence(tag, value)

    if isinstance(value, dict):
        return dumper.represent_mapping(tag, value)

    return dumper.represent_scalar(tag, value)

def map_representer(dumper, value):
    """
    Deal with !Ref style function format and OrderedDict
    """

    value = ODict(value)

    if len(value.keys()) == 1:
        key = list(value.keys())[0]

        if key in CONVERTED_SUFFIXES:
            return fn_representer(dumper, key, value[key])
    
        if key.startswith(FN_PREFIX):
            return fn_representer(dumper, key[4:], value[key])

    return dumper.represent_mapping(TAG_MAP, value, flow_style=False)

# Customise our dumpers
Dumper.add_representer(collections.OrderedDict, map_representer)
CleanDumper.add_representer(collections.OrderedDict, map_representer)

def get_dumper(clean_up=False, long_form=False):
    if clean_up:
        if long_form:
            return LongCleanDumper

        return CleanDumper

    if long_form:
        return LongDumper

    return Dumper
