import cherrypy
from cherrypy import tools

from . import View
from maki.forms import  CompatParams
from maki.utils import log


class HTMLPost(View):

    @cherrypy.expose
    @tools.mako(filename="post/list.mako")
    def index(self):
        return {}


    @cherrypy.expose
    @tools.mako(filename="post/show.mako")
    def default(self, category=None, slug=None):
        if slug is None: # for backwards compatibility, we use category.
            slug = category
        post = self.ctrl.get_post_by_slug(slug)
        if post is None:
            raise cherrypy.NotFound()
        else:
            return {'post': post,
                    'parents': []}

            
        
        

    
class JSONPost(View):
    __mime__ = 'application/json'

        

    @cherrypy.expose
    @tools.json_out()
    def default(self, id):
        post = self.ctrl.get_post_by_id(self.id)
        pdict ={'title': post.title,
                'abstract': post.content,
                'created': post.created.ctime(),
                'content': post.content,
                'slug': post.slug,
                'category': post.category.name,
                'author': post.author.name,
                'format': post.format.name,
                'tags': [t.name for t in post.tags],
                'id': post.id}
        if post.modified:
            pdict['modfied'] =  post.modified.ctime()
        return pdict


    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('POST',))
    def update(self, id_):
        form = self.ctrl.get_edit_form()
        form.process(CompatParams(cherrypy.request.json))
        if form.validate():
            errormsg = self.ctrl.update_post(**form.data)
            if errormsg is None:
                return {'updated': True,
                        'messages': []}
            else:
                return {'updated': False,
                        'messages': ['Unable to store the data',
                                     errormsg]}
        else:
            return {'updated': False,
                    'messages': form.errors}
            
            
        
        
        
        
