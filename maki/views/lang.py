import cherrypy

import maki.scaffold
import maki.i18n


class HTML(maki.scaffold.View):

    @cherrypy.expose
    def default(self, lang):
        self.ctrl.set_lang_in_cookie(lang)
        referer = cherrypy.request.headers.get('Referer', '/')
        if '?' in referer:
            referer = self._ref_without_lang(referer)
        raise cherrypy.HTTPRedirect(referer, 303)


    def _ref_without_lang(self, referer):
        newqs = []
        qs = referer.split('?', 1)[-1]
        for elem in qs.split('&'):
            if 'l=' not in elem:
                newqs.append(elem)
        url  = referer[:referer.index('?')]
        return '?'.join([url, '&'.join(newqs)])

    
