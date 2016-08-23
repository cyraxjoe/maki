import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()

requires = ['CherryPy',
            'Mako',
            'SQLAlchemy',
            'psycopg2',
            'beautifulsoup4',
            'docutils',
            'textile',
            'unidecode',
            'PyYaml',
            'atomize',
            'Pygments']
# tested atomize
# hg+https://joelriv@code.google.com/r/joelriv-atomize/#egg=atomize'
setup(name='maki',
      version='0.3.0',
      author='Joel Rivera',
      author_email='rivera@joel.mx',
      provides=['maki',],
      packages=['maki',
                'maki.controllers',
                'maki.cplugins',
                'maki.ctools',
                'maki.db',
                'maki.views',
                'maki.utils'
                ],
      scripts=['scripts/wsgi.py', ],
      include_package_data=True,
      install_requires=requires)
