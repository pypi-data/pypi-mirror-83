# -*- coding: utf-8 -*-

version = '1.2.9'

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='cpskin.slider',
      version=version,
      description='Slider package for cpskin',
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
      ],
      keywords='',
      author='IMIO',
      author_email='support@imio.be',
      url='https://github.com/imio/',
      license='gpl',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.api',
          'cpskin.locales',
          'cpskin.core',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'plone.api',
              'plone.app.robotframework',
              'plone.app.testing',
          ]
      },
      entry_points={},)
