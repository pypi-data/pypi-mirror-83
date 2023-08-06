from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "boto3==1.16.4",
        "botocore==1.19.4",
        "jmespath==0.10.0; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "s3transfer==0.3.3",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "urllib3==1.25.11; python_version != '3.4'",
    ],
    name="boto4",
    version="0.0.3",
    author="Aaron Mamparo",
    author_email="aaronmamparo@gmail.com",
    description="Enhanced boto3 functionality (made for my own use)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amamparo/boto4",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "build_lambda = boto4_scripts.build_lambda_deployment_package:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.7",
)
