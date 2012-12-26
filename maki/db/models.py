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
    text
)
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr
)
from sqlalchemy.orm import  (
    relationship,
    validates
)


class Base(object):
    @declared_attr
    def __tablename__(cls):
        raise NotImplementedError()
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

tag_post_table = Table('tag_post', Base.metadata,
                       Column('tag_id', Integer, ForeignKey('tags.id')),
                       Column('post_id', Integer, ForeignKey('posts.id')))

class Category(Base):
    __tablename__ = 'categories'

    name = Column(String(32), nullable=False)
    slug = Column(String(32))


class Comment(Base):
    __tablename__ = 'comments'
    
    author_name    = Column(String(64))
    author_email   = Column(String(64))
    content = Column(Text)
    created = Column(DateTime, server_default=text('NOW()'))
    visible = Column(Boolean, server_default='True')


class CommentThread(Base):
    __tablename__ = 'cthreads'

    post_id    = Column(Integer, ForeignKey('posts.id'))
    parent_id  = Column(Integer, ForeignKey('cthreads.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    comment    = relationship('Comment')
    children   = relationship('CommentThread')
    post       = relationship('Post')


class File(Base):
    __tablename__ = 'files'

    name   = Column(String(255), nullable=False)
    note   = Column(String(128))
    format = Column(String(8))

    
class Tag(Base):
    __tablename__ = 'tags'

    name = Column(String(32), nullable=False)
    slug = Column(String(32), nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    title       = Column(String(64))
    abstract    = Column(String(400))
    content     = Column(Text)
    created     = Column(DateTime, server_default=text('NOW()'))
    slug        = Column(String(64))
    public      = Column(Boolean, server_default='False')
    modified    = Column(DateTime, onupdate=datetime.datetime.now)
    author_id   = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    format_id   = Column(Integer, ForeignKey('post_formats.id'))
    tags        = relationship('Tag', secondary=tag_post_table, backref='posts')
    category    = relationship('Category')
    author      = relationship('User')
    format      = relationship('PostFormat')
    comments    = relationship('CommentThread')

    @property
    def comment_count(self):
        return len(self.comments)
    
    
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




