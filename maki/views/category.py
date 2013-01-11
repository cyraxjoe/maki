import cherrypy
from cherrypy import tools

import maki.scaffold

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="category/list.mako")
    def default(self, slug):
        category = self.ctrl.get_category_by_slug(slug)
        if category is None:
            raise cherrypy.NotFound()
        else:
            return {'category': category,
                    'posts': self.ctrl.get_posts(category)}
