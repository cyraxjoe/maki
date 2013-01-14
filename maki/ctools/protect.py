import cherrypy

import maki.utils
from maki.bindutils import bind_tool

@bind_tool(name="protect", point="before_handler", priority=60)
def protect():
    uid = cherrypy.session.get('uid')
    if uid is None:
        maki.utils.log("User not logged in. Then I'm a teapot.")
        raise cherrypy.HTTPError(418, message="I'm a teapot.")

