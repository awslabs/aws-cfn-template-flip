"""
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from .json_encoder import DateTimeAwareJsonEncoder
from .odict import ODict
from .yaml_dumper import CfnYamlDumper
from .yaml_loader import CfnYamlLoader
import json
import yaml


def load_json(source):
    return json.loads(source, object_pairs_hook=ODict)


def dump_json(source):
    return json.dumps(source, indent=4, cls=DateTimeAwareJsonEncoder,
                      separators=(',', ': '), ensure_ascii=False)


def load_yaml(source):
    return yaml.load(source, Loader=CfnYamlLoader)


def dump_yaml(source):
    return yaml.dump(source, Dumper=CfnYamlDumper, default_flow_style=False, allow_unicode=True, width=120)
