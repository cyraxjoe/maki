import cherrypy
from cherrypy import tools

import maki.scaffold

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="post/list.mako")
    def index(self):
        return {}


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
    def update(self, id_):
        valid_fields = set(self.ctrl.get_edit_form().data)
        changes = set(cherrypy.request.json)
        unknown_fields = changes - valid_fields
        if unknown_fields:
            cherrypy.response.status = 500
            return {'updated': False,
                    'messages': ['Invalid field %s' % f
                                 for f in unknown_fields]}
        else:
            errormsg = \
            self.ctrl.update_post(id_, autotag=True, **cherrypy.request.json)
            if errormsg is None:
                return {'updated': True,
                        'messages': []}
            else:
                cherrypy.response.status = 500
                return {'updated': False,
                        'messages': ['Unable to store the data',
                                     errormsg]}
