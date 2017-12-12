"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_tools import load_json, load_yaml, dump_json, dump_yaml
from cfn_tools.odict import ODict
import datetime
import pytest


def test_load_json():
    """
    Should map to an ordered dict
    """

    source = """
    {
        "z": "first",
        "m": "middle",
        "a": "last"
    }
    """

    actual = load_json(source)

    assert type(actual) == ODict
    assert list(actual.keys()) == ["z", "m", "a"]
    assert actual["z"] == "first"
    assert actual["m"] == "middle"
    assert actual["a"] == "last"


def test_load_yaml():
    """
    Should map to an ordered dict
    """

    source = """z: first
m: !Sub
  - The cake is a ${CakeType}
  - CakeType: lie
a: !Ref last
"""

    actual = load_yaml(source)

    assert type(actual) == ODict
    assert list(actual.keys()) == ["z", "m", "a"]
    assert actual["z"] == "first"
    assert actual["m"] == {
        "Fn::Sub": [
            "The cake is a ${CakeType}",
            {
                "CakeType": "lie",
            },
        ],
    }
    assert actual["a"] == {"Ref": "last"}


def test_dump_json():
    """
    JSON dumping just needs to know about datetimes,
    provide a nice indent, and preserve order
    """

    source = ODict((
        ("z", datetime.time(3, 45)),
        ("m", datetime.date(2012, 5, 2)),
        ("a", datetime.datetime(2012, 5, 2, 3, 45)),
    ))

    actual = dump_json(source)

    assert load_json(actual) == {
        "z": "03:45:00",
        "m": "2012-05-02",
        "a": "2012-05-02T03:45:00",
    }

    with pytest.raises(TypeError, message="complex is not JSON serializable"):
        dump_json({
            "c": 1 + 1j,
        })


def test_dump_yaml():
    """
    YAML dumping needs to use quoted style for strings with newlines,
    use a standard indenting style, and preserve order
    """

    source = ODict((
        ("z", "short string",),
        ("m", {"Ref": "embedded string"},),
        ("a", "A\nmulti-line\nstring",),
    ))

    actual = dump_yaml(source)

    assert actual == """z: short string
m:
  Ref: embedded string
a: "A\\nmulti-line\\nstring"
"""
