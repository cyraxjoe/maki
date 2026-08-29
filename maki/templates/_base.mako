<%
if LOCALE:
   html_lang = LOCALE.lang.code
else:
   html_lang = 'en'
%>
<!DOCTYPE html>
<html lang="${html_lang}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
% if KEYWORDS:
    <meta name="keywords" content="${','.join(KEYWORDS)}">
% endif
% if DESCRIPTION:
    <meta name="description" content="${DESCRIPTION}">
    <meta property="og:description" content="${DESCRIPTION}">
% endif
% if title:
    <meta property="og:title" content="${title}">
% endif
    <meta property="og:site_name" content="${_('Introspection')}">
% if feed_url:
    <link href="${feed_url}" type="application/atom+xml" rel="alternate" title="${feed_title}">
% endif
    <link rel="shortcut icon" href="/static/images/favicon.ico">
% if title:
    <title>${_("Introspection")} / ${title}</title>
% else:
    <title>${_("Introspection")}</title>
% endif
    <link rel="stylesheet" href="${STATIC}/css/maki.css">
    <%block name="pygments" />
% for sheet in context.get('styles', ()):
    <link rel="stylesheet" href="${sheet}">
% endfor
  </head>
  <body>
    ${next.body()}
  </body>
</html>
