from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.3"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.app.registry",
    version=version,
    description="Zope 2 and Plone  integration for plone.registry",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone registry settings configuration",
    author="Martin Aspeli",
    author_email="optilude@gmail.com",
    url="https://pypi.org/project/plone.app.registry",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "lxml",
        "plone.app.z3cform",
        "plone.autoform>=1.0",
        "plone.base",
        "plone.registry>=1.0",
        "plone.supermodel>=1.1",
        "Products.statusmessages",
        "setuptools",
        "Products.GenericSetup",
        "plone.z3cform",
        "z3c.form",
        "zope.dottedname",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.testing",
        ]
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
