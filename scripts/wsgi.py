"""
WSGI Deploy script, most likely with mod_wsgi setting
the wsgi environment variable of "configuration" to the
appropiate cherrypy config file.
"""
import cherrypy

import maki
import maki.db


def application(environ, start_response):
    cherrypy.config.update(environ['configuration'])
    cherrypy.serving.request.wsgi_environ = environ
    cherrypy.tree.mount(cherrypy.Application(maki.ROOT, None), '',
                        environ['configuration'])
    maki.db.load_engine(maki.CONFIG('sqlalchemy'))
    return cherrypy.tree(environ, start_response)
