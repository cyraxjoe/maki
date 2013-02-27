import cherrypy as cp

from maki.i18n import gettext as _

def url_and_title(category=None):
    url = ['/feed/']
    title = [_('Introspection'), ]
    if category is not None:
        url.append(category.slug)
        title.append(category.name)
    if cp.response.i18n.showall:
        url.append('?l=*')
    else:
        lang = cp.response.i18n.lang
        url.append('?l=' + lang.code)
        title.append(lang.name)
        return cp.url(''.join(url)), ' / '.join(title)
