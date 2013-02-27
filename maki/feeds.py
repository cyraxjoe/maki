import cherrypy as cp

from maki.i18n import gettext as _


def url_and_title(category=None):
    url = ['/feed/']
    title = [_('Introspection'), ]
    #seslang = cp.session.get(maki.i18n.SES_KEY)
    if category is not None:
        url.append(category.slug)
        title.append(category.name)
    if  cp.request.lang or \
            not cp.response.i18n.showall:
        lang = cp.response.i18n.lang
        url.append('?l=' + lang.code)
        title.append(lang.name)
    return cp.url(''.join(url)), ' / '.join(title)
