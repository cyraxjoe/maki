import types
from collections import defaultdict
from contextlib import contextmanager

import cherrypy
from cherrypy.lib import cptools


# Generic scaffolding code

class ContentTypeDispatcher(cherrypy.dispatch.Dispatcher):

    @contextmanager
    def _mime_view(self, root, branch_name):
        app = cherrypy.request.app
        branch = root._branches[branch_name]
        #cherrypy.log.error("Trying with %s" % branch)
        app.root = branch
        yield
        app.root = root
    

    def find_handler(self, path_info):
        request = cherrypy.serving.request
        root = request.app.root
        try:
            mimes  = list(root._branches.keys())
            if mimes:
                if 'text/html' in mimes: # set text html at top.
                    mimes.insert(0, mimes.pop(mimes.index('text/html')))
                #cherrypy.log.error(str(mimes))
                branch_name = cptools.accept(media=mimes)
                #cherrypy.log.error(branch)
                with self._mime_view(root, branch_name):
                    return super().find_handler(path_info)
        except AttributeError as err:
            cherrypy.log.error(str(err))
        #cherrypy.log.error('USING DEFAULT')
        return super().find_handler(path_info)



class View(object):
    MIME = 'text/html'

    def __init__(self, ctrlr):
        self.ctrl = ctrlr


class MultiViewHandler(object):
    exposed = True

    def __init__(self, *args, **kwargs):
        view_branches = {}
        controller = self
        for view in controller.__views__:
            view_branches[view.MIME] = view(controller)
        controller.__view_branches__ = view_branches


def rootview(cname, cparents, cattribs):
    # this is meant to be used as a metaclass.
    view_routes = defaultdict(dict)
    for name, value in cattribs.items():
        if not name.startswith('__') and \
               getattr(value, '__view_branches__', False):
            for branch, view in value.__view_branches__.items():
                view_routes[branch][name] = view
    cattribs['__view_routes__'] = dict(view_routes)
    return type(cname, cparents, cattribs)
            


class RootView(object):

    def __init__(self):
        self.__setup_branches()

    def __setup_branches(self):
        cherrypy.log.error('Setting branches')
        branches = {}
        cherrypy.log.error(str(self.__view_routes__))
        for bname, props in self.__view_routes__.items():
            branch = type('%sBranch%s' % (self.__class__.__name__,
                                          bname.split('/')[-1].capitalize()),
                          (), props)
            self.__inyect_methods(branch, bname)
            branches[bname] = branch
        self._branches = branches

    def __inyect_methods(self, branch, bname):
        try:
            root_branch = self.__view_branches__[bname]
        except (AttributeError, IndexError) as err:
            cherrypy.log.error(str(err))
            return
        else:
            for prop in dir(root_branch):
                methods = {}
                value = getattr(root_branch, prop)
                if not prop.startswith('_') and \
                       isinstance(value, types.MethodType) and \
                       getattr(value, 'exposed', False):
                    setattr(branch, prop, value)


class MultiRootView(MultiViewHandler, RootView):

    def __init__(self, *args, **kwargs):
        MultiViewHandler.__init__(self, *args, **kwargs)
        RootView.__init__(self, *args, **kwargs)


### Application Code

class JSONPost(View):
    MIME = 'application/json'    

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        return {"content": "hi!"}


class HTMLPost(View):

    @cherrypy.expose
    def index(self):
        return "HI!"


class Post(MultiViewHandler):
    __views__ = [HTMLPost, JSONPost]
  

class HTMLRoot(View):

    @cherrypy.expose
    def index(self):
        return "Hi from index"


class JSONRoot(View):
    MIME = 'application/json'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        return {"cnt": "Hi from index"}
    

class Root(MultiRootView, metaclass=rootview):
    __views__ = [HTMLRoot, JSONRoot]
    post = Post()


app = Root()
cherrypy.quickstart(app, config={'/': 
                                 {'request.dispatch':
                                  ContentTypeDispatcher()}})
