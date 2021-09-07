"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from .yaml_dumper import get_dumper
from cfn_clean import clean, cfn_literal_parser
from cfn_tools import load_json, load_yaml, dump_json
from cfn_tools._config import config
import yaml


def load(template):
    """
    Try to guess the input format
    """

    try:
        data = load_json(template)
        return data, "json"
    except ValueError as e:
        try:
            data = load_yaml(template)
            return data, "yaml"
        except Exception:
            raise e


def dump_yaml(data, clean_up=False, long_form=False):
    """
    Output some YAML
    """

    return yaml.dump(
        data,
        Dumper=get_dumper(clean_up, long_form),
        default_flow_style=False,
        allow_unicode=True,
        width=config.max_col_width
    )


def to_json(template, clean_up=False):
    """
    Assume the input is YAML and convert to JSON
    """

    data, _ = load(template)

    if clean_up:
        data = clean(data)

    return dump_json(data)


def to_yaml(template, clean_up=False, long_form=False, literal=True):
    """
    Assume the input is JSON and convert to YAML
    """

    data, _ = load(template)

    if clean_up:
        data = clean(data)

    if literal:
        data = cfn_literal_parser(data)

    return dump_yaml(data, clean_up, long_form)


def flip(template, in_format=None, out_format=None, clean_up=False, no_flip=False, long_form=False):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    # Do we need to figure out the input format?
    if not in_format:
        # Load the template as JSON?
        if (out_format == "json" and no_flip) or (out_format == "yaml" and not no_flip):
            in_format = "json"
        elif (out_format == "yaml" and no_flip) or (out_format == "json" and not no_flip):
            in_format = "yaml"

    # Load the data
    if in_format == "json":
        data = load_json(template)
    elif in_format == "yaml":
        data = load_yaml(template)
    else:
        data, in_format = load(template)

    # Clean up?
    if clean_up:
        data = clean(data)

    # Figure out the output format
    if not out_format:
        if (in_format == "json" and no_flip) or (in_format == "yaml" and not no_flip):
            out_format = "json"
        else:
            out_format = "yaml"

    # Finished!
    if out_format == "json":
        return dump_json(data)

    return dump_yaml(data, clean_up, long_form)
