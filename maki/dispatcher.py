from contextlib import contextmanager

import cherrypy
from cherrypy.lib import cptools


class ContentTypeDispatcher(cherrypy.dispatch.Dispatcher):
    @contextmanager
    def _branch(self, root, branch_name):
        app = cherrypy.request.app
        branch = root.__branches__[branch_name]
        app.root = branch
        yield
        app.root = root
        # HACK ON SIGHT: Content-Language shouldn't be here.
        cherrypy.response.headers["Vary"] = "Content-Type, Accept, Content-Language"

    def find_handler(self, path_info):
        app = cherrypy.serving.request.app
        parentcls = super(ContentTypeDispatcher, self)
        try:
            bmimes = list(app.root.__branches__)
            if bmimes:
                if "text/html" in bmimes:  # set text html at top.
                    bmimes.insert(0, bmimes.pop(bmimes.index("text/html")))
                branch_name = cptools.accept(media=bmimes)
                with self._branch(app.root, branch_name):
                    return parentcls.find_handler(path_info)
        except AttributeError as err:
            cherrypy.log.error(str(err))
        return parentcls.find_handler(path_info)
