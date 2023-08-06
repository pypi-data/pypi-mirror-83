from setuptools import find_packages, setup
import os

readme_file = os.path.join(os.path.dirname(__file__), "README.md")

with open(readme_file) as readme:
    README = f"{readme.read()}"
README = README.replace(README.split("# Install")[0], "")

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="gql_lazy_paginator",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License",
    description="Lazy GraphQL pagination tools.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TokkoLabs/services-tokkobroker/libraries/rpc-plugins/tokko_rpc",
    author="Jose Salgado",
    author_email="jsalgado@navent.com",
    # ToDo: Add packages versions!
    install_requires=[
        "Django",
        "graphene-django",
        "graphene"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
