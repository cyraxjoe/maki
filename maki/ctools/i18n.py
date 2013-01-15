from collections import namedtuple

import cherrypy

import maki.i18n
from maki import db
from maki.utils import log


Locale = namedtuple('Locale', ('langs', 'clang'))


def choose_lang(langs):
    for langcode in langs:
        if langcode in maki.i18n.AVAILABLE_LANGS:
            log(langcode)
            olang = db.ses.query(db.models.Language)\
                    .filter_by(code=langcode).one()
            return olang


def get_lang(default='en'):
    langs = [x.value.split('-')[0] for x in
             cherrypy.request.headers.elements('Accept-Language')]
    seslang = cherrypy.session.get('_lang_')
    if seslang is not None: #  the preffered language code is in the session.
        langs.insert(0, seslang)
    langs.append(default)
    cherrypy.response.i18n = \
                   Locale(langs=langs, clang=choose_lang(langs))
    log(cherrypy.response.i18n)


def set_lang():
    headers = cherrypy.response.headers
    if 'Content-Language' not in headers:
        headers['Content-Language'] = cherrypy.response.i18n.clang.code


class I18nTool(cherrypy.Tool):


    def __init__(self):
        self._name = 'I18nTool'
        self._point = 'before_handler'
        self.callable = get_lang
        # Make sure, session tool (priority 50) is loaded before
        self._priority = 100


    def _setup(self):
        c = cherrypy.request.config
        # if is an static file , do not use i18n.
        if c.get('tools.staticdir.on', False) or \
           c.get('tools.staticfile.on', False):
            return
        log('settin i18n')
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('before_finalize', set_lang)


cherrypy.tools.i18n = I18nTool()

