from maki.views.root import Root
root = Root()


def bind(cls, name=None, parent=root):
    if name is None:
        name = cls.__name__.lower()


    view_inst = cls()
    setattr(parent, name, view_inst)
    return view_inst
    
    return cls

def setup():
    from maki.views.post import Post
