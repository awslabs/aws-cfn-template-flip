"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import json

def convert_join(sep, parts):
    """
    Fix a Join ;)
    """

    plain_string = True

    args = {}

    for i, part in enumerate(parts):
        if isinstance(part, dict):
            plain_string = False

            if "Ref" in part:
                parts[i] = "${{{}}}".format(part["Ref"])
            elif "Fn::GetAtt" in part:
                params = part["Fn::GetAtt"]
                parts[i] = "${{{}.{}}}".format(params[0], params[1])
            else:
                param_name = "Param{}".format(len(args) + 1)
                args[param_name] = part
                parts[i] = "${{{}}}".format(param_name)

    source = sep.join(parts)

    if plain_string:
        return source

    if args:
        return {
            "Fn::Sub": [source, args],
        }
    
    return {
        "Fn::Sub": source,
    }

def clean(source):
    """
    Clean up the source:
    * Replace use of Fn::Join with Fn::Sub
    """

    if isinstance(source, dict):
        for key, value in source.items():
            if key == "Fn::Join":
                return convert_join(value[0], value[1])
            elif key == "Fn::GetAtt":
                source[key] = "{}.{}".format(value[0], value[1])
            else:
                source[key] = clean(value)

    elif isinstance(source, list):
        return [clean(item) for item in source]

    return source
