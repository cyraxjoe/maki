<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="shortcut icon" href="${STATIC_URL}/images/favicon/instrospeccion.ico" />
      <title>${title or ''}</title>
<!--  <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet"> -->
      <link rel="stylesheet" href="${STATIC_URL}/css/estilo.css" type="text/css"/>
 % for sheet in styles or []:
      <link rel="stylesheet" href="${sheet}" type="text/css" media="screen" />
 % endfor       
     <script type="text/javascript"
	     src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
 % for js in topjs or []:
     <script type="text/javascript" src="${js}"></script>
 % endfor
     <%block name="head" /> \
    </head>
    <body>
      ${next.body()}
 % for js in bottomjs or []:
      <script type="text/javascript" src="${js}"></script>
 % endfor
      <%include file="_google_analytics.mako" />
    </body>
</html>
