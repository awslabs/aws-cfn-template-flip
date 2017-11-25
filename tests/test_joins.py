# Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file.
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cfn_flip


def test_basic_case():
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

    assert expected == actual


def test_ref():
    """
    Refs should be replaced by ${value}
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", {
                "Ref": "Cake"
            }, "is", "a", "lie"],
        ],
    }

    expected = {
        "Fn::Sub": "The ${Cake} is a lie",
    }

    actual = cfn_flip.clean(source)

    assert expected == actual


def test_get_att():
    """
    Intrinsics should be replaced by parameters to Sub
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", {
                "Fn::GetAtt": ["Cake", "Hole"]
            }, "is", "a", "lie"],
        ],
    }

    expected = {
        "Fn::Sub": "The ${Cake.Hole} is a lie",
    }

    actual = cfn_flip.clean(source)

    assert expected == actual


def test_multi_level_get_att():
    """
    Intrinsics should be replaced by parameters to Sub
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", {
                "Fn::GetAtt": ["First", "Second", "Third"]
            }, "is", "a", "lie"],
        ],
    }

    expected = {
        "Fn::Sub": "The ${First.Second.Third} is a lie",
    }

    actual = cfn_flip.clean(source)

    assert expected == actual


def test_others():
    """
    GetAtt should be replaced by ${Thing.Property}
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", {
                "Fn::Base64": "Notreallybase64"
            }, "is", "a", "lie"],
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

    assert expected == actual


def test_in_array():
    """
    Converting Join to Sub should still work when the join is part of a larger array
    """

    source = {
        "things": [
            "Just a string",
            {
                "Fn::Join": [
                    " ",
                    ["The", {
                        "Fn::Base64": "Notreallybase64"
                    }, "is", "a", "lie"],
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

    assert expected == actual


def test_literals():
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

    assert expected == actual


def test_nested_join():
    """
    Test that a join of joins works correctly
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", "cake", {
                "Fn::Join": [
                    " ",
                    ["is", "a"],
                ],
            }, "lie"],
        ],
    }

    expected = "The cake is a lie"

    actual = cfn_flip.clean(source)

    assert expected == actual


def test_deep_nested_join():
    """
    Test that a join works correctly when inside an intrinsic, inside a join
    """

    source = {
        "Fn::Join": [
            " ",
            ["The", "cake", "is", "a", {
                "Fn::ImportValue": {
                    "Fn::Join": [
                        "-",
                        [{
                            "Ref": "lieStack"
                        }, "lieValue"],
                    ]
                },
            }],
        ],
    }

    expected = {
        "Fn::Sub": [
            "The cake is a ${Param1}",
            {
                "Param1": {
                    "Fn::ImportValue": {
                        "Fn::Sub": "${lieStack}-lieValue",
                    },
                },
            },
        ]
    }

    actual = cfn_flip.clean(source)

    assert expected == actual
