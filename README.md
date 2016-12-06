# AWS CloudFormation Template Flip

## About

AWS CloudFormation Template Flip is a tool that converts [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates between [JSON](http://json.org/) and [YAML](http://yaml.org) formats, making use of the YAML format’s short function syntax where possible.

The term "Flip" is inspired by the well-known Unix command-line tool [flip](https://ccrma.stanford.edu/~craig/utility/flip/) which converts text files between Unix, Mac, and MS-DOS formats.

## Installation

AWS CloudFormation Template Flip can be installed using [pip](https://pip.pypa.io/en/stable/):

    pip install cfn_flip

## Usage

### Command line tool

    cfn-flip [<from.template> [<to.template>]]

If no filenames are supplied, input will be taken from `stdin`, and output will be to `stdout`.

If only one filename is supplied, input will be taken from the file, and output will be to `stdout`.

If two filenames are supplied, input will be taken from the first file, and output will be to the second file.

Cloudflip will detect the format of the input template and convert JSON to YAML and YAML to JSON, respectively.

Examples:

* Reading from `stdin` and outputting to `stdout`:

        cat examples/test.json | cfn-flip

* Reading from a file and outputting to `stdout`:

        cfn-flip examples/test.yaml

* Reading from a file and outputting to another file:

        cfn-flip examples/test.json output.yaml

### Python package

To use AWS CloudFormation Template Flip from your own python projects, import one of the functions `flip`, `to_yaml`, or `to_json` as needed.

    from cfn_flip import flip, to_yaml, to_json

    some_yaml_or_json = flip(some_json_or_yaml)
    some_json = to_json(some_yaml)
    some_yaml = to_yaml(some_json)
