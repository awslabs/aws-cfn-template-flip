from cfn_tools import load_json, load_yaml, dump_json, dump_yaml

from cfn_tools import load_json, load_yaml, dump_json, dump_yaml
from cfn_tools.odict import ODict
import datetime
import json
import pytest
import yaml

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
