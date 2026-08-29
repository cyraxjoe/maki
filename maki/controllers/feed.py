import datetime
from xml.etree import ElementTree as ET

import cherrypy as cp

import maki.scaffold
import maki.views
import maki.feeds
from maki import db

ATOM_NS = "http://www.w3.org/2005/Atom"


def _rfc3339(date):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def _sub(parent, tag, text=None, **attrs):
    elem = ET.SubElement(parent, tag, attrs)
    if text is not None:
        elem.text = text
    return elem


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

    def _entry(self, feed, post):
        url = cp.url("/posts/{}".format(post.slug))
        entry = _sub(feed, "entry")
        _sub(entry, "title", post.title)
        _sub(entry, "id", url)
        _sub(entry, "published", _rfc3339(post.created))
        _sub(entry, "updated", _rfc3339(post.modified or post.created))
        author = _sub(entry, "author")
        _sub(author, "name", post.author.vname)
        _sub(
            entry,
            "link",
            href=url,
            rel="alternate",
            type="text/html",
            hreflang=post.lang.code,
        )
        if post.abstract:
            _sub(entry, "summary", post.abstract, type="text")
        _sub(entry, "category", term=post.category.name)
        return entry

    def atom_feed(self, catslug, lang=None):
        (posts, self_link, html_link, title) = self._posts_links_and_title(
            catslug, lang
        )
        ET.register_namespace("", ATOM_NS)
        feed = ET.Element("feed", xmlns=ATOM_NS)
        _sub(feed, "title", title)
        _sub(feed, "id", self_link)
        _sub(feed, "updated", _rfc3339(datetime.datetime.now()))
        author = _sub(feed, "author")
        _sub(author, "name", self._get_blog_owner().vname)
        _sub(feed, "icon", cp.url("/static/images/favicon.ico"))
        _sub(feed, "link", href=self_link, rel="self")
        _sub(feed, "link", href=html_link, rel="alternate", type="text/html")
        for post in posts:
            self._entry(feed, post)
        return ET.tostring(feed, encoding="utf-8", xml_declaration=True)
