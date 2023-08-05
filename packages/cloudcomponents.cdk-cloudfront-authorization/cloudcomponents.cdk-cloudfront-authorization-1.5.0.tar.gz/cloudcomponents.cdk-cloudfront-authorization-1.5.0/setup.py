import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudcomponents.cdk-cloudfront-authorization",
    "version": "1.5.0",
    "description": "CloudFront with Cognito authentication using Lambda@Edge",
    "license": "MIT",
    "url": "https://github.com/cloudcomponents/cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cloudcomponents/cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudcomponents.cdk_cloudfront_authorization",
        "cloudcomponents.cdk_cloudfront_authorization._jsii"
    ],
    "package_data": {
        "cloudcomponents.cdk_cloudfront_authorization._jsii": [
            "cdk-cloudfront-authorization@1.5.0.jsii.tgz"
        ],
        "cloudcomponents.cdk_cloudfront_authorization": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-certificatemanager>=1.69.0, <2.0.0",
        "aws-cdk.aws-cloudfront-origins>=1.69.0, <2.0.0",
        "aws-cdk.aws-cloudfront>=1.69.0, <2.0.0",
        "aws-cdk.aws-cognito>=1.69.0, <2.0.0",
        "aws-cdk.aws-iam>=1.69.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.69.0, <2.0.0",
        "aws-cdk.aws-s3>=1.69.0, <2.0.0",
        "aws-cdk.core>=1.69.0, <2.0.0",
        "aws-cdk.custom-resources>=1.69.0, <2.0.0",
        "cloudcomponents.cdk-deletable-bucket>=1.4.0, <2.0.0",
        "cloudcomponents.cdk-lambda-at-edge-pattern>=1.4.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.13.0, <2.0.0",
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
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
