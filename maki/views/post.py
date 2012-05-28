import cherrypy
from cherrypy import tools

class Post(object):

    @cherrypy.expose
    @tools.mako(filename='post.mako')
    def index(self):
        return {}
        
        
    
    
