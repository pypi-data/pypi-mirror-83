#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os.path import basename
#from os.path import dirname
#from os.path import join
from os.path import splitext
from setuptools import find_packages, setup
with open('README.md') as f:
    readme = f.read()


NAME = "tiny_3d_engine"
VERSION = "0.2.1"
setup(
    name=NAME,
    version=VERSION,
    description='Open Source tiny 3D engine for tkinter',
    keywords=["3D", "python", "Tkinter"],
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Antoine Dauptain',
    author_email='coop@cerfacs.com',
    url='http://cerfacs.fr/coop/',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="CeCILL-B FREE SOFTWARE LICENSE AGREEMENT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=[
        'numpy',
        'click',
        'matplotlib',
       ],
    entry_points={
        "console_scripts": [
            "tiny_3d_engine = tiny_3d_engine.cli:main_cli",
        ]
    },
)
