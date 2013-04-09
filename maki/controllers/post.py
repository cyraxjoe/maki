import math
import json

import cherrypy

import maki.constants
import maki.views
import maki.scaffold
from maki import db
from maki.utils import log
from maki.db.utils import (
    update_model,
    precautious_commit,
    clean_empty_metainfo
)



class Post(maki.scaffold.Controller):
    __views__ = [maki.views.post.HTML,  maki.views.post.JSON]
    CREATE_ACT = 'create'
    EDIT_ACT = 'edit'
    fields_to_create = {'title', 'abstract', 'content',
                       'category', 'tags', 'format', 'lang'}
    fields_to_edit = fields_to_create - {'lang',}
    plimit = maki.constants.POSTS_PER_PAGE


    def _create_or_get_post_meta(self, Model, name, lang):
        log('Searching for %s with name %s and lang %s' % (Model, name, lang.name))
        elem = db.ses.query(Model)\
               .filter_by(name=name).filter_by(lang=lang).scalar()
        if elem is None:
            if not name.strip():
                raise Exception('Invalid name for %s' % Model.__name__)
            elem = Model(name=name, lang=lang)
            log('NOT FOUND!! Creating a new one')
        return elem

    
    def _create_or_get_tags(self, nametags, lang):
        tags = []
        for ntag in nametags or []:
            tags.append(self._create_or_get_post_meta(db.models.Tag, ntag, lang))
        return tags


    def _create_or_get_category(self, cname, lang):
        return self._create_or_get_post_meta(db.models.Category, cname, lang)

            
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


    def _fields_to_db_models(self, fields, lang):
        # This methods flush the sessions, because of the ".scalar" call.
        fields['tags'] = self._create_or_get_tags(fields['tags'], lang)
        fields['category'] = \
                         self._create_or_get_category(fields['category'], lang)
        fields['format'] = self._get_format(fields['format'])
        return fields
        

    def _update_post_model(self, post, fields, isnew=False):
        log('Updating (isnew?: %s) post <%s>:%s' % (isnew, post, fields))
        if isnew:
            lang = fields['lang'] = self._get_lang(fields['lang'])
            post.author_id = db.ses.query(db.models.User)\
                             .filter_by(name=cherrypy.request.login).one().id
        else:
            lang = post.lang
        fields = self._fields_to_db_models(fields, lang)
        # add the post to the session, even if this is not new, because
        # of the .scalar call in `_fields_to_db_models`
        db.ses.add(post) 
        revision = db.models.PostRevision(title=fields.pop('title'),
                                          abstract=fields.pop('abstract'),
                                          content=fields.pop('content'))
        post.revisions.append(revision)
        if update_model(post, fields):
            message = precautious_commit(db.ses)  # None if everything went ok.
            if message is None:
                clean_empty_metainfo()
                return json.dumps({'id': post.id,
                                   'slug': post.slug,
                                   'lang': post.lang.code,
                                   'public': post.public})
            else:
                raise Exception(message)
        else:
            raise Exception("Unable to update the post model.")


    def change_visibility(self, postid, public):
        post = self.get_post_by_id(postid)
        if post is None:
            raise Exception("The post does not exist.")
        else:
            post.public = public
            return precautious_commit(db.ses)


    def create_post(self, **fields):
        return self._update_post_model(db.models.Post(), fields, isnew=True)

    
    def get_post_by_id(self, id):
        return db.ses.query(db.models.Post).filter_by(id=id).scalar()


    def get_post_by_slug(self, slug):
        return db.ses.query(db.models.Post).filter_by(slug=slug).scalar()


    def get_posts(self, catname, public, min_date, max_date):
        # dates limits are not yet implented
        query = db.ses.query(db.models.Post)
        if catname is not None:
            category = self.get_category_by_name()
            query = query.filter_by(category_id=category)
        if isinstance(public, bool):
            query = query.filter_by(public=public)
        return query.order_by(db.models.Post.created)


    def _public_posts_query(self, **filters):
        locale = cherrypy.response.i18n
        Post = db.models.Post
        posts = db.ses.query(Post).filter_by(public=True, **filters)
        posts = posts.order_by(Post.created.desc())
        if not locale.showall:
            posts = posts.filter_by(lang=locale.lang)
        return posts


    def public_posts(self, page, **filters):
        """Return a tuple (real_page, page_count, posts_in_page)"""
        if page.isdigit():
            page = int(page)
        else:
            page = 1
        pquery = self._public_posts_query(**filters)
        page_count = math.ceil(pquery.count() / self.plimit) + 1
        offset = (page - 1) * self.plimit
        return page, page_count, pquery.offset(offset).limit(self.plimit)
        

    def get_category_by_slug(self, slug, preflang, strict=False):
        category =  db.ses.query(db.models.Category)\
                   .filter_by(slug=slug)\
                   .filter_by(lang=preflang).scalar()
        if category is None and not strict: 
            return db.ses.query(db.models.Category)\
                   .filter_by(slug=slug).first()
        else:
            return category

    
    def get_category_by_name(self, name):
        return db.ses.query(db.models.Category).filter_by(name=name).scalar()

    
    def update_post(self, id,  **fields):
        post = self.get_post_by_id(id)
        if post is None:
            raise Exception("The post does not exist.")
        else:
            return self._update_post_model(post, fields)


class Posts(Post):
    __views__ = [maki.views.post.PostsHTML,]
