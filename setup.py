"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from setuptools import setup

setup(
    name="cfn_flip",
    version="0.2.4",
    description="Convert AWS CloudFormation templates between JSON and YAML formats",
    url="https://github.com/awslabs/aws-cfn-template-flip",
    author="Steve Engledow",
    author_email="sengledo@amazon.co.uk",
    license="Apache2",
    packages=["cfn_flip"],
    install_requires=[
        "PyYAML",
        "six",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["cfn-flip=cfn_flip.main:main"],
    },
)
