#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: $pip install .
import os
from setuptools import setup, find_packages

def get_pkg_info(info_file, info):
    val = ""
    info_file.seek(0)
    for line in info_file:
        if line.startswith('__{}__'.format(info)):
            val = line.split("=")[1].replace("'", "").replace('"', "").strip()
    return val

with open(os.path.join('lsys', '__init__.py')) as init_file:
    author = get_pkg_info(init_file, 'author')
    email = get_pkg_info(init_file, 'email')
    version = get_pkg_info(init_file, 'version')

with open('README.rst') as readme_file:
    readme = readme_file.read()

PACKAGE_DATA = {'lsys.tests.baseline_images.test_viz': ['*png']}

requirements = ['numpy', 'matplotlib']

test_requirements = ['pytest>=3.1', 'pytest-mpl>=0.8']

setup(
    name='lsys',
    version=version,
    description="Create and visualize Lindenmayer systems",
    long_description=readme,
    author=author,
    author_email=email,
    url='https://github.com/austinorr/lsys',
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=requirements,
    extras_require={'testing': test_requirements},
    license="BSD license",
    zip_safe=False,
    keywords=['l-systems', 'lindenmayer', 'fractal'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='lsys.tests',
    tests_require=test_requirements
)
