"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import cfn_flip
import json
import unittest
import yaml


class ReplaceJoinTestCase(unittest.TestCase):
    """
    Check that joins get replaced with Subs
    """

    def test_basic_case(self):
        """
        As simple as it gets
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", "cake", "is", "a", "lie"],
            ],
        }

        expected = "The cake is a lie"

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_ref(self):
        """
        Refs should be replaced by ${value}
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", {"Ref": "Cake"}, "is", "a", "lie"],
            ],
        }

        expected = {
            "Fn::Sub": "The ${Cake} is a lie",
        }

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_get_att(self):
        """
        Base64 etc should be replaced by parameters to Sub
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", {"Fn::GetAtt": ["Cake", "Hole"]}, "is", "a", "lie"],
            ],
        }

        expected = {
            "Fn::Sub": "The ${Cake.Hole} is a lie",
        }

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_multi_level_get_att(self):
        """
        Base64 etc should be replaced by parameters to Sub
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", {"Fn::GetAtt": ["First", "Second", "Third"]}, "is", "a", "lie"],
            ],
        }

        expected = {
            "Fn::Sub": "The ${First.Second.Third} is a lie",
        }

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_others(self):
        """
        GetAtt should be replaced by ${Thing.Property}
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", {"Fn::Base64": "Notreallybase64"}, "is", "a", "lie"],
            ],
        }

        expected = {
            "Fn::Sub": [
                "The ${Param1} is a lie",
                {
                    "Param1": {
                        "Fn::Base64": "Notreallybase64",
                    },
                },
            ],
        }

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_in_array(self):
        """
        Converting Join to Sub should still work when the join is part of a larger array
        """

        source = {
            "things": [
                "Just a string",
                {
                    "Fn::Join": [
                        " ",
                        ["The", {"Fn::Base64": "Notreallybase64"}, "is", "a", "lie"],
                    ],
                },
                {
                    "Another": "thing",
                },
            ],
        }

        expected = {
            "things": [
                "Just a string",
                {
                    "Fn::Sub": [
                        "The ${Param1} is a lie",
                        {
                            "Param1": {
                                "Fn::Base64": "Notreallybase64",
                            },
                        },
                    ],
                },
                {
                    "Another": "thing",
                },
            ],
        }

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)

    def test_literals(self):
        """
        Test that existing ${var} in source is respected
        """

        source = {
            "Fn::Join": [
                " ",
                ["The", "${cake}", "is", "a", "lie"],
            ],
        }

        expected = "The ${!cake} is a lie"

        actual = cfn_flip.clean(source)

        self.assertEqual(expected, actual)
