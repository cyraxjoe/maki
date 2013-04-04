import os 
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()

requires = ['CherryPy==3.2.2',
            'Mako==0.7.3',
            'SQLAlchemy==0.7.9',
            'psycopg2==2.4.5',
            'beautifulsoup4==4.1.3',
            'docutils',
            'textile',
            'unidecode',
            'PyYaml',
            'atomize',
            'Pygments']
# tested atomize
# hg+https://joelriv@code.google.com/r/joelriv-atomize/#egg=atomize'
setup(name='maki',
      version='0.2.0',
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
