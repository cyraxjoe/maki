from sqlalchemy.orm.exc import NoResultFound

import maki.views
import maki.scaffold
from maki import db
from maki.utils import log
from maki.db.utils import update_model, precautious_commit



class Post(maki.scaffold.Controller):
    __views__ = [maki.views.post.HTML,
                 maki.views.post.JSON]
    required_fields = {'title', 'abstract', 'content',
                       'category', 'format', 'tags'}

    def _create_or_get_tags(self, nametags):
        tags = []
        Tag = db.models.Tag
        for ntag in nametags or []:
            tag = db.ses.query(Tag).filter_by(name=ntag).scalar()
            if tag is None:
                tag = Tag(name=ntag)
            tags.append(tag)
        return tags

            
    def _get_post(self, query):
        try:
            return query.one()
        except NoResultFound:
            log('Unable to find post', 'ERROR', tb=True)
            return None

        
    def get_post_by_id(self, id):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(id=id))


    def get_post_by_slug(self, slug):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(slug=slug))


    def get_category_by_slug(self, slug):
        return db.ses.query(db.models.Category).filter_by(slug=slug).scalar()

    
    def update_post(self, id, autotag=False, **fields):
        log(fields)
        post = self.get_post_by_id(id)
        if post is None:
            return "The post does not exist."
        if autotag:
            fields['tags'] = self._create_or_get_tags(fields['tags'])
        if update_model(post, fields):
            return precautious_commit(db.ses)  # None if everything went ok.
        else:
            return "Unable to update the post model."

