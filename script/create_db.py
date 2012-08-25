import sys

from cherrypy.lib import reprconf
from maki import db


def create_db(conf):
    config = reprconf.Config(conf)
    db.load_engine(config['sqlalchemy'])
    db.models.Base.metadata.create_all(bind=db.session.bind)
    
if __name__ == '__main__':
    try:
        config = sys.argv[1]
    except IndexError:
        print("Invalid arguments", file=sys.stderr)
    else:
        create_db(config)
        db.session.commit()
        
