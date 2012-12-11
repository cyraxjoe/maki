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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship

Base = declarative_base()

tag_post_table = Table('tag_post', Base.metadata,
                       Column('tag_id', Integer, ForeignKey('tags.id')),
                       Column('user_id', Integer, ForeignKey('users.id')))

class Category(Base):
    __tablename__ = 'categories'

    id   = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    slug = Column(String(32))


class Comment(Base):
    __tablename__ = 'comments'
    
    id      = Column(Integer, primary_key=True)
    name    = Column(String(64))
    email   = Column(String(64))
    content = Column(Text)
    created = Column(DateTime, server_default=text('NOW()'))
    visible = Column(Boolean, server_default='True')


class CommentThread(Base):
    __tablename__ = 'cthreads'

    id         = Column(Integer, primary_key=True)
    post_id    = Column(Integer, ForeignKey('posts.id'))
    parent_id  = Column(Integer, ForeignKey('cthreads.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    comment    = relationship('Comment')
    children   = relationship('CommentThread')


class File(Base):
    __tablename__ = 'files'

    id     = Column(Integer, primary_key=True)
    name   = Column(String(255), nullable=False)
    note   = Column(String(128))
    format = Column(String(8))

    
class Tag(Base):
    __tablename__ = 'tags'

    id   = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    slug = Column(String(32), nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id          = Column(Integer, primary_key=True)
    title       = Column(String(64))
    abstract    = Column(String(400))
    content     = Column(Text)
    created     = Column(DateTime, server_default=text('NOW()'))
    modified    = Column(DateTime, server_default=text('NOW()'))
    author_id   = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    format_id   = Column(Integer, ForeignKey('post_formats.id'))
    slug        = Column(String(64))
    published   = Column(Boolean, server_default='False')
    tags        = relationship('Tag', secondary=tag_post_table, backref='posts')
    category    = relationship('Category')
    author      = relationship('User')
    format      = relationship('PostFormat')
    comments    = relationship('CommentThread')
    
    
class PostFormat(Base):
    __tablename__ = 'post_formats'
    
    id   = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)



class User(Base):
    __tablename__ = 'users'
    
    id     = Column(Integer, primary_key=True)
    name   = Column(String(32), unique=True, nullable=False)
    vname  = Column(String(64))
    email  = Column(String(64), nullable=False)
    passwd = Column(String(64), nullable=False)
    active = Column(Boolean, server_default='True')
