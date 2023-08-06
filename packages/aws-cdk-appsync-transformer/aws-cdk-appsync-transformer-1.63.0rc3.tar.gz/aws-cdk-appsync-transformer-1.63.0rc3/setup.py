import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk-appsync-transformer",
    "version": "1.63.0-rc.3",
    "description": "AWS Amplify inspired CDK construct for creating @directive based AppSync APIs",
    "license": "Apache-2.0",
    "url": "https://github.com/kcwinner/appsync-transformer-construct.git",
    "long_description_content_type": "text/markdown",
    "author": "Ken Winner",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kcwinner/appsync-transformer-construct.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk_appsync_transformer",
        "aws_cdk_appsync_transformer._jsii"
    ],
    "package_data": {
        "aws_cdk_appsync_transformer._jsii": [
            "aws-cdk-appsync-transformer@1.63.0-rc.3.jsii.tgz"
        ],
        "aws_cdk_appsync_transformer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-appsync==1.63.0",
        "aws-cdk.aws-cognito==1.63.0",
        "aws-cdk.aws-dynamodb==1.63.0",
        "aws-cdk.aws-iam==1.63.0",
        "aws-cdk.aws-lambda==1.63.0",
        "aws-cdk.core==1.63.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.12.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
