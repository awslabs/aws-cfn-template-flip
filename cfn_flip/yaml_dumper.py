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

from cfn_clean.yaml_dumper import CleanCfnYamlDumper
from cfn_tools.odict import ODict
from cfn_tools.yaml_dumper import CfnYamlDumper
import six

TAG_STR = "tag:yaml.org,2002:str"
TAG_MAP = "tag:yaml.org,2002:map"
CONVERTED_SUFFIXES = ["Ref", "Condition"]

FN_PREFIX = "Fn::"


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


def string_representer(dumper, value):
    if value.startswith("0"):
        return dumper.represent_scalar(TAG_STR, value, style="'")

    return dumper.represent_scalar(TAG_STR, value)


def join_compactor(joiner, values):
    def ref_packer(value):
        tag = None
        if isinstance(value, ODict):
            tag, value = list(value.items())[0]

        if tag is None:
            return value
        if tag in ('!Sub', 'Sub'):
            return value
        if tag in ('Fn::GetAtt', 'GetAtt') and isinstance(value, list):
            return '${%s}' %  '.'.join(value)
        if tag in ('Fn::Ref', 'Ref', 'Fn::GetAtt', 'GetAtt'):
            return '${%s}' % value
        else:
            raise ValueError("Item in Fn::Join could not be compacted into a !Sub. Failed item: {}".format(value))

    return '!Sub', joiner.join([ref_packer(v) for v in values])


def fn_representer(dumper, fn_name, value):
    tag = "!{}".format(fn_name)

    if tag == "!GetAtt" and isinstance(value, list):
        value = ".".join(value)

    if tag == "!Join":
        try:
            tag, value = join_compactor(*value)
        except ValueError:
            pass

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
CleanDumper.add_representer(ODict, map_representer)


def get_dumper(clean_up=False, long_form=False):
    if clean_up:
        if long_form:
            return LongCleanDumper

        return CleanDumper

    if long_form:
        return LongDumper

    return Dumper
