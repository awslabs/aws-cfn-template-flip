from setuptools import setup

setup(
    name="CloudFormation Template Flip",
    version="0.1",
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
