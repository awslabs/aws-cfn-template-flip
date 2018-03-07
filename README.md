[![Build Status](https://www.travis-ci.org/awslabs/aws-cfn-template-flip.svg?branch=master)](https://www.travis-ci.org/awslabs/aws-cfn-template-flip)
[![PyPI version](https://badge.fury.io/py/cfn_flip.svg)](https://badge.fury.io/py/cfn_flip)

# AWS CloudFormation Template Flip

## About

AWS CloudFormation Template Flip is a tool that converts [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates between [JSON](http://json.org/) and [YAML](http://yaml.org) formats, making use of the YAML format’s short function syntax where possible.

The term "Flip" is inspired by the well-known Unix command-line tool [flip](https://ccrma.stanford.edu/~craig/utility/flip/) which converts text files between Unix, Mac, and MS-DOS formats.

## Installation

AWS CloudFormation Template Flip can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install cfn_flip
```

## Usage

AWS CloudFormation Template Flip is both a command line tool and a python library.

Note that the command line tool is spelled `cfn-flip` with a hyphen, while the python package is `cfn_flip` with an underscore.

### Command line tool

    Usage: cfn-flip [OPTIONS] [INPUT] [OUTPUT]

      AWS CloudFormation Template Flip is a tool that converts AWS
      CloudFormation templates between JSON and YAML formats, making use of the
      YAML format's short function syntax where possible."

    Options:
      -j, --json     Convert to JSON. Assume the input is YAML.
      -y, --yaml     Convert to YAML. Assume the input is JSON.
      -c, --clean    Performs some opinionated cleanup on your template.
      -l, --long     Use long-form syntax for functions when converting to YAML.
      -n, --no-flip  Don't convert. If you use -n in conjunction with -j or -y,
                     the input format is assumed to be the same as the output
                     format you specify.
      --help         Show this message and exit.


Cloudflip will detect the format of the input template and convert JSON to YAML and YAML to JSON, respectively.

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
