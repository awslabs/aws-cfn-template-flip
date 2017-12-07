"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from . import flip
import argparse
import sys

def main():
    """
    Figure out the input and output stream
    Then figure out the input format and set the opposing output format
    """

    # Set up the arg parser
    parser = argparse.ArgumentParser(description="AWS CloudFormation Template Flip is a tool that converts AWS CloudFormation templates between JSON and YAML formats, making use of the YAML format's short function syntax where possible.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-j", "--json", action="store_true", help="Convert to JSON. Assume the input is YAML.")
    group.add_argument("-y", "--yaml", action="store_true", help="Convert to YAML. Assume the input is JSON.")

    parser.add_argument("-n", "--no-flip", action="store_true", help="Don't convert. You can use this to validate or just clean a template without converting it. If you use -n in conjunction with -j or -y, the input format is assumed to be the same as the output format you specify.")
    parser.add_argument("-c", "--clean", action="store_true", help="Performs some opinionated cleanup on your template. For now, this just converts uses of Fn::Join to Fn::Sub.")

    parser.add_argument("input", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="File to read from. If you do not supply a file, input will be read from stdin.")
    parser.add_argument("output", nargs="?", type=argparse.FileType("w"), default=sys.stdout, help="File to write to. If you do not supply a file, output will be written to stdout.")

    args = parser.parse_args()

    template = args.input.read()

    out_format = None

    if args.json:
        out_format = "json"
    elif args.yaml:
        out_format = "yaml"

    try:
        args.output.write(flip(template,
            out_format=out_format,
            clean_up=args.clean,
            no_flip=args.no_flip
        ))
    except Exception as e:
        sys.stderr.write("{}\n".format(str(e)))
        sys.exit(1)
