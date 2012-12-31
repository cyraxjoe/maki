import os 
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = ['CherryPy==3.2.2',
            'Mako==0.7.3',
            'SQLAlchemy==0.7.9',
            'psycopg2==2.4.5',
            'py3k-bcrypt==0.3',
            'beautifulsoup4==4.1.3',
            'wtforms==1.0.2',
            'textile', ]

setup(name='maki',
      version='0.0.0',
      author='Joel Rivera',
      author_email='rivera@joel.mx',
      provides=['maki',],
      packages=['maki',
                'maki.views',
                'maki.db',
                'maki.cplugins',
                'maki.ctools'],
      install_requires=requires)
