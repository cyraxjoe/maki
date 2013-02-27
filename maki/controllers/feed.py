import datetime

import cherrypy as cp
import atomize

import maki.scaffold
import maki.views
import maki.feeds
from maki import db
from maki.utils import log


class Feed(maki.scaffold.Controller):
    __views__ = (maki.views.feed.XML, )


    def _get_blog_owner(self):
        return db.ses.query(db.models.User).first()


    def _posts_link_and_title(self, catslug, lang):
        query = db.ses.query(db.models.Post).filter_by(public=True)
        if catslug is not None:
            category = db.ses.query(db.models.Category)\
                       .filter_by(slug=catslug).scalar()
            if category is not None:
                query = query.filter_by(category=category)
        else:
            category = None
        if lang is not None:
            query = query.filter_by(lang=lang)
        url, title = maki.feeds.url_and_title(category)
        return query, url, title


    def atom_feed(self, catslug, lang=None):
        posts, self_link, title = self._posts_link_and_title(catslug, lang)
        log('link, title: %s %s' % (self_link, title))
        feed = atomize.Feed(title=title,
                            updated=datetime.datetime.now(),
                            guid=self_link,
                            author=self._get_blog_owner().vname,
                            self_link=self_link)
        for post in posts:
            url = cp.url('/post/' + post.slug)
            entry = atomize.Entry(title=post.title,
                                  guid=url,
                                  updated=post.modified, author=post.author.vname,
                                  links=[atomize.Link(url,
                                                      rel='alternate',
                                                      content_type='text/html',
                                                      hreflang=post.lang.code),],
                                  summary=atomize.Summary(post.abstract),
                                  categories=[atomize.Category(post.category.name),])
            feed.entries.append(entry)
        return b'\n'.join((b'<?xml version="1.0" encoding="utf-8"?>',
                           feed.feed_string()))

        



