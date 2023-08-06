#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'b0mb3r'
DESCRIPTION = 'Placeholder for the b0mb3r project.'
URL = 'https://pypi.org/project/b0mb3r'
EMAIL = ''
AUTHOR = 'b0mb3r'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('py setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=["b0mb3r"],
    install_requires=[],
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
