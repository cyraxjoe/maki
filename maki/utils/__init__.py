import re
import pprint

import cherrypy
import unidecode

def log(message, cntx='DEBUG', tb=False):
    if isinstance(message, str):
        cherrypy.log.error(message, context=cntx,
                           traceback=tb)
    else:
        cherrypy.log.error(pprint.pformat(message), context=cntx,
                           traceback=tb)

def in_development():
    return cherrypy.config.get('environment') != 'production'


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+','-', text)
