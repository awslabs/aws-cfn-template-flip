"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_tools import load_json, load_yaml, dump_json, dump_yaml, CfnYamlDumper
from cfn_tools.odict import ODict, OdictItems
from cfn_tools.yaml_loader import multi_constructor, construct_getatt
from yaml import ScalarNode
import datetime
import pytest
import six


class MockNode(object):
    def __init__(self, value=None):
        self.value = value


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


def test_odict_items_sort():
    """
    Simple test to validate sort method.
    TODO: implement sort method
    :return: None
    """
    items = ['B', 'A', 'C']
    odict = OdictItems(items)
    assert not odict.sort()


def test_odict_fail_with_dict():
    """
    Raise exception if we pass dict when initializing the class with dict
    :return: Exception
    """
    items = {'key1': 'value1'}
    with pytest.raises(Exception) as e:
        ODict(items)
    assert 'ODict does not allow construction from a dict' in str(e)


def test_represent_scalar():
    """
    When invoking represent_scalar apply style if value has \n
    :return: ScalarNode
    """
    source = """z: first
    m: !Sub
      - The cake is a ${CakeType}
      - CakeType: lie
    a: !Ref last
    """
    yaml_dumper = CfnYamlDumper(six.StringIO(source))
    resp = yaml_dumper.represent_scalar('Key', 'value\n')
    print(resp)
    assert isinstance(resp, ScalarNode)


def test_multi_constructor_with_invalid_node_type():
    """
    When invoking multi_constructor with invalid node type must raise Exception
    :return:
    """
    with pytest.raises(Exception) as e:
        multi_constructor(None, None, None)
    assert 'Bad tag: !Fn::None' in str(e)


def test_construct_getattr_with_invalid_node_type():
    """
    When invoking multi_constructor with invalid node type must raise Exception
    :return:
    """
    node = MockNode()
    with pytest.raises(ValueError) as e:
        construct_getatt(node)
    assert 'Unexpected node type:' in str(e)


def test_construct_getattr_with_list():
    """
    When invoking multi_constructor with invalid node type must raise Exception
    :return:
    """
    node = MockNode()
    node.value = [MockNode('A'), MockNode('B'), MockNode('C')]
    resp = construct_getatt(node)
    assert resp == ['A', 'B', 'C']
