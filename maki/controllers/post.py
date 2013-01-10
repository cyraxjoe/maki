import cherrypy
from sqlalchemy.orm.exc import NoResultFound

from maki import db
from maki.utils import log
from maki.controllers import Controller
from maki.views.post import HTMLPost, JSONPost
from maki.db.utils import update_model, precautious_commit
from maki.forms import AddPostForm, EditPostForm


class Post(Controller):
    __views__ = [HTMLPost, JSONPost]


    def _get_post(self, query):
        try:
            return query.one()
        except NoResultFound as err:
            cherrypy.log.error(str(err))
            return None

    def get_add_form(self):
        form = AddPostForm()
        # set the valid tags, categories and formats.
        return form
                        

    def get_edit_form(self):
        form = EditPostForm()
        # set the valid tags, categories and formats.
        return form

        
    def get_post_by_id(self, id):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(id=id))

    def get_post_by_slug(self, slug):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(slug=slug))

    def update_post(self, id, autotag=False, **fields):
        log(fields)
        post = self.get_post_by_id(id)
        if post is None:
            return "The post does not exists."
        if autotag:
            fields['tags'] = self._create_or_get_tags(fields['tags'])
        if update_model(post, fields):
            return precautious_commit(db.ses)  # None if everything went ok.
        else:
            return "Unable to update the post model."


    def _create_or_get_tags(self, nametags):
        tags = []
        Tag = db.models.Tag
        for ntag in nametags or []:
            tag = db.ses.query(Tag).filter_by(name=ntag).scalar()
            if tag is None:
                tag = Tag(name=ntag)
            tags.append(tag)
        return tags

            
