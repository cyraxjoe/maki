from maki import db
from maki.bindutils import bind_tool


@bind_tool(name="removedbs", point="on_end_request")
def remove_dbs():
    db.session.remove()
