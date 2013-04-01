import re
import pprint

import cherrypy as cp
import unidecode



def log(message, cntx='DEBUG', tb=False):
    if isinstance(message, str):
        cp.log.error(message, context=cntx, traceback=tb)
    else:
        cp.log.error(pprint.pformat(message), context=cntx, traceback=tb)

def in_development():
    return cp.config.get('environment') not in ('production', 'embedded')


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+','-', text)

