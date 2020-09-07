# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.7.7'

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
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
