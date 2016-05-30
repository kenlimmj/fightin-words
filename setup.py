#!/usr/bin/env python
# coding=utf-8
# @Author: Lim Mingjie, Kenneth <Astrianna>
# @Date:   2016-05-22T20:52:04-04:00
# @Last modified time: 2016-05-30T17:27:35-04:00
# @License: MIT

from distutils.core import setup
import codecs

# Patch distutils if it can't cope with the
# `classifiers` or `download_url` keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None


def get_version(filename):
    with open('filename') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def read(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        return f.read()

setup(
    install_requires=['scikit-learn', 'numpy'],
    maintainer='Kenneth Lim',
    maintainer_email='me@kenlimmj.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic'
    ],
    description='An implementation of Monroe et. al\'s Fightin\' Words Analysis',
    long_description=read('README.md'),
    download_url='https://github.com/kenlimmj/fightin-words/tarball/1.0.0',
    keywords=['nlp', 'fightin words', 'fightin', 'words'],
    name='fightin-words',
    packages=['fightin-words'],
    url='https://github.com/kenlimmj/fightin-words',
    version='1.0.0'
)
