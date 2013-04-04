<%
if LOCALE:
   html_lang = LOCALE.lang.code
else:
   html_lang = 'en'
%>
<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="${html_lang}"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="${html_lang}"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="${html_lang}"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="${html_lang}" > <!--<![endif]-->
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
% if KEYWORDS:
    <meta name="keywords" content="${','.join(KEYWORDS)}" />
% endif
% if DESCRIPTION:
    <meta name="description" content="${DESCRIPTION}" />
% endif  
% if feed_url:
    <link href="${feed_url}" type="application/atom+xml"  rel="alternate" title="${feed_title}">
% endif
    <link rel="shortcut icon" href="/static/images/favicon.ico" />
% if title:
    <title>${_("Introspection")} / ${title}</title>
% else:
    <title>${_("Introspection")}</title>
% endif
    <link rel="stylesheet" href="${STATIC}/css/foundation.min.css">
    <link rel="stylesheet" href="${STATIC}/css/app.css">
    <%block name="pygments" />
    <script src="${STATIC}/js/modernizr.foundation.js"></script>
  </head>
  <body>
    ${next.body()}
  </body>
</html>

