"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

from . import flip
import sys

def main():
    """
    Figure out the input and output stream
    Then figure out the input format and set the opposing output format
    """

    ins = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin
    outs = open(sys.argv[2], "w") if len(sys.argv) > 2 else sys.stdout

    template = ins.read()

    try:
        outs.write(flip(template))
    except Exception as e:
        sys.stderr.write("{}\n".format(str(e)))
        sys.exit(1)
