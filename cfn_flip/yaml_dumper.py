"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

import six

from cfn_clean.yaml_dumper import CleanCfnYamlDumper
from cfn_tools.literal import LiteralString
from cfn_tools.odict import ODict
from cfn_tools.yaml_dumper import CfnYamlDumper
from cfn_tools._config import config

TAG_STR = "tag:yaml.org,2002:str"
TAG_MAP = "tag:yaml.org,2002:map"
CONVERTED_SUFFIXES = ["Ref", "Condition"]

FN_PREFIX = "Fn::"

# Maximum length of a string before switching to angle-bracket-style representation
STR_MAX_LENGTH_QUOTED = config.max_col_width
# Maximum number of newlines a string can have before switching to pipe-style representation
STR_MAX_LINES_QUOTED = 10


class Dumper(CfnYamlDumper):
    """
    The standard dumper
    """


class CleanDumper(CleanCfnYamlDumper):
    """
    Cleans up strings
    """


class LongDumper(CfnYamlDumper):
    """
    Preserves long-form function syntax
    """


class LongCleanDumper(CleanCfnYamlDumper):
    """
    Preserves long-form function syntax
    """


def literal_unicode_representer(dumper, value):
    return dumper.represent_scalar(TAG_STR, value, style='|')


def string_representer(dumper, value):
    if sum(1 for nl in value if nl in ('\n', '\r')) >= STR_MAX_LINES_QUOTED:
        return dumper.represent_scalar(TAG_STR, value, style="|")

    if len(value) >= STR_MAX_LENGTH_QUOTED and '\n' not in value:
        return dumper.represent_scalar(TAG_STR, value, style=">")

    if value.startswith("0"):
        return dumper.represent_scalar(TAG_STR, value, style="'")

    return dumper.represent_scalar(TAG_STR, value)


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

    value = ODict(value.items())

    if len(value.keys()) == 1:
        key = list(value.keys())[0]

        if key in CONVERTED_SUFFIXES:
            return fn_representer(dumper, key, value[key])

        if key.startswith(FN_PREFIX):
            return fn_representer(dumper, key[4:], value[key])

    return dumper.represent_mapping(TAG_MAP, value, flow_style=False)


# Customise our dumpers
Dumper.add_representer(ODict, map_representer)
Dumper.add_representer(six.text_type, string_representer)
Dumper.add_representer(LiteralString, literal_unicode_representer)
CleanDumper.add_representer(LiteralString, literal_unicode_representer)
CleanDumper.add_representer(ODict, map_representer)


def get_dumper(clean_up=False, long_form=False):
    if clean_up:
        if long_form:
            return LongCleanDumper

        return CleanDumper

    if long_form:
        return LongDumper

    return Dumper
