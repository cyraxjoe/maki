"""
Error handling.

Notice how the fallback error behaves, all the unexpected errors
those that the user do not rise directly are managed in the `fallback_error`,
this method first try to use the default handler of 500, if other error
raises from the handler of the 500, then use the default template and notify,
if the notification fails, then an ugly page of cherrypy gets returned,
which is ok because we already try two times to recover from the error
and notify, so if the error is in the notification then let the user notify us
about the error.
"""
import warnings

import maki
from maki.utils import in_development
from maki.utils import makoutils
from maki.utils import mail


def _error(template, status, message, traceback, version, prodhook=None):
    """
    Render the error page with the appropiate parameters, notice that
    the notified parameters hast 3 relevant states True/False/None,
    and is a required parameter.
    """
    if in_development():            
        params = {'status': status,
                  'message': message,
                  'traceback': traceback,
                  'version': version,
                  'notified': None}
    else:
        params =  {'message': message,
                   'status': status}        
        if callable(prodhook):
            params['notified'] = prodhook()
        else:
            params['notified'] = None
    params['STATIC'] = maki.CONFIG('templates')['static_url']
    params['_'] = lambda s: s
    return makoutils.direct_render(template, params)


def error_404(status, message='', traceback='', version=''):
    template =  'errors/404.mako'
    # NOTICE: We are using "decode", because cherrypy break with bytes
    # strings, this is probably a bug in cherrypy, because the 500
    # require bytes and almost any other cherrypy handler. 
    return _error(template, status, message, traceback, version).decode()


def error_500(status, message='', traceback='', version=''):
    template = 'errors/500.mako'
    params = [template, status, message, traceback, version, ]
    def notify():
        body = "<h3>Mensage</h3><p>%s</p><br/><h3>Traceback</h3><pre>%s</pre>" % \
               (message, traceback)
        subject = 'Error in Maki blog [%s]' % status        
        return mail.send(sender, admin, subject,  body)
    try:
        admin, sender = mail.get_admin_addresses()
        params.append(notify)
    except KeyError:
        params.append(lambda: False)
        warnings.warn('Unable to get email address to notify error')
    return _error(*params).decode()


