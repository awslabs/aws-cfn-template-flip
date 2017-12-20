"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from . import flip
import click
import sys


@click.command()
@click.option("--json", "-j", "out_format", flag_value="json", help="Convert to JSON. Assume the input is YAML.")
@click.option("--yaml", "-y", "out_format", flag_value="yaml", help="Convert to YAML. Assume the input is JSON.")
@click.option("--clean", "-c", is_flag=True, help="Performs some opinionated cleanup on your template.")
@click.option("--long", "-l", is_flag=True, help="Use long-form syntax for functions when converting to YAML.")
@click.option("--no-flip", "-n", is_flag=True, help="Don't convert. If you use -n in conjunction with -j or -y, " +
                                                    "the input format is assumed to be the same as the output format" +
                                                    " you specify.")
@click.argument("input", type=click.File("r"), default=sys.stdin)
@click.argument("output", type=click.File("w"), default=sys.stdout)
@click.version_option(message='AWS Cloudformation Template Flip, Version %(version)s')
def main(**kwargs):
    """
    AWS CloudFormation Template Flip is a tool that converts
    AWS CloudFormation templates between JSON and YAML formats,
    making use of the YAML format's short function syntax where possible."
    """
    out_format = kwargs.pop('out_format')
    no_flip = kwargs.pop('no_flip')
    clean = kwargs.pop('clean')
    long_form = kwargs.pop('long')
    input_file = kwargs.pop('input')
    output_file = kwargs.pop('output')
    try:
        output_file.write(flip(
            input_file.read(),
            out_format=out_format,
            clean_up=clean,
            no_flip=no_flip,
            long_form=long_form,
        ))
    except Exception as e:
        raise click.ClickException("{}".format(e))
