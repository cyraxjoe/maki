import os

import cherrypy
from cherrypy import tools

local_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))

from .ctools import makotemplates




def set_static_files(root):
    static_config = {'section': '/static',
                     'dir': os.path.join(local_dir, 'static'),
                     'match': r'\.(css|gif|html?|ico|jpe?g|js|png|swf|xml)$',
                     }
    favicon_path = os.path.join(local_dir, 'static', 'favicon.ico')
    
    root.favicon_ico = tools.staticfile.handler(filename=favicon_path)
    root.static = tools.staticdir.handler(**static_config)


def set_tools():
    makotool = makotemplates.MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', makotool)
    

def get_root():
    from .views import index, post
    root = index.Index()
    root.post = post.Post()

    set_static_files(root)
    return root

set_tools()
