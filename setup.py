#!/usr/bin/python

from setuptools import setup
#import sys, os
from jsonutil import version

setup(name='jsonutil',
      version=version,
      description="JSON Manipulation Utility",
      long_description="""\
jsonutil is a JSON manipulation utility. It lets you extract various bits of
data from a JSON object, with an easy-to-understand "path" syntax.
""",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities',
      ],
      keywords='json',
      author='David Paleino',
      author_email='d.paleino@gmail.com',
      url='http://www.hanskalabs.net/projects/jsonutil',
      license='GPL-3+',
      packages=[],
      scripts=['jsonutil'],
      include_package_data=False,
      zip_safe=False,
      requires=[
          'cjson',
      ],
)
