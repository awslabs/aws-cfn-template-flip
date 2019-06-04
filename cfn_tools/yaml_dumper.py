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

import re
import six
import yaml
from yaml.emitter import Emitter, ScalarAnalysis

from .literal import LiteralString
from .odict import ODict

TAG_MAP = "tag:yaml.org,2002:map"
TAG_STRING = "tag:yaml.org,2002:str"
AWS_ACCOUNT_ID = r"^0[0-9]+$"


class CfnEmitter(Emitter):
    def analyze_scalar(self, scalar):
        # We have Json payloads that we want to show as literal
        # This way we can skip the checks that analize_scalar do in the string when you have
        # leading_space or leading_break
        if not scalar or isinstance(scalar, LiteralString):
            return ScalarAnalysis(scalar=scalar, empty=True, multiline=False,
                                  allow_flow_plain=False, allow_block_plain=True,
                                  allow_single_quoted=True, allow_double_quoted=True,
                                  allow_block=True)
        return super(CfnEmitter, self).analyze_scalar(scalar)


class CfnYamlDumper(yaml.Dumper, CfnEmitter):
    """
    Indent block sequences from parent using more common style
    ("  - entry"  vs "- entry").
    Causes fewer problems with validation and tools.
    """

    def increase_indent(self, flow=False, indentless=False):
        return super(CfnYamlDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
        if re.match(AWS_ACCOUNT_ID, value):
            style = "\'"

        if isinstance(value, six.text_type):
            if any(eol in value for eol in "\n\r") and style is None:
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


def literal_unicode_representer(dumper, value):
    return dumper.represent_scalar(TAG_STRING, value, style='|')


# Customise the dumper
CfnYamlDumper.add_representer(ODict, map_representer)
CfnYamlDumper.add_representer(LiteralString, literal_unicode_representer)
CfnYamlDumper.add_representer(six.text_type, string_representer)
