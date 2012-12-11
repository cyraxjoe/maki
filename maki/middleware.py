import maki

def set_defaults(env):
    env['STATIC_URL'] = maki.APP.config['templates']['static_url']
    
