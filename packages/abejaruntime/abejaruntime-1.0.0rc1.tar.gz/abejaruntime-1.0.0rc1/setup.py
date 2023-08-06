#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import abejaruntime36.version


def _install_requires():
    requires = [
        'numpy',
    ]
    return requires


if __name__ == '__main__':
    description = 'ABEJA Platform Runtime for Python'
    setup(
        name='abejaruntime',
        version=abejaruntime36.version.VERSION,
        python_requires='>=3.6,<4.0',
        install_requires=_install_requires(),
        description=description,
        author='ABEJA Inc.',
        author_email='dev@abeja.asia',
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: Apache Software License",
        ],
        packages=find_packages(exclude=["tests.*", "tests"]),
        include_package_data=True,
        zip_safe=False,
        entry_points={
            "console_scripts": [
                "abeja-runtime-python = abejaruntime36.run:main"
            ]
        }
    )
