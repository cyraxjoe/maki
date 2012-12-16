from cherrypy import tools

from maki import dispatcher


class HTMLPost(object):
    def __init__(self, id):
        self.id = id

    @tools.mako(filename="post/get.mako")
    def GET(self):
        return {}

    
class JSONPost(object):
    def __init__(self, id):
        self.id = id

    @tools.json_out()
    def GET(self):
        return {'name': 'test'}



exposed = True
_cp_dispatch = dispatcher.JSONnHTML(JSONPost, HTMLPost)

@tools.mako(filename="post/list.mako")
def GET():
    return {}


