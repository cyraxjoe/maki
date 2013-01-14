import cherrypy
from cherrypy import tools

import maki.scaffold


class JSON(maki.scaffold.View):
    __mime__ = 'application/json'

    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=['POST',])
    def default(self):
        if not cherrypy.request.json:
            raise cherrypy.HTTPError(400, 'Invalid JSON')
        else:
            fields = cherrypy.request.json
        missing_fields = self.ctrl.required_fields -  set(fields)
        if not missing_fields:
            if self.ctrl.authenticate(fields['user'], fields['passwd']):
                return {'authenticated': True}
            else:
                return {'authenticated': False}        
        else:
            raise cherrypy.HTTPError(400, 'Invalid required fields in JSON')
            
