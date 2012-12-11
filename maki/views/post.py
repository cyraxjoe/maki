import cherrypy
from cherrypy import tools

from maki import db


@cherrypy.expose
@tools.mako(filename='post/index.mako')
def default(postid=None):
    cherrypy.log.error('%s' % db.ses)
    return {}

@cherrypy.expose
def add():
    pass


    
    
