import locale

import cherrypy

import maki.utils

AVAILABLE_LANGS = ('en', 'es')
ANY_LANG = 'ANY'
CKEY = '_lang_'

STRINGS = \
{ '_DATE_FORMAT_': {'en': '%b %e, %Y',
                    'es': '%e %b, %Y'},
  'Introspection':
       {'es': 'Introspección'},
 'ntrospection':
        {'es': 'ntrospección'},
 'Categories':
        {'es': 'Categorías'},
 'Who am I?':
        {'es': '¿Quién soy yo?'},
 'just another software developer from Monterrey, Mexico': 
        {'es': 'solo un desarrollador de software más de Monterrey, México'},
 'More about me':
        {'es': 'Más sobre mí'},
 'This work is licensed under a': 
        {'es': 'Este obra está bajo una'},
 'http://creativecommons.org/licenses/by/3.0/deed.en_US':
        {'es': 'http://creativecommons.org/licenses/by/3.0/deed.es'},
 'Creative Commons Attribution 3.0 Unported License':
        {'es': 'Licencia Creative Commons Atribución 3.0 Unported',},
  'The visibility of the posts is filtered by the selected option':
       {'es': 'La visibilidad de los posts es filtrada por la opción seleccionada'},
  'Any': {'es': 'Todos'},
  'what is this?': {'es': '¿Qué es esto?'},
  'Home': {'es': 'Inicio',},
  'Made with cherrypy': {'es': 'Hecho con cherrypy'},
  'Proudly hosted at webfaction': {'es': 'Orgullosamente hospedado en webfaction'}
 }


def getlang_from_config():
    try:
        return maki.CONFIG('i18n')['default']
    except KeyError:
        return cherrypy.config['i18n']['default']

    
def getlangcode():
    try:
        return cherrypy.response.i18n.lang.code
    except AttributeError:
        maki.utils.log('Unable to get i18n from cherrypy.response.')
        return getlang_from_config()


def gettext(string, langcode=None):
    if langcode is None:
        langcode = getlangcode()
    if string in STRINGS:
        if langcode in STRINGS[string]:
            return STRINGS[string][langcode]
        return string
    else:
        return string


def full_locale(langcode=None):
    if langcode is None:
        langcode = getlangcode()
    if langcode  == 'en':  # US
        return 'en_US.UTF-8' 
    elif langcode == 'es':  # MX
        return 'es_MX.UTF-8'
    else:
        return locale.normalize(langcode) 
        

def fmt_date(date, langcode=None):
    if langcode is None:
        langcode = getlangcode()
    dformat = gettext('_DATE_FORMAT_', langcode)
    original_loc = locale.getlocale()
    try:
        locale.setlocale(locale.LC_ALL, full_locale(langcode))
        return date.strftime(dformat)
    finally:
        locale.setlocale(locale.LC_ALL, original_loc)
        
