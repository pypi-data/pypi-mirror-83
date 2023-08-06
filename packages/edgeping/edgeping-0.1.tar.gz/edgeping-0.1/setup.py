# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise ValueError("Requires Python 3.6 or superior")

from edgeping import __version__  # NOQA

install_requires = []

with open("README.rst") as f:
    description = f.read()


classifiers = [
    "Programming Language :: Python",
    "License :: OSI Approved :: Apache Software License",
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3 :: Only",
]


setup(
    name="edgeping",
    version=__version__,
    url="https://github.com/tarekziade/edgeping",
    packages=find_packages(),
    long_description=description.strip(),
    description=("Mozilla Edge Server."),
    author="Tarek Ziade",
    author_email="tarek@ziade.org",
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    install_requires=install_requires,
    entry_points="""
      [console_scripts]
      edgeping = edgeping.server:main
      """,
)
