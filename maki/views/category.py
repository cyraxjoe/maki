import cherrypy
from cherrypy import tools

from maki.views import View

class HTMLCategory(View):

    @cherrypy.expose
    @tools.mako(filename="category/list.mako")
    def default(self, slug):
        category = self.ctrl.get_category_by_slug(slug)
        if category is None:
            raise cherrypy.NotFound()
        else:
            return {'category': category,
                    'posts': self.ctrl.get_posts(category)}
