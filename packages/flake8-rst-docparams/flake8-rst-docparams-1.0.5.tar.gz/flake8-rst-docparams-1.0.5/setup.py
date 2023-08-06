# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from importlib.machinery import SourceFileLoader


def get_version() -> str:
    """
    Get the site-engine version string.

    :return: str
    """
    m = SourceFileLoader('init', 'src/flake8_rst_docparams/__init__.py').load_module()
    return m.__version__

setup(
    name='flake8-rst-docparams',
    long_description=open('README.rst').read(),
    version=get_version(),
    description='Check for reStructuredText function parameter documentation',
    author='Jakob Simon-Gaarde',
    author_email='jakobsg@gmail.com',
    url='https://bitbucket.org/jakobsg/flake8-rst-docparams',
    package_dir={'': 'src/'},
    packages=find_packages('src'),
    entry_points={
        'flake8.extension': [
            'DP = flake8_rst_docparams.check_params:CheckSource',
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Flake8",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance"
    ],
)
