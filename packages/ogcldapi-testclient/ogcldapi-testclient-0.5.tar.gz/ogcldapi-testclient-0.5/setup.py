#!/usr/bin/env python
# -*- coding: latin-1 -*-
import codecs
import re
import os
from setuptools import setup


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )
    return codecs.open(path, mode, encoding)


with open_local(['testclient', '__init__.py'], encoding='latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open_local(['README.md'], encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='ogcldapi-testclient',
    packages=['testclient'],
    package_dir={'testclient': 'testclient'},
    version=version,
    description='A test client (command line program) for implementations of the "OGC LD API" which is a variant of '
                'the standardised OGC API: Features that delivers OGC API data and also Linked Data..',
    author='Nicholas Car',
    author_email='nicholas.car@surroundaustralia.com',
    url='https://github.com/surroundaustralia/ogcldapi-testclient',
    download_url='https://github.com/surroundaustralia/ogcldapi-testclient/archive/{:s}.tar.gz'.format(version),
    license='LICENSE',
    keywords=['Open Geospatial Consortium', 'Open API', 'OGC API', 'Semantic Web', 'Linked Data API'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/surroundaustralia/ogcldapi-testclient/issues',
        'Source': 'https://github.com/surroundaustralia/ogcldapi-testclient/',
    },
)
