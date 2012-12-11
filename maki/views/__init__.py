import cherrypy

from . import (
    post,
    login,
)


@cherrypy.expose
def index():
    return "ok"

