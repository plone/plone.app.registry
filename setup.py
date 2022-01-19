# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.0.0a6'

setup(
    name='plone.app.registry',
    version=version,
    description="Zope 2 and Plone  integration for plone.registry",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='plone registry settings configuration',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.org/project/plone.app.registry',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml',
        'plone.app.z3cform',
        'plone.autoform>=1.0b2',
        'plone.registry>=1.0b1',
        'plone.supermodel>=1.1dev',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Products.statusmessages',
        'setuptools',
        'zope.component',
        'zope.dottedname',
        'zope.i18nmessageid',
        'zope.interface',
        'Zope2',
    ],
    extras_require={'test': ['plone.app.testing', ]},
    entry_points="""
    # -*- Entry points: -*-
    """,
)
