import cherrypy

from cherrypy import tools


class Root(object):

    @cherrypy.expose
    @tools.mako(filename='root.mako')
    def index(self):
        return {}
        
        
