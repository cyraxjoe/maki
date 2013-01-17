import cherrypy

import maki.scaffold
import maki.views
import maki.i18n
from maki.utils import log

class Lang(maki.scaffold.Controller):
    __views__ = (maki.views.lang.HTML,)


    def set_lang_in_session(self, lang):
        if lang  == maki.i18n.ANY_LANG:
            cherrypy.session[maki.i18n.SES_KEY] = maki.i18n.ANY_LANG
        else:
            if lang in maki.i18n.AVAILABLE_LANGS:
                cherrypy.session[maki.i18n.SES_KEY] = lang
            else:
                log('Trying to set invalid lang %s' % lang,
                    'ERROR')
    
