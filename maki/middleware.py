import cherrypy

import maki
import maki.i18n
import maki.utils
import maki.db.utils

def set_defaults(env):
    env['IN_DEVELOPMENT'] = maki.utils.in_development()
    env['STATIC'] = maki.APP.config['templates']['static_url']
    env['CATEGORIES'] = maki.db.utils.get_categories()
    env['LOCALE'] = cherrypy.response.i18n.clang
    env['LOCALE_SHOW_ALL'] = cherrypy.response.i18n.showall
    env['_'] = maki.i18n.gettext


def set_csstyles(env, csstyles):
    sheets = []
    static_url = env['STATIC']
    for sheet_path in csstyles:
        sheets.append('/'.join((static_url, 'css', sheet_path)))
    env['styles'] = sheets
    

