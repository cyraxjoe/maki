import cherrypy

from maki import db
from maki.controllers import Controller
from maki.views.post import HTMLPost, JSONPost



class Post(Controller):
    __views__ = [HTMLPost, JSONPost]
    
    def get_post(self, identifier):
        cherrypy.log.error(identifier)
        if identifier.isdigit():
            return self.get_post_by_id(identifier)
        else:
            return self.get_post_by_slug(identifier)
        
    def get_post_by_id(self, id):
        return db.ses.query(db.models.Post).filter_by(id=id).one()
        

    def get_post_by_slug(self, slug):
        return db.ses.query(db.models.Post).filter_by(slug=slug).one()

