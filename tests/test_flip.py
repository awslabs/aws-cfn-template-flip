"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_flip.custom_yaml import CustomLoader
import cfn_flip
import json
import six
import unittest
import yaml

class CfnFlipTestCase(unittest.TestCase):
    def setUp(self):
        """
        Load in the examples and pre-parse the expected results
        """

        with open("examples/test.json", "r") as f:
            self.input_json = f.read()

        with open("examples/test.yaml", "r") as f:
            self.input_yaml = f.read()

        with open("examples/clean.json", "r") as f:
            self.clean_json = f.read()

        with open("examples/clean.yaml", "r") as f:
            self.clean_yaml = f.read()

        self.parsed_json = json.loads(self.input_json)
        self.parsed_yaml = yaml.load(self.input_yaml, Loader=CustomLoader)

        self.parsed_clean_json = json.loads(self.clean_json)
        self.parsed_clean_yaml = yaml.load(self.clean_yaml, Loader=CustomLoader)

        self.bad_data = "<!DOCTYPE html>\n\n<html>\n\tThis isn't right!\n</html>"

        self.fail_message = "Could not determine the input format"

    def test_to_json_with_yaml(self):
        """
        Test that to_json performs correctly
        """

        actual = cfn_flip.to_json(self.input_yaml)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_to_json_with_json(self):
        """
        Test that to_json still works when passed json
        (All json is valid yaml)
        """

        actual = cfn_flip.to_json(self.input_json)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_to_yaml_with_json(self):
        """
        Test that to_yaml performs correctly
        """

        actual = cfn_flip.to_yaml(self.input_json)

        # The result should not parse as json
        with self.assertRaises(ValueError):
            json.loads(actual)

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_to_yaml_with_yaml(self):
        """
        Test that to_yaml fails with a ValueError when passed yaml
        Yaml is not valid json
        """

        with six.assertRaisesRegex(self, Exception, "Invalid JSON"):
            actual = cfn_flip.to_yaml(self.input_yaml)

    def test_flip_to_json(self):
        """
        Test that flip performs correctly transforming from yaml to json
        """

        actual = cfn_flip.flip(self.input_yaml)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_flip_to_yaml(self):
        """
        Test that flip performs correctly transforming from json to yaml
        """

        actual = cfn_flip.flip(self.input_json)

        # The result should not parse as json
        with self.assertRaises(ValueError):
            json.loads(actual)

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_flip_to_clean_json(self):
        """
        Test that flip performs correctly transforming from yaml to json
        and the `clean_up` flag is active
        """

        actual = cfn_flip.flip(self.input_yaml, clean_up=True)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_clean_json)

    def test_flip_to_clean_yaml(self):
        """
        Test that flip performs correctly transforming from json to yaml
        and the `clean_up` flag is active
        """

        actual = cfn_flip.flip(self.input_json, clean_up=True)

        # The result should not parse as json
        with self.assertRaises(ValueError):
            json.loads(actual)

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_clean_yaml)

    def test_flip_with_bad_data(self):
        """
        Test that flip fails with an error message when passed bad data
        """

        with six.assertRaisesRegex(self, Exception, self.fail_message):
            cfn_flip.flip(self.bad_data)

    def test_flip_to_json_with_datetimes(self):
        """
        Test that the json encoder correctly handles dates and datetimes
        """

        from datetime import date, datetime, time

        tricky_data = """
        a date: 2017-03-02
        a datetime: 2017-03-02 19:52:00
        """

        actual = cfn_flip.to_json(tricky_data)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, {
            "a date": "2017-03-02",
            "a datetime": "2017-03-02T19:52:00",
        })

    def test_flip_to_yaml_with_clean_getatt(self):
        """
        The clean flag should convert Fn::GetAtt to its short form
        """

        data = """
        {
            "Fn::GetAtt": ["Left", "Right"]
        }
        """

        expected = "!GetAtt 'Left.Right'\n"

        self.assertEqual(cfn_flip.to_yaml(data, clean_up=False), expected)
        self.assertEqual(cfn_flip.to_yaml(data, clean_up=True), expected)

    def test_flip_to_yaml_with_multi_level_getatt(self):
        """
        Test that we correctly convert multi-level Fn::GetAtt
        from JSON to YAML format
        """

        data = """
        {
            "Fn::GetAtt": ["First", "Second", "Third"]
        }
        """

        expected = "!GetAtt 'First.Second.Third'\n"

        self.assertEqual(cfn_flip.to_yaml(data), expected)

    def test_flip_to_yaml_with_dotted_getatt(self):
        """
        Even though documentation does not suggest Resource.Value is valid
        we should support it anyway as cloudformation allows it :)
        """

        data = """
        [
            {
                "Fn::GetAtt": "One.Two"
            },
            {
                "Fn::GetAtt": "Three.Four.Five"
            }
        ]
        """

        expected = "- !GetAtt 'One.Two'\n- !GetAtt 'Three.Four.Five'\n"

        self.assertEqual(cfn_flip.to_yaml(data), expected)

    def test_flip_to_json_with_multi_level_getatt(self):
        """
        Test that we correctly convert multi-level Fn::GetAtt
        from YAML to JSON format
        """

        data = "!GetAtt 'First.Second.Third'\n"

        expected = {
            "Fn::GetAtt": ["First", "Second", "Third"]
        }

        actual = cfn_flip.to_json(data, clean_up=True)
        self.assertEqual(expected, json.loads(actual))

    def test_getatt_from_yaml(self):
        """
        Test that we correctly convert the short form of GetAtt
        into the correct JSON format from YAML
        """

        source = """
        - !GetAtt foo.bar
        - Fn::GetAtt: [foo, bar]
        """

        expected = [
            {"Fn::GetAtt": ["foo", "bar"]},
            {"Fn::GetAtt": ["foo", "bar"]},
        ]

        # No clean
        actual = cfn_flip.to_json(source, clean_up=False)
        self.assertEqual(expected, json.loads(actual))

        # With clean
        actual = cfn_flip.to_json(source, clean_up=True)
        self.assertEqual(expected, json.loads(actual))

    def test_flip_to_json_with_condition(self):
        """
        Test that the Condition key is correctly converted
        """

        source = """
            MyAndCondition: !And
            - !Equals ["sg-mysggroup", !Ref "ASecurityGroup"]
            - !Condition SomeOtherCondition
        """

        expected = {
            "MyAndCondition": {
                "Fn::And": [
                    {"Fn::Equals": ["sg-mysggroup", {"Ref": "ASecurityGroup"}]},
                    {"Condition": "SomeOtherCondition"}
                ]
            }
        }

        actual = cfn_flip.to_json(source, clean_up=True)
        self.assertEqual(expected, json.loads(actual))

    def test_flip_to_yaml_with_newlines(self):
        """
        Test that strings containing newlines are quoted
        """

        source = r'["a", "b\n", "c\r\n", "d\r"]'

        expected = "".join([
            '- a\n',
            '- "b\\n"\n',
            '- "c\\r\\n"\n',
            '- "d\\r"\n',
        ])

        actual = cfn_flip.to_yaml(source)

        self.assertEqual(expected, actual)

    def test_flip_with_json_output(self):
        """
        We should be able to specify that the output is JSON
        """

        actual = cfn_flip.flip(self.input_yaml, out_format="json")

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_flip_with_yaml_output(self):
        """
        We should be able to specify that the output is YAML
        """

        actual = cfn_flip.flip(self.input_json, out_format="yaml")

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_no_flip_with_json(self):
        """
        We should be able to submit JSON and get JSON back
        """

        actual = cfn_flip.flip(self.input_json, no_flip=True)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_no_flip_with_yaml(self):
        """
        We should be able to submit YAML and get YAML back
        """

        actual = cfn_flip.flip(self.input_yaml, no_flip=True)

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_no_flip_with_explicit_json(self):
        """
        We should be able to submit JSON and get JSON back
        and specify the output format explicity
        """

        actual = cfn_flip.flip(self.input_json, out_format="json", no_flip=True)

        parsed_actual = json.loads(actual)

        self.assertDictEqual(parsed_actual, self.parsed_json)

    def test_no_flip_with_explicit_yaml(self):
        """
        We should be able to submit YAML and get YAML back
        and specify the output format explicity
        """

        actual = cfn_flip.flip(self.input_yaml, out_format="yaml", no_flip=True)

        parsed_actual = yaml.load(actual, Loader=CustomLoader)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_explicit_json_rejects_yaml(self):
        """
        Given an output format of YAML
        The input format should be assumed to be JSON
        and YAML input should be rejected
        """

        with six.assertRaisesRegex(self, Exception, "Invalid JSON"):
            cfn_flip.flip(self.input_yaml, out_format="yaml")

    def test_explicit_yaml_rejects_bad_yaml(self):
        """
        Given an output format of YAML
        The input format should be assumed to be JSON
        and YAML input should be rejected
        """

        with six.assertRaisesRegex(self, Exception, "Invalid YAML"):
            cfn_flip.flip(self.bad_data, out_format="json")
