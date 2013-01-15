import datetime
import hashlib

import bcrypt
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
    event
)
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr
)
from sqlalchemy.orm import  (
    relationship,
    validates
)
import maki.i18n
from maki.utils import slugify


class Base(object):
    @declared_attr
    def __tablename__(cls):
        raise NotImplementedError()
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

tag_post_table = Table('tag_post', Base.metadata,
                          Column('tag_id', Integer, ForeignKey('tags.id')),
                          Column('post_id', Integer, ForeignKey('posts.id')))


class PostMetainfo(object):
    name = Column(String(32), nullable=False, unique=True)
    slug = Column(String(32), nullable=False, unique=True)
    endure = Column(Boolean(), server_default='False')

    @declared_attr
    def __table_args__(self):
        return (UniqueConstraint('name', 'lang_id'),
                UniqueConstraint('slug', 'lang_id'))
    
    @declared_attr
    def lang_id(self):
        return Column(Integer, ForeignKey('languages.id'), nullable=False)
    
    @declared_attr
    def lang(self):
        return relationship('Language')


    
class Category(PostMetainfo, Base):
    __tablename__ = 'categories'


class Tag(PostMetainfo, Base):
    __tablename__ = 'tags'


class Language(Base):
    __tablename__ = 'languages'
    name = Column(String(48))
    code = Column(String(2))


class PostRevision(Base):
    __tablename__ = 'post_revisions'

    title       = Column(String(64), nullable=False)
    abstract    = Column(String(400))
    content     = Column(Text)
    modified    = Column(DateTime, onupdate=datetime.datetime.now, server_default=text('NOW()'))
    post_id     = Column(Integer, ForeignKey('posts.id'), nullable=False)


    
class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = (UniqueConstraint('slug', 'lang_id'),)

    slug        = Column(String(64), nullable=False)
    created     = Column(DateTime, server_default=text('NOW()'))
    public      = Column(Boolean, server_default='False', nullable=False)
    author_id   = Column(Integer, ForeignKey('users.id'), nullable=False)
    lang_id     = Column(Integer, ForeignKey('languages.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    format_id   = Column(Integer, ForeignKey('post_formats.id'), nullable=False)
    tags        = relationship('Tag', secondary=tag_post_table, backref='posts')
    category    = relationship('Category', backref='posts', order_by='Post.created')
    format      = relationship('PostFormat')
    lang        = relationship('Language')
    author      = relationship('User')
    revisions   = relationship('PostRevision', backref='post', uselist=True,
                               order_by='PostRevision.modified')

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
    __tablename__ = 'post_formats'
    
    name = Column(String(20), nullable=False, unique=True)



class User(Base):
    __tablename__ = 'users'
    
    name   = Column(String(32), unique=True, nullable=False)
    vname  = Column(String(64))
    email  = Column(String(64), nullable=False)
    passwd = Column(String(60), nullable=False)
    active = Column(Boolean, server_default='True')


    @validates('passwd')
    def validate_passwd(self, key, passwd):
        """Hash the passwd (sha256) then bcrypt-it and return."""
        try:
            hpasswd = hashlib.sha256(passwd.encode()).hexdigest()
        except AttributeError: # bytes
            hpasswd = hashlib.sha256(passwd).hexdigest()
        except Exception: # any other exception, raise.
            raise
        
        return bcrypt.hashpw(hpasswd, bcrypt.gensalt())


def set_slug_in_elem(elem, newvalue, oldvalue, initiator):
    elem.slug = slugify(newvalue)

event.listen(Tag.name, 'set', set_slug_in_elem)
event.listen(Category.name, 'set', set_slug_in_elem)
event.listen(Post.revisions, 'append',
             lambda post, revision, init:
                 setattr(post, 'slug',  slugify(revision.title)))
