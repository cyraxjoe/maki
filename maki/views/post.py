import cherrypy
from cherrypy import tools

from maki.views import BaseView

@tools.mako(filename="post/list.mako")
def GET():
    return {}



class HTMLPost(BaseView):

    @tools.mako(filename="post/get.mako")
    def GET(self):
        return {}


    def POST(self, **params):
        cherrypy.log.error('HTML POST')
        return "POSTed HTML"
        

    
class JSONPost(BaseView):

    @tools.json_out()
    def GET(self):
        return {'title': 'Le mighty post\nasas\n',
                'content': 'Le content',
                'created': '12/12/12-11:11:11'
                }

    
    def POST(self, **params):
        cherrypy.log.error('JSON POST')
        return "POSTed JSON"


    def PUT(self):
        pass


    def DELETE(self):
        pass

