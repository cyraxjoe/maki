import cherrypy
from cherrypy import tools

import maki.views as views
from maki.db import with_dbs




@views.bind
@with_dbs
class Post(object):


    @cherrypy.expose
    @tools.mako(filename='post/index.mako')
    def default(self, postid=None):
        cherrypy.log.error('self.dbs')
        return {}

    @cherrypy.expose
    def add(self):
        pass
        
        
    
    
