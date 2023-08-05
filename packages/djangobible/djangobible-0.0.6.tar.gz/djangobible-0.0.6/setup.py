#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['djangobible', 'djangobible.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0', 'pythonbible>=0.1.1']

extras_require = \
{'test': ['pytest-django>=3.10.0']}

setup(name='djangobible',
      version='0.0.6',
      description='django-bible python library.',
      author='Nathan Patton',
      author_email='npatton@gmail.com',
      url='https://github.com/avendesora/django-bible',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.6',
     )
