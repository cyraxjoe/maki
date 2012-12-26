import cherrypy
from cherrypy import tools

from maki.views import View

class HTMLFrontPage(View):


    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self):
        posts = self.ctrl.get_posts()
        return {'posts': posts}
        
    
