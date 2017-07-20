"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import cfn_flip
import json
import unittest
from cfn_flip.custom_yaml import custom_yaml


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
        self.parsed_yaml = custom_yaml.load(self.input_yaml)

        self.parsed_clean_json = json.loads(self.clean_json)
        self.parsed_clean_yaml = custom_yaml.load(self.clean_yaml)

        self.bad_data = "<!DOCTYPE html>\n\n<html>\n\tThis isn't right!\n</html>"

        self.fail_message = "Could not determine the input format: .+"

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

        parsed_actual = custom_yaml.load(actual)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_to_yaml_with_yaml(self):
        """
        Test that to_yaml fails with a ValueError when passed yaml
        Yaml is not valid json
        """

        with self.assertRaises(ValueError):
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

        parsed_actual = custom_yaml.load(actual)

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

        parsed_actual = custom_yaml.load(actual)

        self.assertDictEqual(parsed_actual, self.parsed_clean_yaml)

    def test_flip_with_bad_data(self):
        """
        Test that flip fails with an error message when passed bad data
        """

        with self.assertRaisesRegexp(Exception, self.fail_message):
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

        self.assertEqual(cfn_flip.to_yaml(data, clean_up=True), expected)

    def test_getatt_from_yaml(self):
        """
        Test that we correctly convert the short form of GetAtt
        into the correct JSON format from YAML
        """

        source = """
        - !GetAtt foo.bar
        - !GetAtt [foo, bar]
        - Fn::GetAtt: [foo, bar]
        """

        expected = [
            {"Fn::GetAtt": ["foo", "bar"]},
            {"Fn::GetAtt": ["foo", "bar"]},
            {"Fn::GetAtt": ["foo", "bar"]},
        ]

        actual = cfn_flip.to_json(source, clean_up=True)
        print(actual)
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
