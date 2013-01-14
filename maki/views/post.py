import cherrypy
from cherrypy import tools

import maki.scaffold
#from maki.utils import log  

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="post/list.mako")
    def index(self, category):
        obcategory = self.ctrl.get_category_by_slug(category)
        if obcategory is None:
            raise cherrypy.NotFound()
        else:
            return {'category': obcategory,
                    'posts': obcategory.posts}


    @cherrypy.expose
    @tools.mako(filename="post/show.mako", csstyles=('post.css',))
    def default(self, category=None, slug=None):
        if slug is None: # for backwards compatibility, we use category.
            slug = category
        post = self.ctrl.get_post_by_slug(slug)
        if post is None:
            raise cherrypy.NotFound()
        else:
            return {'post': post,
                    'parents': [],
                    'title': post.title,
                    'styles': '/static/'}

            
class JSON(maki.scaffold.View):
    __mime__ = 'application/json'

    def _have_valid_fields(self):
        changes = set(cherrypy.request.json)
        return self.ctrl.required_fields == changes


    def _modify_post(self, update_method, actionrsl,  *args):
        if self._have_valid_fields():
            errormsg = update_method(*args, **cherrypy.request.json)
            if errormsg is None:
                return {'created': True,
                        'messages': None}
            else:
                cherrypy.response.status = 500
                return {'created': False,
                        'messages': errormsg}
        else:
            cherrypy.response.status = 500
            return {'created': False,
                    'messages': 'Missing required fields'}
        
            
    @cherrypy.expose
    @tools.json_out()
    def default(self, id):
        if not id.isdigit():
            raise cherrypy.NotFound()
        else:
            post = self.ctrl.get_post_by_id(id)
            
        pdict ={'title': post.title,
                'abstract': post.abstract,
                'created': post.created_fmt,
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
    @tools.protect()
    def add(self):
        return self._modify_post(self.ctrl.create_post, 'created')

    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('POST',))
    @tools.protect()
    def update(self, id_):
        return self._modify_post(self.ctrl.update_post, 'updated',  id_)
