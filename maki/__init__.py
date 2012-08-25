import os
import cherrypy
import maki.ctools
import maki.cplugins
import maki.views

maki.views.setup()
local_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))
app = cherrypy.Application(maki.views.root, '/')
