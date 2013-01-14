import hashlib

import bcrypt
import cherrypy

import maki.scaffold
import maki.views
from maki import db


class Login(maki.scaffold.Controller):
    __views__ = (maki.views.login.JSON,)

    required_fields = {'user', 'passwd'}

    def _have_valid_passwd(self, user, passwd):
        if bcrypt.hashpw(passwd, user.passwd) == user.passwd:
            return True
        else:
            return False
            
    def _get_user_by_name(self, username):
        return db.ses.query(db.models.User).filter_by(name=username).scalar()


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
        
