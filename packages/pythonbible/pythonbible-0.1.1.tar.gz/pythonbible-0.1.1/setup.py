#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pythonbible', 'pythonbible.bible', 'pythonbible.bible.osis']

package_data = \
{'': ['*'], 'pythonbible': ['data/*'], 'pythonbible.bible': ['osis/versions/*']}

extras_require = \
{'all': ['defusedxml >=0.6.0'],
 'dev': ['bandit >=1.6.2', 'black >=20.8b1', 'prospector >=1.3.0'],
 'test': ['pytest >=6.1.1', 'pytest-cov >=2.10.1']}

setup(name='pythonbible',
      version='0.1.1',
      description='pythonbible includes features for parsing texts for scripture references,',
      author='Nathan Patton',
      author_email='npatton@gmail.com',
      url='https://github.com/avendesora/python-bible',
      packages=packages,
      package_data=package_data,
      extras_require=extras_require,
      python_requires='>=3.6',
     )
