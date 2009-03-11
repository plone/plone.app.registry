from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='plone.app.registry',
      version=version,
      description="Zope 2 and PLlone  integration for plone.registry",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone registry settings configuration',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/plone.app.registry',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.registry',
          'plone.supermodel',
          'plone.app.z3cform',
          'plone.autoform',
          'Plone',
          'elementtree',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
