"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import cfn_flip
import json
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

        self.parsed_json = json.loads(self.input_json)
        self.parsed_yaml = yaml.load(self.input_yaml)

        self.bad_data = "<!DOCTYPE html>\n\n<html>\n\tThis isn't right!\n</html>"

        self.fail_message = "Could not determine the input format. Perhaps it's malformed?"

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

        parsed_actual = yaml.load(actual)

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

        parsed_actual = yaml.load(actual)

        self.assertDictEqual(parsed_actual, self.parsed_yaml)

    def test_flip_with_bad_data(self):
        """
        Test that flip fails with an error message when passed bad data
        """

        with self.assertRaisesRegexp(Exception, self.fail_message):
            cfn_flip.flip(self.bad_data)

if __name__ == "__main__":
    unittest.main()
