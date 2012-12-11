import cherrypy

from mako import exceptions
from mako.lookup import TemplateLookup

from maki.bindutils import bind_tool
from maki import middleware


class MakoHandler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""
    
    def __init__(self, template, next_handler):
        self.template = template
        self.next_handler = next_handler

    def _debug_render(self, env):
        try:
            return self.template.render(**env)
        except Exception:
            return exceptions.html_error_template().render()
    
    def __call__(self):
        env = self.next_handler()
        middleware.set_defaults(env)
        if cherrypy.config.get('environment') == 'production':
            return self.template.render(**env).decode()
        else:
            return self._debug_render(env).decode()


@bind_tool(name='mako', point='on_start_resource')
class MakoLoader(object):
    
    def __init__(self):
        self.lookups = {}
    
    def __call__(self, filename, directories, module_directory=None,
                 collection_size=-1):

        # Find the appropriate template lookup.
        key = (tuple(directories), module_directory)
        
        try:
            lookup = self.lookups[key]
        except KeyError:
            lookup = TemplateLookup(directories=directories,
                                    module_directory=module_directory,
                                    collection_size=collection_size,
                                    input_encoding='utf-8',
                                    output_encoding='utf-8')
            self.lookups[key] = lookup
            
        cherrypy.request.lookup = lookup
        
        # Replace the current handler.
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)

