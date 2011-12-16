# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.simplesocial
"""
import os
import sys
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.8'

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n'
    )

tests_require=['zope.testing']

if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    requires = ['simplejson']
else:
    requires = []

setup(name='collective.simplesocial',
      version=version,
      description="Basic Facebook Connect support for Plone",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='facebook connect social network feed fan',
      author='Groundwire',
      author_email='info@groundwire.org',
      url='http://plone.org/products/simplesocial',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'collective.autopermission',
                        'plone.app.z3cform',
                        ] + requires,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'collective.simplesocial.tests.test_docs.test_suite',
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
