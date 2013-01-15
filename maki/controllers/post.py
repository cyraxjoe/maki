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
                       'category', 'tags', 'format',
                       'lang'}

    def _create_or_get_post_meta(self, Model, name, lang):
        elem = db.ses.query(Model)\
               .filter_by(name=name).filter_by(lang=lang).scalar()
        if elem is None:
            if not name.strip():
                raise Exception('Invalid name for %s' % Model.__name__)
            elem = Model(name=name, lang=lang)
        return elem

    
    def _create_or_get_tags(self, nametags, lang):
        tags = []
        for ntag in nametags or []:
            tags.append(self._create_or_get_post_meta(db.models.Tag, ntag, lang))
        return tags


    def _create_or_get_category(self, cname, lang):
        return self._create_or_get_post_meta(db.models.Category, cname, lang)


            
    def _get_post(self, query):
        try:
            return query.one()
        except NoResultFound:
            log('Unable to find post', 'ERROR', tb=True)
            return None


    def _update_post(self, post, fields):
        log('Updating post <%s>:%s' % (post, fields))
        # This methods flush the sessions, because of the ".scalar" call.
        lang = fields['lang'] = self._get_lang(fields['lang'])
        fields['tags'] = self._create_or_get_tags(fields['tags'], lang)
        fields['category'] = \
                         self._create_or_get_category(fields['category'], lang)
        fields['format'] = self._get_format(fields['format'])

        log(fields)
        revision = db.models.PostRevision(title=fields.pop('title'),
                                          abstract=fields.pop('abstract'),
                                          content=fields.pop('content'))
        if post is None:  # new
            post = db.models.Post()
            post.author_id = cherrypy.session['uid']
            db.ses.add(post)
        if update_model(post, fields):
            post.revisions.append(revision)
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

    def get_post_by_slug(self, slug, lang):
        return self._get_post(db.ses.query(db.models.Post)\
                              .filter_by(slug=slug)\
                              .filter_by(lang=lang))

    def get_category_by_slug(self, slug, lang):
        return db.ses.query(db.models.Category)\
               .filter_by(slug=slug)\
               .filter_by(lang=lang).scalar()


    def _get_format(self, fname):
        # this could "explode" but that's ok.
        return db.ses.query(db.models.PostFormat).filter_by(name=fname).one()


    def _get_lang(self, langcode):
        lang = db.ses.query(db.models.Language)\
               .filter_by(code=langcode).scalar()
        if lang is None:
            raise Exception('Unknown langcode %s' % langcode)
        else:
            return lang

    def create_post(self, **fields):
        return self._update_post(None, fields)

    
    def update_post(self, id,  **fields):
        post = self.get_post_by_id(id)
        if post is None:
            raise Exception("The post does not exist.")
        else:
            return self._update_post(post, fields)
