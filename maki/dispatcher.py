import cherrypy

class JSONnHTML(object):

    def __init__(self, controller, jsonrs, htmlrs):
        self.jsonrs = jsonrs
        self.htmlrs = htmlrs
        self.ctrlr = controller

    def __call__(self, vpath):
        cherrypy.log.error(str(vpath))
        if vpath:
            id_ = vpath.pop()
            if is_a_json_request(id_):
                id_ = id_[-5]
                return self.jsonrs(self.ctrlr, id_)
            else:
                return self.htmlrs(self.ctrlr, id_)
        else:
            return False

        
    def POST(self, **params):
        if is_a_json_request():
            return self.jsonrs().POST(**params)
        else:
            return self.htmlrs().POST(**params)


def is_a_json_request(vpath=None):
    if vpath is None:
        accept = cherrypy.request.headers['Accept'].split(',')
        if len(accept) == 1  and accept[0] == 'application/json':
            return True
        else:
            return False
    else:
        return vpath.endswith('.json')
        
