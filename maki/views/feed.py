import cherrypy as cp

import maki.scaffold
from maki.utils import log

class XML(maki.scaffold.View):

    @cp.expose
    def default(self, category=None):
        log('category is %s' % category)
        cp.response.headers['Content-type'] = 'application/atom+xml'
        if not cp.request.lang:
            return self.ctrl.atom_feed(category)
        else:
            return self.ctrl.atom_feed(category, cp.response.i18n.lang)
