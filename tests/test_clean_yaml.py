from pytest import param
import pytest
import cfn_flip
import json

testdata = [
    param(
        {
            "Fn::Join": [
                " ",
                ["The", "cake", "is", "a", "lie"],
            ],
        },
        "The cake is a lie\n...\n",
        id='Plain Join',
    ),
    param(
        {
            "Ref": "Cake"
        },
        "!Ref 'Cake'\n",
        id='Plain Ref',
    ),
    param(
        {
            "Fn::Join": [
                " ",
                ["The", {
                    "Ref": "Cake"
                }, "is", "a", "lie"],
            ],
        },
        "!Sub 'The ${Cake} is a lie'\n",
        id='Ref in Join',
    ),
    param(
        {
            "Fn::Join": [
                " ",
                [
                    "The",
                    "Cake",
                    "is",
                    "a",
                    {
                        "Fn::ImportValue": "LieStack-lieValue",
                    },
                ],
            ],
        },
        "!Sub ['The Cake is a ${Param1}', {Param1: !ImportValue 'LieStack-lieValue'}]\n",
        id='ImportValue in Join',
    ),
    param(
        {
            "Fn::Join": [
                " ",
                [
                    "The",
                    "Cake",
                    "is",
                    "a",
                    {
                        "Fn::ImportValue": {
                            "Fn::Join": [
                                "-",
                                [
                                    "LieStack",
                                    "lieValue",
                                ],
                            ],
                        }
                    },
                ],
            ],
        },
        "!Sub ['The Cake is a ${Param1}', {Param1: !ImportValue 'LieStack-lieValue'}]\n",
        id='Join in ImportValue in Join',
    ),
    param(
        {
            "Fn::Join": [
                " ",
                [
                    "The",
                    "Cake",
                    "is",
                    "a",
                    {
                        "Fn::ImportValue": {
                            "Fn::Join": [
                                "-",
                                [
                                    {
                                        "Ref": "lieStack",
                                    },
                                    "lieValue",
                                ],
                            ],
                        }
                    },
                ],
            ],
        },
        "!Sub ['The Cake is a ${Param1}', {Param1: !ImportValue {'Fn::Sub': '${lieStack}-lieValue'}}]\n",
        id='Ref in Join in ImportValue in Join',
    ),
]


@pytest.mark.parametrize('source, expected', testdata)
def test_nested(source, expected):

    actual = cfn_flip.to_yaml(json.dumps(source), clean_up=True)
    assert actual == expected
