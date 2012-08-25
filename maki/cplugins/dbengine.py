import maki
import maki.db

from cherrypy.process import plugins
from maki.bindutils import bind_plugin

@bind_plugin('dbengine')
class LoadDatabaseEngine(plugins.SimplePlugin):

    def start(self):
        print('loading engine')
        maki.db.load_engine(maki.app.config['sqlalchemy'])
        
