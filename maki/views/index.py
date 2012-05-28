import cherrypy
from cherrypy import tools

class Index(object):

    @cherrypy.expose
    @tools.mako(filename='index.mako')
    def index(self):
        return {}
        
        
