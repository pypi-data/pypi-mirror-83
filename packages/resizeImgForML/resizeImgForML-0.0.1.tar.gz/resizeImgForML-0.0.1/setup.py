from setuptools import setup, find_packages
import os

name = 'resizeImgForML'
version = '0.0.1'

def read_from_file(filename):
    return open(filename).read().splitlines()


short_description = '`resizeImgForML` is a package for resize images for machie learning.'

long_description = """\
Requirements
------------
* Python 3.x

Features
--------
* nothing

History
-------

* 0.0.1 (2020-10-27)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* first release

Usage
------------
please look at Github README

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plan to upgrade
---------------------

* open image through one unipue path(it is useful for WebApp like Django) 
* open one directory and all of image at the directory 
* resize & save images for MNIST

and more, if i can

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* first release
"""

setup(
    name=name,
    version=version,
    url='https://github.com/k-mawa/resizeImgForML',
    description=short_description,
    long_description=long_description,
    keywords=['machine', 'machine learning', 'resize', 'Pillow', 'PIL', 'openCV'],
    packages=find_packages(),
    install_requires=read_from_file('requirements.txt'),
    author='Kosuke Mawatari',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],

)