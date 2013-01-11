import cherrypy
from cherrypy import tools

import maki.scaffold

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self):
        posts = self.ctrl.get_posts()
        return {'posts': posts}
        
    
