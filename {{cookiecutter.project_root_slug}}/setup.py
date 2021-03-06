#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

import os

PACKAGE_NAME = '{{ cookiecutter.project_slug }}'


###########################
# Readme and longdesc
###########################
try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')

except ImportError:
    convert = None
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )
    def read_md(f):
        return open(f, 'r').read()  # noqa

def file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

readme = read_md(file_path('README.md')) if os.path.exists('README.md') else read_md('README.rst')
hist_fn = file_path('HISTORY.rst')
history =  hist_fn if os.path.exists(hist_fn) else read_md(file_path('HISTORY.md'))


###########################
# Version
###########################

def get_version(version_tuple):
    # additional handling of a,b,rc tags, this can
    # be simpler depending on your versioning scheme
    if not isinstance(version_tuple[-1], int):
        return '.'.join(
            map(str, version_tuple[:-1])
        ) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


# path to the packages __init__ module in project
# source tree
init = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, '__init__.py')
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(init))
)[0]

VERSION = get_version(eval(version_line.split('=')[-1]))

###########################
# requirements
###########################

#see https://caremad.io/posts/2013/07/setup-vs-requirement/
#and https://packaging.python.org/discussions/install-requires-vs-requirements/

def strip_comments(l):
    return l.split('#', 1)[0].strip()


requirements = [
    {%- if cookiecutter.command_line_interface|lower == 'click' %}
    'Click',
    {%- endif %}
    # TODO: Put package requirements here
]

setup_requirements = [
{%- if cookiecutter.use_pytest == 'y' %}
    'pytest-runner',
{%- endif %}
# TODO ({{ cookiecutter.git_username }}): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
{%- if cookiecutter.use_pytest == 'y' %}
    'pytest',
{%- endif %}
# TODO: Put package test requirements here
]


{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    name='{{ cookiecutter.project_slug }}',
    version=VERSION,
    description="{{ cookiecutter.project_short_description }}",
    long_description=readme + '\n\n' + history,
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}']),
    # url='https://github.com/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}',
    package_dir={'{{ cookiecutter.project_slug }}':
                 '{{ cookiecutter.project_slug }}'},
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
        ],
    },
    {%- endif %}
    include_package_data=True,
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    zip_safe=False,
    keywords='{{ cookiecutter.project_slug }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
