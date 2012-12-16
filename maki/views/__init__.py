from cherrypy import tools
from . import post, login

exposed = True

@tools.mako(filename="frontpage.mako")
def GET():
    return {}

