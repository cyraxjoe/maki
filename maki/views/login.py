import cherrypy
from cherrypy import tools

from maki.forms import (
    LoginForm,
    CompatParams
)
from maki.views import View


class JSONLogin(View):
    __mime__ = 'application/json'

    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=['POST',])
    def default(self):
        if cherrypy.request.json:
            form = LoginForm(CompatParams(cherrypy.request.json))
        else:
            raise cherrypy.HTTPError(400, 'Invalid JSON')
        if form.validate():
            if self.ctrl.authenticate(form.user.data, form.passwd.data):
                return {'authenticated': True}
            else:
                return {'authenticated': False}
        else:
            raise cherrypy.HTTPError(400, 'Invalid JSON')
            
