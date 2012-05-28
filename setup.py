import os 
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['CherryPy>=3.2',
            'Mako>=0.7',
            'storm>=0.19']

setup(name='Maki',
      version='0.0.0',
      author='Joel Rivera',
      author_email='rivera@joel.mx',
      provides=['maki',],
      packages=['maki',],
      install_requires=requires)
