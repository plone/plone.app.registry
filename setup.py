from setuptools import setup, find_packages

version = '1.2.5'

setup(name='plone.app.registry',
      version=version,
      description="Zope 2 and Plone  integration for plone.registry",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from
      # https://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
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
          'lxml',
          'setuptools',
          'plone.registry>=1.0b1',
          'plone.supermodel>=1.1dev',
          'plone.app.z3cform',
          'plone.autoform>=1.0b2',
          'Products.CMFPlone',
          'Zope2',
          'Products.CMFCore',
          'Products.GenericSetup',
          'Products.statusmessages',
          'zope.component',
          'zope.interface',
          'zope.i18nmessageid',
          'zope.dottedname',
      ],
      extras_require={'test': ['plone.app.testing',]},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
