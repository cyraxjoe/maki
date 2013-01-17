from collections import namedtuple

import cherrypy

import maki.i18n
from maki import db
from maki.utils import log


Locale = namedtuple('Locale', ('lang', 'showall'))


def choose_lang(langs):
    for langcode in langs:
        if langcode in maki.i18n.AVAILABLE_LANGS:
            log(langcode)
            olang = db.ses.query(db.models.Language)\
                    .filter_by(code=langcode).one()
            return olang


def get_lang(default='en'):
    langs = [x.value.split('-')[0].lower() for x in
             cherrypy.request.headers.elements('Accept-Language')]
    langs.append(default)
    seslang = cherrypy.session.get(maki.i18n.SES_KEY)
    locargs = {'showall': False}        
    if seslang is not None:
        if seslang == maki.i18n.ANY_LANG: 
            locargs['showall'] = True
        else:
            langs.insert(0, seslang)
    locargs['lang'] = choose_lang(langs)
    cherrypy.response.i18n = Locale(**locargs)


def set_lang():
    headers = cherrypy.response.headers
    if 'Content-Language' not in headers:
        headers['Content-Language'] = cherrypy.response.i18n.lang.code


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

