import cherrypy

import maki.scaffold
import maki.i18n


class HTML(maki.scaffold.View):

    @cherrypy.expose
    def default(self, lang):
        self.ctrl.set_lang_in_session(lang)
        referer = cherrypy.request.headers.get('Referer', '/')
        if '/post/' in referer:
            referer = self._referer_for_post_index(referer)
        raise cherrypy.HTTPRedirect(referer, 303)
    
    
    def _referer_for_post_index(self, referer):
        #  avoid 404 in case that the user is viewing an specific category.
        if '?' in referer and 'lang=' not in referer:
            prevlangcode = maki.i18n.getlangcode()
            referer = '%s&lang=%s' % (referer, prevlangcode)
        return referer
