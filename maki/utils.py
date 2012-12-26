import pprint

import cherrypy

def log(message, cntx='DEBUG', tb=False):
    if isinstance(message, str):
        cherrypy.log.error(message, context=cntx,
                           traceback=tb)
    else:
        cherrypy.log.error(pprint.pformat(message), context=cntx,
                           traceback=tb)

