[![Build Status](https://www.travis-ci.org/awslabs/aws-cfn-template-flip.svg?branch=master)](https://www.travis-ci.org/awslabs/aws-cfn-template-flip)
[![PyPI version](https://badge.fury.io/py/cfn-flip.svg)](https://badge.fury.io/py/cfn-flip)
[![Codecov Test Coverage](https://codecov.io/gh/awslabs/aws-cfn-template-flip/branch/master/graphs/badge.svg?style=flat)](https://codecov.io/gh/awslabs/aws-cfn-template-flip)
[![Snap Status](https://build.snapcraft.io/badge/awslabs/aws-cfn-template-flip.svg)](https://build.snapcraft.io/user/awslabs/aws-cfn-template-flip)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-white.svg)](https://snapcraft.io/cfn-flip)

# AWS CloudFormation Template Flip

## About

AWS CloudFormation Template Flip is a tool that converts [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates between [JSON](http://json.org/) and [YAML](http://yaml.org) formats, making use of the YAML format's short function syntax where possible.

The term "Flip" is inspired by the well-known Unix command-line tool [flip](https://ccrma.stanford.edu/~craig/utility/flip/) which converts text files between Unix, Mac, and MS-DOS formats.

## Installation

AWS CloudFormation Template Flip can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install cfn-flip
```

## Usage

AWS CloudFormation Template Flip is both a command line tool and a python library.

Note that the command line tool is spelled `cfn-flip` with a hyphen, while the python package is `cfn_flip` with an underscore.

### Command line tool

```
Usage: cfn-flip [OPTIONS] [INPUT] [OUTPUT]

  AWS CloudFormation Template Flip is a tool that converts AWS
  CloudFormation templates between JSON and YAML formats, making use of the
  YAML format's short function syntax where possible."

Options:
  -i, --input [json|yaml]   Specify the input format. Overrides -j and -y
                            flags.
  -o, --output [json|yaml]  Specify the output format. Overrides -j, -y, and
                            -n flags.
  -j, --json                Convert to JSON. Assume the input is YAML.
  -y, --yaml                Convert to YAML. Assume the input is JSON.
  -c, --clean               Performs some opinionated cleanup on your
                            template.
  -l, --long                Use long-form syntax for functions when converting
                            to YAML.
  -n, --no-flip             Perform other operations but do not flip the
                            output format.
  --version                 Show the version and exit.
  --help                    Show this message and exit.
```


cfn-flip will detect the format of the input template and convert JSON to YAML and YAML to JSON, respectively.

Examples:

* Reading from `stdin` and outputting to `stdout`:

    ```bash
    cat examples/test.json | cfn-flip
    ```

* Reading from a file and outputting to `stdout`:

    ```bash
    cfn-flip examples/test.yaml
    ```

* Reading from a file and outputting to another file:

    ```bash
    cfn-flip examples/test.json output.yaml
    ```

* Reading from a file and cleaning up the output

    ```bash
    cfn-flip -c examples/test.json
    ```

### Python package

To use AWS CloudFormation Template Flip from your own python projects, import one of the functions `flip`, `to_yaml`, or `to_json` as needed.

```python
from cfn_flip import flip, to_yaml, to_json

"""
All functions expect a string containing serialised data
and return a string containing serialised data
or raise an exception if there is a problem parsing the input
"""

# flip takes a best guess at the serialisation format
# and returns the opposite, converting json into yaml and vice versa
some_yaml_or_json = flip(some_json_or_yaml)

# to_json expects serialised yaml as input, and returns serialised json
some_json = to_json(some_yaml)

# to_yaml expects serialised json as input, and returns serialised yaml
some_yaml = to_yaml(some_json)

# The clean_up flag performs some opinionated, CloudFormation-specific sanitation of the input
# For example, converting uses of Fn::Join to Fn::Sub
# flip, to_yaml, and to_json all support the clean_up flag
clean_yaml = to_yaml(some_json, clean_up=True)
```
