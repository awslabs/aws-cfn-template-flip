"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_tools import dump_json, load_json, load_yaml
from cfn_tools.odict import ODict
import cfn_flip
import pytest
import yaml


@pytest.fixture
def input_json():
    with open("examples/test.json", "r") as f:
        return f.read().strip()


@pytest.fixture
def input_yaml():
    with open("examples/test.yaml", "r") as f:
        return f.read().strip()


@pytest.fixture
def clean_json():
    with open("examples/clean.json", "r") as f:
        return f.read().strip()


@pytest.fixture
def clean_yaml():
    with open("examples/clean.yaml", "r") as f:
        return f.read().strip()


@pytest.fixture
def parsed_json():
    return load_json(input_json())


@pytest.fixture
def parsed_yaml():
    return load_yaml(input_yaml())


@pytest.fixture
def parsed_clean_json():
    return load_json(clean_json())


@pytest.fixture
def parsed_clean_yaml():
    return load_yaml(clean_yaml())


@pytest.fixture
def bad_data():
    return "<!DOCTYPE html>\n\n<html>\n\tThis isn't right!\n</html>"


@pytest.fixture
def fail_message():
    return "Could not determine the input format"


def test_to_json_with_yaml(input_yaml, parsed_json):
    """
    Test that to_json performs correctly
    """

    actual = cfn_flip.to_json(input_yaml)
    assert load_json(actual) == parsed_json


def test_to_json_with_json(input_json, parsed_json):
    """
    Test that to_json still works when passed json
    (All json is valid yaml)
    """

    actual = cfn_flip.to_json(input_json)

    assert load_json(actual) == parsed_json


def test_to_yaml_with_json(input_json, parsed_yaml):
    """
    Test that to_yaml performs correctly
    """

    actual = cfn_flip.to_yaml(input_json)

    # The result should not parse as json
    with pytest.raises(ValueError):
        load_json(actual)

    parsed_actual = load_yaml(actual)

    assert parsed_actual == parsed_yaml


def test_to_yaml_with_yaml(input_yaml):
    """
    Test that to_yaml fails with a ValueError when passed yaml
    Yaml is not valid json
    """

    with pytest.raises(Exception, message="Invalid JSON"):
        cfn_flip.to_yaml(input_yaml)


def test_flip_to_json(input_yaml, input_json, parsed_json):
    """
    Test that flip performs correctly transforming from yaml to json
    """

    actual = cfn_flip.flip(input_yaml)

    assert load_json(actual) == parsed_json


def test_flip_to_yaml(input_json, input_yaml, parsed_yaml):
    """
    Test that flip performs correctly transforming from json to yaml
    """

    actual = cfn_flip.flip(input_json)
    assert actual == input_yaml + "\n"

    # The result should not parse as json
    with pytest.raises(ValueError):
        load_json(actual)

    parsed_actual = load_yaml(actual)
    assert parsed_actual == parsed_yaml


def test_flip_to_clean_json(input_yaml, clean_json, parsed_clean_json):
    """
    Test that flip performs correctly transforming from yaml to json
    and the `clean_up` flag is active
    """

    actual = cfn_flip.flip(input_yaml, clean_up=True)

    assert load_json(actual) == parsed_clean_json


def test_flip_to_clean_yaml(input_json, clean_yaml, parsed_clean_yaml):
    """
    Test that flip performs correctly transforming from json to yaml
    and the `clean_up` flag is active
    """

    actual = cfn_flip.flip(input_json, clean_up=True)
    assert actual == clean_yaml + "\n"

    # The result should not parse as json
    with pytest.raises(ValueError):
        load_json(actual)

    parsed_actual = load_yaml(actual)
    assert parsed_actual == parsed_clean_yaml


def test_flip_with_bad_data(fail_message, bad_data):
    """
    Test that flip fails with an error message when passed bad data
    """

    with pytest.raises(Exception, message=fail_message):
        cfn_flip.flip(bad_data)


def test_flip_to_json_with_datetimes():
    """
    Test that the json encoder correctly handles dates and datetimes
    """

    tricky_data = """
    a date: 2017-03-02
    a datetime: 2017-03-02 19:52:00
    """

    actual = cfn_flip.to_json(tricky_data)

    parsed_actual = load_json(actual)

    assert parsed_actual == {
        "a date": "2017-03-02",
        "a datetime": "2017-03-02T19:52:00",
    }


def test_flip_to_yaml_with_clean_getatt():
    """
    The clean flag should convert Fn::GetAtt to its short form
    """

    data = """
    {
        "Fn::GetAtt": ["Left", "Right"]
    }
    """

    expected = "!GetAtt 'Left.Right'\n"

    assert cfn_flip.to_yaml(data, clean_up=False) == expected
    assert cfn_flip.to_yaml(data, clean_up=True) == expected


def test_flip_to_yaml_with_multi_level_getatt():
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

    assert cfn_flip.to_yaml(data) == expected


def test_flip_to_yaml_with_dotted_getatt():
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

    assert cfn_flip.to_yaml(data) == expected


def test_flip_to_json_with_multi_level_getatt():
    """
    Test that we correctly convert multi-level Fn::GetAtt
    from YAML to JSON format
    """

    data = "!GetAtt 'First.Second.Third'\n"

    expected = {
        "Fn::GetAtt": ["First", "Second.Third"]
    }

    actual = cfn_flip.to_json(data, clean_up=True)

    assert load_json(actual) == expected


def test_getatt_from_yaml():
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
    assert load_json(actual) == expected

    # With clean
    actual = cfn_flip.to_json(source, clean_up=True)
    assert load_json(actual) == expected


def test_flip_to_json_with_condition():
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
    assert load_json(actual) == expected


def test_flip_to_yaml_with_newlines():
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

    assert cfn_flip.to_yaml(source) == expected


def test_clean_flip_to_yaml_with_newlines():
    """
    Test that strings containing newlines use blockquotes when using "clean"
    """

    source = dump_json(ODict((
        ("outer", ODict((
            ("inner", "#!/bin/bash\nyum -y update\nyum install python"),
            ("subbed", ODict((
                ("Fn::Sub", "The cake\nis\n${CakeType}"),
            ))),
        ))),
    )))

    expected = """outer:
  inner: |-
    #!/bin/bash
    yum -y update
    yum install python
  subbed: !Sub |-
    The cake
    is
    ${CakeType}
"""

    assert cfn_flip.to_yaml(source, clean_up=True) == expected


def test_flip_with_json_output(input_yaml, parsed_json):
    """
    We should be able to specify that the output is JSON
    """

    actual = cfn_flip.flip(input_yaml, out_format="json")

    assert load_json(actual) == parsed_json


def test_flip_with_yaml_output(input_json, parsed_yaml):
    """
    We should be able to specify that the output is YAML
    """

    actual = cfn_flip.flip(input_json, out_format="yaml")

    parsed_actual = load_yaml(actual)

    assert parsed_actual == parsed_yaml


def test_no_flip_with_json(input_json, parsed_json):
    """
    We should be able to submit JSON and get JSON back
    """

    actual = cfn_flip.flip(input_json, no_flip=True)

    assert load_json(actual) == parsed_json


def test_no_flip_with_yaml(input_yaml, parsed_yaml):
    """
    We should be able to submit YAML and get YAML back
    """

    actual = cfn_flip.flip(input_yaml, no_flip=True)

    parsed_actual = load_yaml(actual)

    assert parsed_actual == parsed_yaml


def test_no_flip_with_explicit_json(input_json, parsed_json):
    """
    We should be able to submit JSON and get JSON back
    and specify the output format explicity
    """

    actual = cfn_flip.flip(input_json, out_format="json", no_flip=True)

    assert load_json(actual) == parsed_json


def test_no_flip_with_explicit_yaml(input_yaml, parsed_yaml):
    """
    We should be able to submit YAML and get YAML back
    and specify the output format explicity
    """

    actual = cfn_flip.flip(input_yaml, out_format="yaml", no_flip=True)

    parsed_actual = load_yaml(actual)

    assert parsed_actual == parsed_yaml


def test_explicit_json_rejects_yaml(input_yaml):
    """
    Given an output format of YAML
    The input format should be assumed to be JSON
    and YAML input should be rejected
    """

    with pytest.raises(Exception, message="Invalid JSON"):
        cfn_flip.flip(input_yaml, out_format="yaml")


def test_explicit_yaml_rejects_bad_yaml(bad_data):
    """
    Given an output format of YAML
    The input format should be assumed to be JSON
    and YAML input should be rejected
    """

    with pytest.raises(Exception, message="Invalid YAML"):
        cfn_flip.flip(bad_data, out_format="json")


def test_flip_to_yaml_with_longhand_functions(input_json, parsed_json):
    """
    When converting to yaml, sometimes we'll want to keep the long form
    """

    actual1 = cfn_flip.flip(input_json, long_form=True)
    actual2 = cfn_flip.to_yaml(input_json, long_form=True)

    # No custom loader as there should be no custom tags
    parsed_actual1 = yaml.load(actual1)
    parsed_actual2 = yaml.load(actual2)

    # We use the parsed JSON as it contains long form function calls
    assert parsed_actual1 == parsed_json
    assert parsed_actual2 == parsed_json


def test_unconverted_types():
    """
    When converting to yaml, we need to make sure all short-form types are tagged
    """

    fns = {
        "Fn::GetAtt": "!GetAtt",
        "Fn::Sub": "!Sub",
        "Ref": "!Ref",
        "Condition": "!Condition",
    }

    for fn, tag in fns.items():
        value = dump_json({
            fn: "something"
        })

        expected = "{} 'something'\n".format(tag)

        assert cfn_flip.to_yaml(value) == expected


def test_get_dumper():
    """
    When invoking get_dumper use clean_up & long_form
    :return: LongCleanDumper
    """
    resp = cfn_flip.get_dumper(clean_up=True, long_form=True)
    assert resp == cfn_flip.yaml_dumper.LongCleanDumper
