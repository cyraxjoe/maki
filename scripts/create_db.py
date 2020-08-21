import sys
import subprocess

from cherrypy.lib import reprconf
from maki import db


def fill_db(config):
    db.load_engine(config["sqlalchemy"])
    db.models.Base.metadata.create_all(bind=db.session.bind)


def drop_and_create_db(conf):
    dbname = conf["sqlalchemy"]["url"].rsplit("/")[-1]
    print('Droping "%s" database...' % dbname)
    try:
        subprocess.check_output(["dropdb", dbname], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        msg = err.output.decode().strip()
        if not msg.endswith("does not exist"):
            raise Exception(msg)
    print('Creating "%s" database' % dbname)
    subprocess.call("createdb %s " % dbname, shell=True)
    print("Done")


def main():
    try:
        config_path = sys.argv[1]
    except IndexError:
        print("Invalid arguments", file=sys.stderr)
        sys.exit(1)
    config = reprconf.Config(config_path)
    try:
        extrcom = sys.argv[2]
    except IndexError:
        pass
    else:
        if extrcom == "drop":
            drop_and_create_db(config)
    fill_db(config)
    db.session.commit()


if __name__ == "__main__":
    main()
