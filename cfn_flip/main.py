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
@click.option("--input", "-i", "in_format", type=click.Choice(["json", "yaml"]), help="Specify the input format. Overrides -j and -y flags.")
@click.option("--output", "-o", "out_format", type=click.Choice(["json", "yaml"]), help="Specify the output format. Overrides -j, -y, and -n flags.")
@click.option("--json", "-j", "out_flag", flag_value="json", help="Convert to JSON. Assume the input is YAML.")
@click.option("--yaml", "-y", "out_flag", flag_value="yaml", help="Convert to YAML. Assume the input is JSON.")
@click.option("--clean", "-c", is_flag=True, help="Performs some opinionated cleanup on your template.")
@click.option("--long", "-l", is_flag=True, help="Use long-form syntax for functions when converting to YAML.")
@click.option("--no-flip", "-n", is_flag=True, help="Perform other operations but do not flip the output format.")
@click.argument("input", type=click.File("r"), default=sys.stdin)
@click.argument("output", type=click.File("w"), default=sys.stdout)
@click.version_option(message='AWS Cloudformation Template Flip, Version %(version)s')
@click.pass_context
def main(ctx, **kwargs):
    """
    AWS CloudFormation Template Flip is a tool that converts
    AWS CloudFormation templates between JSON and YAML formats,
    making use of the YAML format's short function syntax where possible.
    """
    in_format = kwargs.pop('in_format')
    out_format = kwargs.pop('out_format') or kwargs.pop('out_flag')
    no_flip = kwargs.pop('no_flip')
    clean = kwargs.pop('clean')
    long_form = kwargs.pop('long')
    input_file = kwargs.pop('input')
    output_file = kwargs.pop('output')

    if not in_format:
        if input_file.name.endswith(".json"):
            in_format = "json"
        elif input_file.name.endswith(".yaml") or input_file.name.endswith(".yml"):
            in_format = "yaml"

    if input_file.name == "<stdin>" and sys.stdin.isatty():
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        flipped = flip(
            input_file.read(),
            in_format=in_format,
            out_format=out_format,
            clean_up=clean,
            no_flip=no_flip,
            long_form=long_form
        )
        output_file.write(flipped)
    except Exception as e:
        raise click.ClickException("{}".format(e))
