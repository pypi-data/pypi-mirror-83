#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'PyJWT',
    'requests',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='btc_top_pool_api_sdk',
    version='1.0.2',
    description="Pool OpenAPI SDK.",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Mars Yuan",
    author_email='marshalys@gmail.com',
    url='https://github.com/btc-top/pool-api-doc',
    packages=[
        'btc_top_pool_api_sdk',
    ],
    package_dir={'btc_top_pool_api_sdk':
                 'btc_top_pool_api_sdk'},
    include_package_data=True,
    install_requires=requirements,
    license="",
    zip_safe=False,
    keywords='pool-api-sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
