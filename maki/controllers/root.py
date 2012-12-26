from . import Controller
from .post import Post
from .login import Login


class Root(Controller):
    post = Post()
    login = Login()
    
