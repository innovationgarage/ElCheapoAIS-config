#!/usr/bin/env python

import setuptools

setuptools.setup(name='elcheapoais-config',
      version='0.1',
      description='Configuration system for ElcheapoAIS',
      long_description='Configuration system for ElcheapoAIS',
      long_description_content_type="text/markdown",
      author='Egil Moeller',
      author_email='egil@innovationgarage.no',
      url='https://github.com/innovationgarage/ElCheapoAIS-config',
      packages=setuptools.find_packages(),
      install_requires=[
          "PyGObject",
          "dbus-python==1.2.12"
      ],
      include_package_data=True,
      entry_points='''
      [console_scripts]
      elcheapoais-config = elcheapoais_config:main
      '''
  )
