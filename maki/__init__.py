import os
import cherrypy

import maki.ctools
import maki.cplugins
import maki.views

LOCAL_DIR = os.path.join(os.getcwd(), os.path.dirname(__file__))
APP = cherrypy.Application(maki.views, '/')
