import cherrypy

class JSONnHTML(object):

    def __init__(self, jsonrs, htmlrs):
        jsonrs.exposed = True
        htmlrs.exposed = True
        self.jsonrs = jsonrs
        self.htmlrs = htmlrs

    def __call__(self, vpath):
        cherrypy.log.error(str(vpath))
        if vpath:
            id_ = vpath.pop()
            if id_.endswith('.json'):
                id_ = id_[-5]
                return self.jsonrs(id_)
            else:
                return self.htmlrs(id_)
        else:
            return False


