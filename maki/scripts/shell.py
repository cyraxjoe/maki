# General python history management (PYSTARTUP)
# Cleaned up 7/11/2009 by Jeff Schroeder <jeffschroeder@computer.org>
# Released under the public domain for all to share and share alike.
try:
    import readline
except ImportError:
    pass
else:
    import os
    import atexit
    import rlcompleter

class irlcompleter(rlcompleter.Completer):
    def complete(self, text, state):
        if text == "":
            readline.insert_text('\t')
            return None
        else:
            return rlcompleter.Completer.complete(self,text,state)
# You could change this line to bind another key instead tab.
readline.parse_and_bind("tab: complete")
readline.set_completer(irlcompleter().complete)
# Restore our command-line history, and save it when Python exits.
historyPath = os.path.expanduser("~/.pyhistory")
# Create a blank history file if it doesn't exist already
if not os.path.exists(historyPath) and not os.path.isdir(historyPath):
    try:
        open(historyPath, 'w').close()
    # Gracefully ignore things if historyPath is not writable
    except IOError:
        pass
# Read the history file in for autocompletion and save it on exit
if os.access(historyPath, os.R_OK):
    readline.read_history_file(historyPath)
if os.access(historyPath, os.W_OK):
    atexit.register(lambda x=historyPath: readline.write_history_file(x))

def run():
    # Specific to maki
    import sys
    import code
    from pprint import pprint

    import cherrypy
    from cherrypy.lib import reprconf
    config = reprconf.Config(sys.argv[1]) # first arg == config file
    cherrypy.config = config

    import maki
    from maki import db
    db.load_engine(config['sqlalchemy'])
    code.interact('Welcome to the Maki Python Shell', local=locals())
