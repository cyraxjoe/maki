import cherrypy
from maki import db

@cherrypy.expose
def index():
    return "ok %s" % db.ses
