from contextlib import contextmanager

import cherrypy
from cherrypy.lib import cptools


class View(object):
    __mime__ = 'text/html'
        
    def __init__(self, controller):
        self.ctrl = controller


class Controller(object):
    __views__ = ()


    def __init__(self):
        self.__branches__ = {}
        self.__init_branches()

    def __setattr__(self, name, value):
        # if is a controller, merge the subtree.
        if isinstance(value, Controller):
            for mime, branch in value.__branches__.items():
                if mime not in self.__branches__:
                    self.__create_branch(mime) # bridge branch.
                setattr(self.__branches__[mime], name, branch)
        super(Controller, self).__setattr__(name, value)


    def __init_branches(self):        
        for ViewClass in self.__views__:
            self.__create_branch(ViewClass.__mime__,
                                 (self, ),  # connect the controller.
                                 ViewClass)
        # create the routes of the subcontrollers already binded to the class
        # We are using again the "isinstance" because the value could
        # be a method and this will make it a function.
        for name, value in vars(self.__class__).items():
            if not name.startswith('_') and \
                   isinstance(value, Controller):
                setattr(self, name, value)


    def __create_branch(self, mime, initargs=(), *parents):
        if mime in self.__branches__:
            raise Exception('Branch "%s" already exists' % mime)
        else:
            clsname = ''.join([self.__class__.__name__,
                               mime.split('/')[-1].upper(),
                               'Branch'])
            Branch = type(clsname, parents, {})
            self.__branches__[mime] = Branch(*initargs)


        


class ContentTypeDispatcher(cherrypy.dispatch.Dispatcher):

    @contextmanager
    def _branch(self, root, branch_name):
        app = cherrypy.request.app
        branch = root.__branches__[branch_name]
        app.root = branch
        yield
        app.root = root
    

    def find_handler(self, path_info):
        app = cherrypy.serving.request.app
        parentcls = super(ContentTypeDispatcher, self)
        try:
            bmimes = list(root.__branches__)
            if bmimes:
                if 'text/html' in bmimes: # set text html at top.
                    bmimes.insert(0, bmimes.pop(bmimes.index('text/html')))
                branch_name = cptools.accept(media=bmimes)
                with self._branch(app.root, branch_name):
                    return parentcls.find_handler(path_info)
        except AttributeError as err:
            cherrypy.log.error(str(err))
        return parentcls.find_handler(path_info)

        

# Example
class JSONComment(View):
    __mime__ = 'application/json'

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def index(self):
        return  {'cnt': "Comment index",
                 'ctrl': str(self.ctrl.fetch_comment())}


class JSONPost(View):
    __mime__ = 'application/json'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        return {'cnt': "Post index",
                'ctrl': str(self.ctrl)}


class HTMLPost(View):
    
    @cherrypy.expose
    def index(self):
        return "HTML Post INDEX"


class HTMLRoot(View):

    @cherrypy.expose
    def index(self):
        return "HTML root index"
    

class Comment(Controller):
    __views__ = [JSONComment]

    def fetch_comment(self):
        return {"name": "Example",
                "content": "Le content"}


class Post(Controller):
    __views__ = [HTMLPost, JSONPost]


class Root(Controller):
    __views__ =  [HTMLRoot]
    post = Post()


if __name__ == '__main__':
    root = Root()
    root.post.comment = Comment()
    config = {'/': {'request.dispatch': ContentTypeDispatcher()}}
    cherrypy.quickstart(root, config=config)
