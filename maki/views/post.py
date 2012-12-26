import cherrypy
from cherrypy import tools

from . import View


class HTMLPost(View):

    @cherrypy.expose
    @tools.mako(filename="post/list.mako")
    def index(self):
        return {}
        

    
class JSONPost(View):
    __mime__ = 'application/json'

    @cherrypy.expose
    @tools.json_out()
    def default(self):
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

