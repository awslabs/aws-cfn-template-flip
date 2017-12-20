"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_tools.odict import ODict
import pytest


def test_get_set():
    """
    It should at least work the same as a dict
    """

    case = ODict()

    case["one"] = 1
    case["two"] = 2

    assert len(case.keys()) == 2
    assert case["one"] == 1


def test_list_constructor():
    """
    We should be able to construct one from a tuple of pairs
    """

    case = ODict((
        ("one", 1),
        ("two", 2),
    ))

    assert len(case.keys()) == 2
    assert case["one"] == 1
    assert case["two"] == 2
    assert case["two"] == 2


def test_ordering():
    """
    Ordering should be left intact
    """

    case = ODict()

    case["z"] = 1
    case["a"] = 2

    assert list(case.keys()) == ["z", "a"]


def test_ordering_from_constructor():
    """
    Ordering should be left intact
    """

    case = ODict([
        ("z", 1),
        ("a", 2),
    ])

    assert list(case.keys()) == ["z", "a"]


def test_constructor_disallows_dict():
    """
    For the sake of python<3.6, don't accept dicts
    as ordering will be lost
    """

    with pytest.raises(Exception, message="ODict does not allow construction from a dict"):
        ODict({
            "z": 1,
            "a": 2,
        })


def test_explicit_sorting():
    """
    Even an explicit sort should result in no change
    """

    case = ODict((
        ("z", 1),
        ("a", 2),
    )).items()

    actual = sorted(case)

    assert actual == case
