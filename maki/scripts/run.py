import sys

import cherrypy as cp

import maki


def main():
    config_file = sys.argv[1]
    cp.quickstart(maki.ROOT, config=config_file)


if __name__ == '__main__':
    main()
