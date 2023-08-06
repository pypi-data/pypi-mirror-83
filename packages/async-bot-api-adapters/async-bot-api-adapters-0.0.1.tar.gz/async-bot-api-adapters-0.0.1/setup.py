#!/usr/bin/env python
from os.path import join, dirname
from setuptools import setup, find_packages

import adapters

setup(name='async-bot-api-adapters',
      version=adapters.__version__,
      description='Common interface for vk/telegram api calls',
      author='Sergey Konik',
      author_email='s.konik.job@gmail.com',
      url='',
      long_description=open(join(dirname(__file__), 'README.rst')).read(),
      packages=find_packages(),
      install_requires=[
          'aiovk==3.0.0',
          'aiogram==2.10.1'
      ]
)
