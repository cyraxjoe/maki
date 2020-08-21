import re
import pprint

import cherrypy as cp
import unidecode


def log(message, cntx="DEBUG", tb=False):
    if isinstance(message, str):
        cp.log.error(message, context=cntx, traceback=tb)
    else:
        cp.log.error(pprint.pformat(message), context=cntx, traceback=tb)


def in_development():
    return cp.config.get("environment") not in ("production", "embedded")


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r"\W+", "-", text)


def redirect_if_kwargs(kwargs, original_url, *valid_kwargs):
    """
    Just a handy function to redirect to the original URL when
    any extra kwarg is received on the request.

    It also have some extra magic to gather the valid kwargs
    and redirect to that place just removing the invalid ones.
    """
    # fuck you linkedin or any other platform that modify my URLs
    if kwargs:
        if valid_kwargs:
            qs, qsparts = "", []
            for kw in valid_kwargs:
                qsparts.append(cp.request.params.get(kw, None))
            if any(qsparts):
                qs = "&".join(
                    ["{}={}".format(p, v) for p, v in zip(valid_kwargs, qsparts) if v]
                )
            if qs:
                original_url = "{}?{}".format(original_url, qs)
        raise cp.HTTPRedirect(original_url, 301)
