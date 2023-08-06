import json
import os
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))

package_name = package["name"].replace(" ", "_").replace("-", "_")

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[],
     # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers = [
        'Framework :: Dash',
    ],    
)
