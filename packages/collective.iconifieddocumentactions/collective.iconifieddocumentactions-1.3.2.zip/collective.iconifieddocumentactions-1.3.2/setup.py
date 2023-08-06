# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.3.2'

setup(name='collective.iconifieddocumentactions',
      version=version,
      description="Display document_actions as icons",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Imio',
      author_email='support@imio.be',
      url='https://github.com/IMIO/collective.iconifieddocumentactions',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'plone.app.robotframework',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
