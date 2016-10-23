# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.5'

setup(
    name='plone.app.registry',
    version=version,
    description="Zope 2 and Plone  integration for plone.registry",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='plone registry settings configuration',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.python.org/pypi/plone.app.registry',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
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
        'Products.CMFPlone',
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
