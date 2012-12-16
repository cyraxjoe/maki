from cherrypy import tools
from . import post, login

exposed = True

@tools.mako(filename="index.mako")
def GET():
    return {}

