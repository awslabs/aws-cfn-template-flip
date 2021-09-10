"""
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License. A copy of the License is located at

    https://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from cfn_tools.odict import ODict
from cfn_tools.literal import LiteralString
from collections.abc import KeysView

import json
import six

UNCONVERTED_KEYS = [
    # Resource Type, String Attribute to keep Json
    ("AWS::StepFunctions::StateMachine", "DefinitionString")
]


def has_intrinsic_functions(parameter):
    intrinsic_functions = ["Fn::Sub", "!Sub", "!GetAtt"]
    result = False
    if isinstance(parameter, (list, tuple, dict, KeysView)):
        for item in parameter:
            if item in intrinsic_functions:
                result = True
                break
    return result


def convert_join(value):
    """
    Fix a Join ;)
    """

    if not isinstance(value, list) or len(value) != 2:
        # Cowardly refuse
        return value

    sep, parts = value[0], value[1]

    if isinstance(parts, six.string_types):
        return parts

    if not isinstance(parts, list):
        # This looks tricky, just return the join as it was
        return {
            "Fn::Join": value,
        }

    plain_string = True

    args = ODict()
    new_parts = []

    for part in parts:
        part = clean(part)

        if isinstance(part, dict):
            plain_string = False

            if "Ref" in part:
                new_parts.append("${{{}}}".format(part["Ref"]))
            elif "Fn::GetAtt" in part:
                params = part["Fn::GetAtt"]
                new_parts.append("${{{}}}".format(".".join(params)))
            else:
                for key, val in args.items():
                    # we want to bail if a conditional can evaluate to AWS::NoValue
                    if isinstance(val, dict):
                        if "Fn::If" in val and "AWS::NoValue" in str(val["Fn::If"]):
                            return {
                                "Fn::Join": value,
                            }

                    if val == part:
                        param_name = key
                        break
                else:
                    param_name = "Param{}".format(len(args) + 1)
                    args[param_name] = part

                new_parts.append("${{{}}}".format(param_name))

        elif isinstance(part, six.string_types):
            new_parts.append(part.replace("${", "${!"))

        else:
            # Doing something weird; refuse
            return {
                "Fn::Join": value
            }

    source = sep.join(new_parts)

    if plain_string:
        return source

    if args:
        return ODict((
            ("Fn::Sub", [source, args]),
        ))

    return ODict((
        ("Fn::Sub", source),
    ))


def clean(source):
    """
    Clean up the source:
    * Replace use of Fn::Join with Fn::Sub
    * Keep json body for specific resource properties
    """

    if isinstance(source, dict):
        for key, value in source.items():
            if key == "Fn::Join":
                return convert_join(value)

            else:
                source[key] = clean(value)

    elif isinstance(source, list):
        return [clean(item) for item in source]

    return source


def cfn_literal_parser(source):
    """
    Sanitize the source:
    * Keep json body for specific resource properties
    """

    if isinstance(source, dict):
        for key, value in source.items():
            if key == "Type":
                for item in UNCONVERTED_KEYS:
                    if value == item[0]:
                        # Checking if this resource has "Properties" and the property literal to maintain
                        # Better check than just try/except KeyError :-)
                        if source.get("Properties") and source.get("Properties", {}).get(item[1]):
                            if isinstance(source["Properties"][item[1]], dict) and \
                                    not has_intrinsic_functions(source["Properties"][item[1]].keys()):
                                source["Properties"][item[1]] = LiteralString(u"{}".format(json.dumps(
                                    source["Properties"][item[1]],
                                    indent=2,
                                    separators=(',', ': '))
                                ))

            else:
                source[key] = cfn_literal_parser(value)

    elif isinstance(source, list):
        return [cfn_literal_parser(item) for item in source]

    return source
