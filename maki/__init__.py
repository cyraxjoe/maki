import os
import cherrypy

from maki import scaffold; scaffold.setup() #  Yes... that's what I mean.
import maki.controllers
from maki import dispatcher  # used in the config file.

__all__ = ['dispatcher', 'errors']

LOCAL_DIR = os.path.join(os.getcwd(), os.path.dirname(__file__))
ROOT = maki.controllers.Root()
CONFIG = lambda section: cherrypy.tree.apps[''].config[section]
# At the bottom because the module depends on the previos variables.
from maki import errors      # used in the config file.
