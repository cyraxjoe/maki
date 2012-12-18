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
        post = self.ctrlr.get_post(self.id)
        pdict ={'title': post.title,
                'abstract': post.content,
                'created': post.created.ctime(),
                'content': post.content,
                'slug': post.slug,
                'category': post.category.name,
                'author': post.author.name,
                'format': post.format.name,
                'tags': [t.name for t in post.tags]}
        if post.modified:
            pdict['modfied'] =  post.modified.ctime()
        return pdict

    
    def POST(self, **params):
        cherrypy.log.error('JSON POST')
        return "POSTed JSON"


    def PUT(self):
        pass


    def DELETE(self):
        pass

