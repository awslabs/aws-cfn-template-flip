# AWS CloudFormation Template Flip

## About

AWS CloudFormation Template Flip is a tool that converts [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates between [JSON](http://json.org/) and [YAML](http://yaml.org) formats, making use of the YAML format’s short function syntax where possible.

The term "Flip" is inspired by the well-known Unix command-line tool [flip](https://ccrma.stanford.edu/~craig/utility/flip/) which converts text files between Unix, Mac, and MS-DOS formats.

## Installation

AWS CloudFormation Template Flip can be installed using [pip](https://pip.pypa.io/en/stable/):

    pip install cfn_flip

## Usage

AWS CloudFormation Template Flip is both a command line tool and a python library.

Note that the command line tool is spelled `cfn-flip` with a hyphen, while the python package is `cfn_flip` with an underscore.

### Command line tool

    cfn-flip [-h] [-c] [input] [output]

    AWS CloudFormation Template Flip is a tool that converts AWS CloudFormation
    templates between JSON and YAML formats, making use of the YAML format's short
    function syntax where possible.

    positional arguments:
      input        File to read from. If you do not supply a file, input will be
                   read from stdin.
      output       File to write to. If you do not supply a file, output will be
                   written to stdout.

    optional arguments:
      -h, --help   show this help message and exit
      -c, --clean  Performs some opinionated cleanup on your template. For now,
                   this just converts uses of Fn::Join to Fn::Sub.

Cloudflip will detect the format of the input template and convert JSON to YAML and YAML to JSON, respectively.

Examples:

* Reading from `stdin` and outputting to `stdout`:

        cat examples/test.json | cfn-flip

* Reading from a file and outputting to `stdout`:

        cfn-flip examples/test.yaml

* Reading from a file and outputting to another file:

        cfn-flip examples/test.json output.yaml

* Reading from a file and cleaning up the output

        cfn-flip -c examples/test.json

### Python package

To use AWS CloudFormation Template Flip from your own python projects, import one of the functions `flip`, `to_yaml`, or `to_json` as needed.

    from cfn_flip import flip, to_yaml, to_json

    some_yaml_or_json = flip(some_json_or_yaml)
    some_json = to_json(some_yaml)
    some_yaml = to_yaml(some_json)
    clean_yaml = to_yaml(some_json, clean_up=True)
