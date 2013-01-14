import cherrypy
from sqlalchemy.orm.exc import NoResultFound

import maki.views
import maki.scaffold
from maki import db
from maki.utils import log
from maki.db.utils import update_model, precautious_commit, clean_empty_metainfo



class Post(maki.scaffold.Controller):
    __views__ = [maki.views.post.HTML,
                 maki.views.post.JSON]
    required_fields = {'title', 'abstract', 'content',
                       'category', 'tags', 'format'}

    def _create_or_get_post_meta(self, Model, name):
        elem = db.ses.query(Model).filter_by(name=name).scalar()
        if elem is None:
            if not name.strip():
                raise Exception('Invalid name for %s' % Model.__name__)
            
            elem = Model(name=name)
        return elem

    
    def _create_or_get_tags(self, nametags):
        tags = []
        for ntag in nametags or []:
            tags.append(self._create_or_get_post_meta(db.models.Tag, ntag))
        return tags


    def _create_or_get_category(self, cname):
        return self._create_or_get_post_meta(db.models.Category, cname)


    def _get_format(self, fname):
        # this could "explode" but that's ok.
        return db.ses.query(db.models.PostFormat).filter_by(name=fname).one()

            
    def _get_post(self, query):
        try:
            return query.one()
        except NoResultFound:
            log('Unable to find post', 'ERROR', tb=True)
            return None


    def _update_post(self, post, fields):
        log('Updating post <%s>:%s' % (post, fields))
        # This two methods flush the sessions, because of the ".scalar" call.
        fields['tags'] = self._create_or_get_tags(fields['tags'])
        fields['category'] = self._create_or_get_category(fields['category'])
        fields['format'] = self._get_format(fields['format'])
        if post is None:  # new
            post = db.models.Post()
            post.author_id = cherrypy.session['uid']
            db.ses.add(post)
        if update_model(post, fields):
            message = precautious_commit(db.ses)  # None if everything went ok.
            if message is None:
                clean_empty_metainfo()
                return '{"id": %s, "slug": "%s"}' % (post.id, post.slug)
            else:
                raise Exception(message)
            
        else:
            raise Exception("Unable to update the post model.")

    
    def get_post_by_id(self, id):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(id=id))


    def get_post_by_slug(self, slug):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(slug=slug))


    def get_category_by_slug(self, slug):
        return db.ses.query(db.models.Category).filter_by(slug=slug).scalar()


    def create_post(self, **fields):
        return self._update_post(None, fields)

    
    def update_post(self, id,  **fields):
        post = self.get_post_by_id(id)
        if post is None:
            raise Exception("The post does not exist.")
        else:
            return self._update_post(post, fields)
