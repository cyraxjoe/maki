import os

import mako.exceptions
from mako.lookup import TemplateLookup

import maki

TEMPLATE_DIR = os.path.join(maki.LOCAL_DIR, 'templates')
DEFAULT_LOOKUP = TemplateLookup(directories=[TEMPLATE_DIR, ],
                                input_encoding='utf-8',
                                output_encoding='utf-8')


def direct_render(template, params):
    tpl = DEFAULT_LOOKUP.get_template(template)
    try:
        return tpl.render(**params)
    except Exception:
        raise Exception(mako.exceptions.text_error_template().render())
