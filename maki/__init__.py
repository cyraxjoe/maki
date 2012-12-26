import os
import cherrypy

import maki.ctools
import maki.cplugins
from maki.controllers.root import Root
from maki import dispatcher

__all__ = ['dispatcher',]


LOCAL_DIR = os.path.join(os.getcwd(), os.path.dirname(__file__))
APP = cherrypy.Application(Root(), '/')

