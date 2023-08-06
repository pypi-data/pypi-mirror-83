# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.1.2'

setup(name='collective.sticky',
      version=version,
      description="Collective sticky package",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Plone Zope Sticky',
      author='',
      author_email='',
      url='http://github.com/imio/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.api',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      )
