import os
import cherrypy

from maki import scaffold; scaffold.setup() #  Yes... that's what I mean.
import maki.controllers
from maki import dispatcher  # this is going to be used in the config file.

__all__ = ['dispatcher',]

LOCAL_DIR = os.path.join(os.getcwd(), os.path.dirname(__file__))
ROOT = maki.controllers.Root()
CONFIG = lambda section: cherrypy.tree.apps[''].config[section]
