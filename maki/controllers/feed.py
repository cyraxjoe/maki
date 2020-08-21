import datetime

import cherrypy as cp
import atomize

import maki.scaffold
import maki.views
import maki.feeds
from maki import db


class Feed(maki.scaffold.Controller):
    __views__ = (maki.views.feed.XML,)

    def _get_blog_owner(self):
        return db.ses.query(db.models.User).first()

    def _posts_links_and_title(self, catslug, lang):
        Post = db.models.Post
        Category = db.models.Category
        query = db.ses.query(Post).filter_by(public=True)
        alturl = None
        if catslug is not None:
            category = (
                db.ses.query(Category)
                .join(Post)
                .filter(Post.public == True)  # noqa: E712
                .filter(Category.slug == catslug)  # noqa: E712
            ).scalar()
            if category is None:
                raise cp.NotFound()
            else:
                query = query.filter_by(category=category)
                alturl = "/posts/?cat={}&amp;l={}".format(
                    category.slug, category.lang.code
                )
        else:
            category = None
        if lang is not None:
            query = query.filter_by(lang=lang)
            if alturl is None:
                alturl = "/?l={}".format(lang.code)
        else:
            alturl = "/"
        feedurl, title = maki.feeds.url_and_title(category, strict=True)
        query = query.order_by(Post.created.desc())
        return query, feedurl, cp.url(alturl), title

    def atom_feed(self, catslug, lang=None):
        (posts, self_link, html_link, title) = self._posts_links_and_title(
            catslug, lang
        )
        favicon_url = cp.url("/static/images/favicon.ico")
        feed = atomize.Feed(
            title=title,
            updated=datetime.datetime.now(),
            guid=self_link,
            author=self._get_blog_owner().vname,
            self_link=self_link,
            icon=atomize.Icon(favicon_url),
            links=[atomize.Link(html_link, rel="alternate", content_type="text/html")],
        )
        for post in posts:
            url = cp.url("/posts/{}".format(post.slug))
            entry = atomize.Entry(
                title=post.title,
                guid=url,
                published=atomize.Published(post.created),
                updated=post.modified,
                author=post.author.vname,
                links=[
                    atomize.Link(
                        url,
                        rel="alternate",
                        content_type="text/html",
                        hreflang=post.lang.code,
                    ),
                ],
                summary=atomize.Summary(post.abstract),
                categories=[atomize.Category(post.category.name),],
            )
            feed.entries.append(entry)
        return b"\n".join(
            (b'<?xml version="1.0" encoding="utf-8"?>', feed.feed_string())
        )
