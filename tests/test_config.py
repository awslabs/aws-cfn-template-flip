# -*- coding: utf-8 -*-
#
# tests/cli.py
#
# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import pytest
from cfn_tools._config import config, apply_configs, _CONFIG_DEFAULTS, _ConfigArg, _Config


def test_config_rest():
    assert config.reset() is None


def test_config_rest_with_item():
    assert config.reset("max_col_width") is None


def test_config_with_env_var():
    os.environ["CFN_MAX_COL_WIDTH"] = "200"
    assert config.reset() is None
    del os.environ["CFN_MAX_COL_WIDTH"]


def test_config_get_item():
    assert config['max_col_width'] == 200


def test_invalid_config_set_attr():
    with pytest.raises(TypeError):
        config.invalid_entry = "200"


def test_config_apply_configs():
    @apply_configs
    def temp_my_func(max_col_width):
        return max_col_width
    assert temp_my_func() == 200


def test_config_apply_type_null():
    _CONFIG_DEFAULTS['test_nullable'] = _ConfigArg(dtype=bool, nullable=True, has_default=False)
    test_config = _Config()
    test_config.test_nullable = None
    assert test_config.test_nullable is None


def test_config_apply_type_null_error():
    _CONFIG_DEFAULTS['test_nullable'] = _ConfigArg(dtype=int, nullable=False, has_default=True, default="nil")
    with pytest.raises(ValueError):
        _ = _Config()
