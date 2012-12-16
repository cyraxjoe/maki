import maki.views.login
from maki import dispatcher
from maki import controllers

disp = _cp_dispatch = dispatcher.JSONnHTML(controllers.Login(),
                                           maki.views.login.JSONLogin,
                                           maki.views.login.HTMLLogin)
POST = disp.POST
exposed = True
