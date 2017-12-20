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
from cfn_clean import clean
from cfn_tools import load_json, load_yaml, dump_json
import yaml


def load(template):
    """
    Try to guess the input format
    """

    try:
        data = load_json(template)
        return data, "json"
    except ValueError:
        data = load_yaml(template)
        return data, "yaml"


def dump_yaml(data, clean_up=False, long_form=False):
    """
    Output some YAML
    """

    return yaml.dump(
        data,
        Dumper=get_dumper(clean_up, long_form),
        default_flow_style=False
    )


def to_json(template, clean_up=False):
    """
    Assume the input is YAML and convert to JSON
    """

    data = load_yaml(template)

    if clean_up:
        data = clean(data)

    return dump_json(data)


def to_yaml(template, clean_up=False, long_form=False):
    """
    Assume the input is JSON and convert to YAML
    """

    data = load_json(template)

    if clean_up:
        data = clean(data)

    return dump_yaml(data, clean_up, long_form)


def flip(template, out_format=None, clean_up=False, no_flip=False, long_form=False):
    """
    Figure out the input format and convert the data to the opposing output format
    """

    data = None
    in_format = None

    if no_flip:
        in_format = out_format
    elif out_format == "json":
        in_format = "yaml"
    elif out_format == "yaml":
        in_format = "json"

    if in_format == "json":
        data = load_json(template)
    elif in_format == "yaml":
        data = load_yaml(template)
    else:
        try:
            data, in_format = load(template)
        except Exception:
            raise Exception("Could not determine the input format")

    if no_flip:
        out_format = in_format
    elif in_format == "json":
        out_format = "yaml"
    else:
        out_format = "json"

    if clean_up:
        data = clean(data)

    if out_format == "json":
        return dump_json(data)

    return dump_yaml(data, clean_up, long_form)
