# -*- coding: utf-8 -*-
"""Installer for the cs.zestreleaser.eggbuilder package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="cs.zestreleaser.eggbuilder",
    version="1.0.1",
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Mikel Larreategi",
    author_email="mlarreategi@codesyntax.com",
    url="https://github.com/collective/cs.zestreleaser.eggbuilder",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/cs.zestreleaser.eggbuilder",
        "Source": "https://github.com/collective/cs.zestreleaser.eggbuilder",
        "Tracker": "https://github.com/collective/cs.zestreleaser.eggbuilder/issues",
        # 'Documentation': 'https://cs.zestreleaser.eggbuilder.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["cs", "cs.zestreleaser"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "zest.releaser",
    ],
    extras_require={"test": []},
    entry_points={
        "zest.releaser.releaser.after_checkout": [
            "csseggbuilder=cs.zestreleaser.eggbuilder.builder:build"
        ],
        "zest.releaser.postreleaser.after": [
            "csseggbuilder=cs.zestreleaser.eggbuilder.builder:show_contents"
        ],
    },
)
