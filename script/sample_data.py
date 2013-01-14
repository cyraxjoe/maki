import sys

from cherrypy.lib import reprconf

from maki import db

def _simple_add(dbs, Model, elements):
    emodels = [Model(**element) for element in elements]
    dbs.add_all(emodels)
    return emodels
        

def sample_categories(dbs):
    categories = [{'name': 'Programming'},
                  {'name': 'Biology'}]
    return _simple_add(dbs, db.models.Category, categories)



def sample_posts(dbs, pformat, author, category, tags):
    posts = [{'title': 'Sample title of post',
              'abstract': 'Micro sample abstract',
              'content': 'Le content of the sample post',
              'slug': 'sample-title-of-post',
              'public': True,
              'format': pformat,
              'author': author,
              'category': category,
              'tags': tags}]
    return _simple_add(dbs, db.models.Post, posts)


def sample_post_formats(dbs):
    frmts = [{'name': 'textile'},
             {'name': 'rst'} ]
    return _simple_add(dbs, db.models.PostFormat, frmts)



def sample_tags(dbs):
    tags = [{'name': 'python'},
            {'name': 'monterrey'},
            {'name': 'golang'}]
    return _simple_add(dbs, db.models.Tag, tags)


def sample_users(dbs):
    users = [{'name': 'joe',
              'vname': 'Joel Rivera',
              'email': 'rivera@joel.mx',
              'passwd': 'samplepasswd',
              'active': True},]
    return _simple_add(dbs, db.models.User, users)




def load_all():
    tags = sample_tags(db.ses)
    pformats = sample_post_formats(db.ses)
    users = sample_users(db.ses)
    categories = sample_categories(db.ses)
    sample_posts(db.ses, pformats[1],  users[0], categories[0], tags)
    db.ses.commit()

if __name__ == '__main__':
    config = reprconf.Config(sys.argv[1])
    db.load_engine(config['sqlalchemy'])
    load_all()
