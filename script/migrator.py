import json
import sys
from datetime import datetime

from cherrypy.lib import reprconf

from maki import db

SPANISH_ID = 1
RST_FMT = 2

def _build_elem(name, Model, cache):
    try:
        return cache[name]
    except KeyError:
        elem = Model(name=name, lang_id=SPANISH_ID)
        cache[name] = elem
        return elem


tag_cache = {}
def build_tag(tagname, tag_cache=tag_cache):
    return _build_elem(tagname, db.models.Tag, tag_cache)

cat_cache = {}
def build_category(catname, cat_cache=cat_cache):
    return _build_elem(catname, db.models.Category, cat_cache)
    


def load_posts(json_posts):
    posts = reversed(json.load(json_posts))
    # new : old,...
    common_fields = {'slug': 'url',
                     'public': 'published',
                     'author_id': 'author_id'}
    cntfields =  ['title', 'abstract', 'content']
    for post in posts:
        revision = {f: post[f] for f in cntfields}
        pfields = {new: post[old] for new, old in common_fields.items()}
        pfields['revisions'] = [db.models.PostRevision(**revision), ]
        pfields['lang_id'] = SPANISH_ID
        pfields['created'] = datetime.fromtimestamp(post['created'])
        pfields['tags'] = [build_tag(tag) for tag in post['tags']]
        pfields['category'] = build_category(post['category'])
        pfields['format_id'] = RST_FMT
        db.ses.add(db.models.Post(**pfields))
    db.ses.commit()


if __name__ == '__main__':
    config = reprconf.Config(sys.argv[1])
    db.load_engine(config['sqlalchemy'])
    with open(sys.argv[2]) as json_posts:
        load_posts(json_posts)
