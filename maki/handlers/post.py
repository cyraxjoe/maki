import maki.views.post
from maki import controllers
from maki import dispatcher

disp = _cp_dispatch = dispatcher.JSONnHTML(controllers.Post(),
                                           maki.views.post.JSONPost,
                                           maki.views.post.HTMLPost)
POST = disp.POST
GET = maki.views.post.GET
exposed = True

