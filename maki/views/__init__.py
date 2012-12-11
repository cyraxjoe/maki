import cherrypy
from cherrypy import tools

from . import (
    post,
    login,
)


@cherrypy.expose
@tools.mako(filename="index.mako")
def index():
    return {}

