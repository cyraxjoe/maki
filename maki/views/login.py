from maki import dispatcher


class JSONLogin(object):
    pass


class HTMLLogin(object):
    pass

_cp_dispatch = dispatcher.JSONnHTML(JSONLogin, HTMLLogin)
exposed = True
def GET():
    return "Index login"
