import cherrypy

import maki.scaffold

class HTML(maki.scaffold.View):

    @cherrypy.expose
    def default(self, lang):
        self.ctrl.set_lang_in_session(lang)
        referer = cherrypy.request.headers.get('Referer', '/')
        raise cherrypy.HTTPRedirect(referer, 303)
    
    
