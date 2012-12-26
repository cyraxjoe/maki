from wtforms import Form
from wtforms import validators as val
from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    TextAreaField,
    HiddenField,
)


class CompatParams(dict):
    """Utility class to work with WTForms, just past the
    params of the request to the constructor of this class
    and every interaction with WTForms should be fine."""

    def getlist(self, name):
        if isinstance(self[name], list) or isinstance(self[name], tuple):
            return self[name]
        else:
            return [self[name], ]


class LoginForm(Form):
    user = TextField('User',
                     [val.Required(), val.Length(min=1, max=32)])
    passwd = PasswordField('Password',
                           [val.Required(), val.Length(min=6, max=64)])
    

class AddPostForm(Form):
    title = TextField('Title', [val.Required(),])
    abstract = TextField('Abstract', [val.Required()])
    content = TextAreaField('Content', [val.Required()])
    category = SelectField('Category', [val.Required()], choices=[])
    format = SelectField('Format', [val.Required()], choices=[])
    tags = SelectMultipleField('Tags', choices=[])


class EditPostForm(AddPostForm):
    pass
    

class AddCategoryForm(Form):
    name = TextField('Name')
    slug = TextField('Name')


class EditCategoryForm(AddCategoryForm):
    pass

    

