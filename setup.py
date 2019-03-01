#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()

requirements = [

]

test_requirements = [

]

setup(
    name='pyrwr',
    version='1.0.0',
    description='Python Implementation for Random Walk with Restart',
    long_description=readme,
    author='Jinhong Jung',
    author_email='jinhongjung@snu.ac.kr',
    url='https://github.com/jinhongjung/pyrwr',
    entry_points={
        'console_scripts': [
            'pyrwr=pyrwr.__main__:main'
        ]
    },
    packages=['pyrwr', 'utils'],
    include_package_data=True,
    install_requirements=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6.6',
    ],
    test_suites='tests',
    test_require=test_requirements
)
