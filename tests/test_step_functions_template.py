import cfn_flip
import pytest


@pytest.fixture
def input_json_state_machine():
    with open("examples/test_json_state_machine.json", "r") as f:
        return f.read()


@pytest.fixture
def output_yaml_state_machine():
    with open("examples/test_yaml_state_machine.yaml", "r") as f:
        return f.read()


def test_state_machine_with_str(input_json_state_machine, output_yaml_state_machine):
    resp = cfn_flip.to_yaml(input_json_state_machine)
    assert resp == output_yaml_state_machine
