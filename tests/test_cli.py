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
from click.testing import CliRunner
from cfn_flip import main


def test_cli_with_version():
    runner = CliRunner()
    result = runner.invoke(main.main, ['--version'])
    assert not result.exception
    assert result.exit_code == 0
    assert 'AWS Cloudformation Template Flip, Version ' in result.output


def test_cli_with_input_json(tmpdir):
    # file_standard is the reference document that we expect to generate
    file_standard = open('examples/test.yaml', 'r').read()
    # file_output is the temporary file that we will generate to compare with file_standard
    file_output = tmpdir.join('unit_test.yaml')
    runner = CliRunner()
    result = runner.invoke(main.main, ['--yaml', 'examples/test.json', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_cli_with_input_yaml(tmpdir):
    # file_standard is the reference document that we expect to generate
    file_standard = open('examples/test.json', 'r').read()
    # file_output is the temporary file that we will generate to compare with file_standard
    file_output = tmpdir.join('unit_test.json')
    runner = CliRunner()
    result = runner.invoke(main.main, ['--json', 'examples/test.yaml', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    file_result = file_output.read()
    assert file_result == file_standard


def test_cli_with_invalid_input():
    runner = CliRunner()
    result = runner.invoke(main.main, ['--yaml', 'examples/invalid'])
    assert result.exception
    assert result.exit_code == 1
    assert result.output.startswith("Error: Expecting property name")


def test_format_detection_with_invalid_input():
    runner = CliRunner()
    result = runner.invoke(main.main, ['examples/invalid'])
    assert result.exception
    assert result.exit_code == 1
    assert result.output.startswith("Error: Expecting property name")


def test_specified_json_input_with_guessed_output(tmpdir):
    file_standard = open('examples/test.yaml', 'r').read()
    file_output = tmpdir.join('unit_test.yaml')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-i', 'json', 'examples/test.json', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_specified_yaml_input_with_guessed_output(tmpdir):
    file_standard = open('examples/test.json', 'r').read()
    file_output = tmpdir.join('unit_test.yaml')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-i', 'yaml', 'examples/test.yaml', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_specified_json_input_with_no_flip(tmpdir):
    file_standard = open('examples/test.json', 'r').read()
    file_output = tmpdir.join('unit_test.json')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-i', 'json', '-n', 'examples/test.json', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_specified_yaml_input_with_no_flip(tmpdir):
    file_standard = open('examples/test.yaml', 'r').read()
    file_output = tmpdir.join('unit_test.yaml')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-i', 'yaml', '-n', 'examples/test.yaml', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_no_flip_is_overriden_by_specified_json_output(tmpdir):
    file_standard = open('examples/test.json', 'r').read()
    file_output = tmpdir.join('unit_test.json')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-o', 'json', '-n', 'examples/test.yaml', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_no_flip_is_overriden_by_specified_yaml_output(tmpdir):
    file_standard = open('examples/test.yaml', 'r').read()
    file_output = tmpdir.join('unit_test.yaml')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-o', 'yaml', '-n', 'examples/test.json', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_specified_json_output_overrides_j_flag(tmpdir):
    file_standard = open('examples/test.json', 'r').read()
    file_output = tmpdir.join('unit_test.json')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-o', 'json', '-y', 'examples/test.json', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard


def test_specified_yaml_output_overrides_j_flag(tmpdir):
    file_standard = open('examples/test.yaml', 'r').read()
    file_output = tmpdir.join('unit_test.yaml')

    runner = CliRunner()
    result = runner.invoke(main.main, ['-o', 'yaml', '-j', 'examples/test.yaml', file_output.strpath])
    assert not result.exception
    assert result.exit_code == 0
    assert file_output.read() == file_standard
