import sys

from cherrypy.lib import reprconf

from maki import db

def _simple_add(dbs, Model, elements):
    emodels = [Model(**element) for element in elements]
    dbs.add_all(emodels)
    return emodels
        

def sample_categories(dbs, lang):
    categories = [{'name': 'Programming',
                   'lang': lang},
                  {'name': 'Biology',
                   'lang': lang}]
    return _simple_add(dbs, db.models.Category, categories)



def sample_posts(dbs, pformat, author, category, tags, lang):
    revisions = [{'title': 'Sample title of post',
                  'abstract': 'Micro sample abstract',
                  'content': 'Le content of the sample post'}]
    posts = [{'public': True,
              'format': pformat,
              'author': author,
              'category': category,
              'tags': tags,
              'lang': lang,
              'revisions':
              (_simple_add(dbs, db.models.PostRevision, revisions))}]
    return _simple_add(dbs, db.models.Post, posts)


def sample_post_formats(dbs):
    frmts = [{'name': 'textile'},
             {'name': 'rst'} ]
    return _simple_add(dbs, db.models.PostFormat, frmts)


def sample_tags(dbs, lang):
    tags = [{'name': 'python',   'lang': lang},
            {'name': 'monterrey', 'lang': lang},
            {'name': 'golang', 'lang': lang}]
    return _simple_add(dbs, db.models.Tag, tags)


def sample_users(dbs):
    users = [{'name': 'joe',
              'vname': 'Joel Rivera',
              'email': 'rivera@joel.mx',
              'passwd': 'samplepasswd',
              'active': True},]
    return _simple_add(dbs, db.models.User, users)

def sample_languages(dbs):
    langs = [{'name': 'Español', 'code': 'es'},
             {'name': 'English', 'code': 'en'}]
    return _simple_add(dbs, db.models.Language, langs)



def load_all():
    languages = sample_languages(db.ses)
    lang_en = languages[1]
    tags = sample_tags(db.ses, lang_en)
    pformats = sample_post_formats(db.ses)
    users = sample_users(db.ses)
    categories = sample_categories(db.ses, lang_en)
    sample_posts(db.ses, pformats[1],  users[0], categories[0],
                 tags, lang_en)
    db.ses.commit()

if __name__ == '__main__':
    config = reprconf.Config(sys.argv[1])
    db.load_engine(config['sqlalchemy'])
    load_all()
