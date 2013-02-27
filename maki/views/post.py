import cherrypy
from cherrypy import tools

import maki.scaffold
import maki.feeds
from maki.utils import log



class HTML(maki.scaffold.View):

    @cherrypy.expose            
    @tools.mako(filename="post/list.mako")
    def index(self, cat, page='1'):
        """The index posts is filtered by a category.
        The unfiltered list is basically the front page.
        """
        lang = cherrypy.response.i18n.lang
        category = self.ctrl.get_category_by_slug(cat, lang)
        if category is None:
            raise cherrypy.NotFound()
        else:
            page, pages, posts = self.ctrl.public_posts(page, category=category)
            feed_url, feed_title = maki.feeds.url_and_title(category)
            breadcrumb = self._breadcrumb(category)
            return {'title': category.name, 
                    'category': category,
                    'posts': posts,
                    'pages': pages,
                    'currpage': page,
                    'breadcrumb': breadcrumb,
                    'feed_url': feed_url,
                    'feed_title': feed_title}


    @cherrypy.expose
    @tools.mako(filename="post/show.mako", csstyles=('post.css',))
    def default(self, slug=None):
        post = self.ctrl.get_post_by_slug(slug)
        if post is None or not post.public:
            raise cherrypy.NotFound()
        else:
            breadcrumb = self._breadcrumb(post.category, post)
            return {'post': post,
                    'title': post.title,
                    'breadcrumb': breadcrumb}


    def _breadcrumb(self, cat, post=None):
        if cherrypy.response.i18n.showall:
            caturl = '/post/?cat=%s&amp;l=%s' % (cat.slug, cat.lang.code)
        else:
            caturl = '/post/?cat=%s' % cat.slug
        bcrumb = [(caturl, cat.name), ]
        if post is not None:
            bcrumb.append(('/post/%s' % post.slug, post.title))
        return bcrumb
    



            
class JSON(maki.scaffold.View):
    __mime__ = 'application/json'

    def _model_to_dict(self, post):
        pdict ={'title': post.title,
                'abstract': post.abstract,
                'created': post.created_fmt,
                'content': post.content,
                'slug': post.slug,
                'category': post.category.name,
                'author': post.author.name,
                'format': post.format.name,
                'tags': [t.name for t in post.tags],
                'lang': post.lang.code,
                'id': post.id,
                'public': post.public}
        if post.modified:
            pdict['modfied'] =  post.modified.ctime()
        return pdict


    def _have_valid_fields(self, reqfields):
        changes = set(cherrypy.request.json)
        return reqfields == changes


    def _identify_action(self, action):
        if action == self.ctrl.CREATE_ACT:
            actionrstl = 'created'
            reqfields = self.ctrl.fields_to_create
            update_method = self.ctrl.create_post
        elif action == self.ctrl.EDIT_ACT:
            actionrstl = 'updated'
            reqfields = self.ctrl.fields_to_edit
            update_method = self.ctrl.update_post
        else:
            raise Exception('Invalid action to modify post: %s' % action)
        return actionrstl, reqfields, update_method


    def _modify_post(self, action, *args):
        actionrslt, reqfields, update_method = self._identify_action(action)
        if self._have_valid_fields(reqfields):
            try:
                post_id_slug= update_method(*args, **cherrypy.request.json)
            except Exception as exep:
                log('Unable to modify post', tb=True)
                cherrypy.response.status = 500
                return {actionrslt: False,
                        'message': str(exep)}
            else:
                return {actionrslt: True,
                        'message': post_id_slug}
        else:
            log('Trying to modify post, with invalid fields \n\t%s' % \
                cherrypy.request.json)
            cherrypy.response.status = 500
            return {actionrslt: False,
                    'message': 'Invalid fields'}

            
    @cherrypy.expose
    @tools.json_out()
    def default(self, identifier, by='id'):
        if by == 'id':
            post = self.ctrl.get_post_by_id(identifier) 
        elif by == 'slug':
            post = self.ctrl.get_post_by_slug(identifier)
        else:
            post = None            
        if post is None:
            raise cherrypy.NotFound(message="Unable to find any post")
        return self._model_to_dict(post)


    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('POST',))
    @tools.protect()
    def add(self):
        return self._modify_post(self.ctrl.CREATE_ACT)

    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('POST',))
    @tools.protect()
    def update(self, id_):
        return self._modify_post(self.ctrl.EDIT_ACT, id_)


    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('GET',))
    @tools.protect()
    def index(self, category=None, public=None, min_date=None, max_date=None):
        if public is not None:
            if public.isdigit() and int(public) > 1:
                public = True
            else:
                public = None
        return  [self._model_to_dict(post) for post in \
                 self.ctrl.get_posts(category, public, min_date, max_date)]

    @cherrypy.expose
    @tools.json_out()
    @tools.json_in()
    @tools.allow(methods=('POST',))
    @tools.protect()
    def visibility(self):
        response = {"visib-chg": False, "message": None}
        rjson = cherrypy.request.json
        if 'id' in rjson and 'public' in rjson:
            message = self.ctrl.change_visibility(rjson['id'], rjson['public'])
            if message is None:
                response['visib-chg'] = True
            else:
                cherrypy.response.status = 500
                response['message'] = message
        else:
            cherrypy.response.status = 500
            response['message'] = 'Missing required field.'
        return response


