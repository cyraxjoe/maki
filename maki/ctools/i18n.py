from collections import namedtuple

import cherrypy
from sqlalchemy.exc import InvalidRequestError

import maki.i18n
from maki import db
#from maki.utils import log


Locale = namedtuple('Locale', ('lang', 'showall'))


def choose_lang(langs, default='en'):
    langs.append(default)
    for langcode in langs:
        if langcode in maki.i18n.AVAILABLE_LANGS:
            olang = db.ses.query(db.models.Language)\
                    .filter_by(code=langcode).one()
            return olang


def get_lang():        
    langs = [x.value.split('-')[0].lower() for x in
             cherrypy.request.headers.elements('Accept-Language')]
    seslang = cherrypy.session.get(maki.i18n.SES_KEY)
    locargs = {'showall': False}        
    if seslang is not None:
        if seslang == maki.i18n.ANY_LANG: 
            locargs['showall'] = True
        else:
            langs.insert(0, seslang)
     # top priority if the lang is in the request
    if hasattr(cherrypy.request, 'lang') and \
           cherrypy.request.lang is not None:
        langs.insert(0, cherrypy.request.lang)
    locargs['lang'] = choose_lang(langs)
    cherrypy.response.i18n = Locale(**locargs)


def set_lang():
    headers = cherrypy.response.headers
    if 'Content-Language' not in headers:
        try:
            headers['Content-Language'] = cherrypy.response.i18n.lang.code
        except InvalidRequestError:  # rollback in the sqlsession.
            headers['Content-Language'] = maki.i18n.getlang_from_config()
        except AttributeError:  # in case that the request wasn't i18n'ted
            pass
        

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
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('before_finalize', set_lang)


def set_lang_in_request():
    cherrypy.request.lang = cherrypy.request.params.pop('l', None)

cherrypy.tools.i18n = I18nTool()
cherrypy.tools.i18n_request = cherrypy.Tool('before_handler', set_lang_in_request)

