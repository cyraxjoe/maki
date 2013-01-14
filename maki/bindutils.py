import types
import cherrypy
    
def bind_tool(name, point, priority=50):
    def set_tool(tool):
        if isinstance(tool, types.FunctionType):
            setattr(cherrypy.tools, name,
                    cherrypy.Tool(point, tool, priority=priority))
        else:
            setattr(cherrypy.tools, name,
                    cherrypy.Tool(point, tool(), priority=priority))
    return set_tool


def bind_plugin(name):
    def set_plugin(cls):
        plugin = cls(cherrypy.engine)
        setattr(cherrypy.engine, name, plugin)
        plugin.subscribe()
        return cls
    return set_plugin
