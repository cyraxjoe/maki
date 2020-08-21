import cherrypy

import maki.scaffold
import maki.views
import maki.i18n
from maki.utils import log


class Lang(maki.scaffold.Controller):
    __views__ = (maki.views.lang.HTML,)

    def set_lang_in_cookie(self, lang):
        response = cherrypy.response
        if lang == maki.i18n.ANY_LANG:
            response.cookie[maki.i18n.CKEY] = maki.i18n.ANY_LANG
        else:
            if lang in maki.i18n.AVAILABLE_LANGS:
                response.cookie[maki.i18n.CKEY] = lang
            else:
                log("Trying to set invalid lang %s" % lang, "ERROR")
                return
        response.cookie[maki.i18n.CKEY]["path"] = "/"
        response.cookie[maki.i18n.CKEY]["expires"] = 3600
