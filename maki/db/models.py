import datetime
import hashlib

from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    UniqueConstraint,
    text,
    event,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, validates

import maki.constants
import maki.i18n
from maki.utils import slugify


class Base(object):
    @declared_attr
    def __tablename__(cls):
        raise NotImplementedError()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)

tag_post_table = Table(
    "tag_post",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
)
trans_post_table = Table(
    "trans_post_rel",
    Base.metadata,
    Column("from_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("to_id", Integer, ForeignKey("posts.id"), primary_key=True),
)
trans_tag_table = Table(
    "trans_tag_rel",
    Base.metadata,
    Column("from_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("to_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
trans_category_table = Table(
    "trans_category_rel",
    Base.metadata,
    Column("from_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("to_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


class Translatable(object):
    @declared_attr
    def lang_id(cls):
        return Column(Integer, ForeignKey("languages.id"), nullable=False)

    @declared_attr
    def lang(cls):
        return relationship("Language")

    @declared_attr
    def trans_of(cls):
        secondary = "trans_%s_rel" % cls.__name__.lower()
        return relationship(
            cls.__name__,
            secondary=secondary,
            primaryjoin="%s.id==%s.c.from_id" % (cls.__name__, secondary),
            secondaryjoin="%s.id==%s.c.to_id" % (cls.__name__, secondary),
            backref="translations",
        )


class PostMetainfo(Translatable):
    name = Column(String(32), nullable=False)
    slug = Column(String(32), nullable=False)
    endure = Column(Boolean(), server_default="False")

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint("name", "lang_id"),
            UniqueConstraint("slug", "lang_id"),
        )


class Category(PostMetainfo, Base):
    __tablename__ = "categories"
    posts = relationship("Post", order_by="Post.created.desc()")


class Tag(PostMetainfo, Base):
    __tablename__ = "tags"
    posts = relationship(
        "Post", secondary=tag_post_table, order_by="Post.created.desc()"
    )


class Language(Base):
    __tablename__ = "languages"
    name = Column(String(48))
    code = Column(String(2))


class PostRevision(Base):
    __tablename__ = "post_revisions"

    title = Column(String(64), nullable=False)
    abstract = Column(String(400))
    content = Column(Text)
    modified = Column(
        DateTime, onupdate=datetime.datetime.now, server_default=text("NOW()")
    )
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)


class Post(Translatable, Base):
    __tablename__ = "posts"

    slug = Column(String(64), nullable=False, unique=True)
    created = Column(DateTime, server_default=text("NOW()"))
    public = Column(Boolean, server_default="False", nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    format_id = Column(Integer, ForeignKey("post_formats.id"), nullable=False)
    tags = relationship("Tag", secondary=tag_post_table)
    category = relationship("Category")
    format = relationship("PostFormat")
    author = relationship("User")
    revisions = relationship(
        "PostRevision", backref="post", order_by="PostRevision.modified"
    )

    @property
    def crev(self):
        return self.revisions[-1]

    @property
    def title(self):
        return self.crev.title

    @property
    def abstract(self):
        return self.crev.abstract

    @property
    def content(self):
        return self.crev.content

    @property
    def modified(self):
        return self.crev.modified

    @property
    def created_fmt(self):
        return maki.i18n.fmt_date(self.created)

    @property
    def modified_fmt(self):
        return maki.i18n.fmt_date(self.modified)


class PostFormat(Base):
    __tablename__ = "post_formats"

    name = Column(String(20), nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"

    name = Column(String(32), unique=True, nullable=False)
    vname = Column(String(64))
    email = Column(String(64), nullable=False)
    ha1 = Column(String(32), nullable=False)
    active = Column(Boolean, server_default="True")

    @validates("ha1")
    def validates_ha1(self, key, passwd):
        if self.name is None:
            raise Exception("Set the name first")
        pack = ":".join([self.name, maki.constants.REALM, passwd])
        return hashlib.md5(pack.encode()).hexdigest()


def set_slug_in_elem(elem, newvalue, oldvalue, initiator):
    elem.slug = slugify(newvalue)


event.listen(Tag.name, "set", set_slug_in_elem)
event.listen(Category.name, "set", set_slug_in_elem)
event.listen(
    Post.revisions,
    "append",
    lambda post, revision, init: setattr(post, "slug", slugify(revision.title)),
)
