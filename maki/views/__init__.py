from cherrypy import tools

exposed = True

@tools.mako(filename="frontpage.mako")
def GET():
    return {}

class BaseView(object):
    exposed = True
    
    def __init__(self, ctrlr, id=None):
        self.ctrl = ctrlr
        self.id = id
