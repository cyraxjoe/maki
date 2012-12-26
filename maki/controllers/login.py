import hashlib

import bcrypt
import cherrypy
from sqlalchemy.exc import DataError

from maki import db
from maki.views.login import JSONLogin
from . import Controller



class Login(Controller):
    __views__ = (JSONLogin,)
    

    def _have_valid_passwd(self, user, passwd):
        if bcrypt.hashpw(passwd, user.passwd) == user.passwd:
            return True
        else:
            return False
            

    def _get_user_by_name(self, username):
        try:
            user = db.ses.query(db.models.User).filter_by(name=username).one()
        except DataError:
            return None
        else:
            return user
    

    def authenticate(self, username, passwd):
        user = self._get_user_by_name(username)
        passwd = hashlib.sha256(passwd.encode()).hexdigest()
        if user is not None:
            if self._have_valid_passwd(user, passwd):
                cherrypy.session['uid'] = user.id
                return True
            else:
                return False
        else:
            return False
        
