#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='stayawake',
    version='0.1.0',
    description="A tool for keeping your computer awake",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kevin Wierman",
    author_email='kwierman@gmail.com',
    url='https://github.com/kwierman/stayawake',
    packages=find_packages(exclude=["tests", "docs"]),
    package_dir={'stayawake':
                 'stayawake'},
    entry_points={
        'console_scripts': [
            'stayawake=stayawake.cli:main'
        ]
    },
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='stayawake',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    install_requires=['pyautogui==0.9.52',
                      'click>=7.0.0',],
)
