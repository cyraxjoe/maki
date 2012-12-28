import maki


def set_defaults(env):
    env['STATIC_URL'] = maki.APP.config['templates']['static_url']


def set_csstyles(env, csstyles):
    sheets = []
    static_url = env['STATIC_URL']
    for sheet_path in csstyles:
        sheets.append('/'.join((static_url, 'css', sheet_path)))
    env['styles'] = sheets
