from wtforms import Form
from wtforms import validators as val
from wtforms import (TextField, PasswordField)


class LoginForm(Form):
    user = TextField('User',
                     [val.Required(), val.Length(min=1, max=32)])
    passwd = PasswordField('Password',
                           [val.Required(), val.Length(min=6, max=64)])
    


class CompatParams(dict):
    """Utility class to work with WTForms, just past the
    params of the request to the constructor of this class
    and every interaction with WTForms should be fine."""

    def getlist(self, name):
        if isinstance(self[name], list) or isinstance(self[name], tuple):
            return self[name]
        else:
            return [self[name], ]
