import cherrypy as cp

import maki.scaffold


class XML(maki.scaffold.View):

    @cp.expose
    def default(self, category=None):
        cp.response.headers['Content-type'] = 'application/atom+xml'
        if not cp.request.lang:
            return self.ctrl.atom_feed(category)
        else:
            return self.ctrl.atom_feed(category, cp.response.i18n.lang)
