#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import setuptools


author = 'XESS Corp.'
email = 'info@xess.com'
version = '0.0.1'

if 'sdist' in sys.argv[1:]:
    with open('pygmyhdl/pckg_info.py','w') as f:
        for name in ['version','author','email']:
            f.write("{} = '{}'\n".format(name,locals()[name]))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # Put package requirements here
    'future >= 0.15.0',
]

test_requirements = [
    # Put package test requirements here
    'pytest',
]

setup(
    name='pygmyhdl',
    version = version,
    description="Pygmy version of MyHDL.",
    long_description=readme + '\n\n' + history,
    author = author,
    author_email= email,
    url='https://github.com/xesscorp/pygmyhdl',
#    packages=['pygmyhdl',],
    packages=setuptools.find_packages(),
    entry_points={'console_scripts':['pygmyhdl = pygmyhdl.__main__:main']},
    package_dir={'pygmyhdl':
                 'pygmyhdl'},
    include_package_data=True,
    package_data={'pygmyhdl': ['*.gif', '*.png']},
    scripts=[],
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pygmyhdl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)