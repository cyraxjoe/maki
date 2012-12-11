from cherrypy.process import plugins

import maki
import maki.db
from maki.bindutils import bind_plugin

@bind_plugin('dbengine')
class LoadDatabaseEngine(plugins.SimplePlugin):

    def start(self):
        maki.db.load_engine(maki.APP.config['sqlalchemy'])
        
