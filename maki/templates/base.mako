<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">

      <title>${title or ''}</title>
      <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet">
      % for sheet in styles or []:
          <link rel="stylesheet" href="${sheet}" type="text/css" media="screen" />
      % endfor       

     <script type="text/javascript"
	      src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
     % for js in topjs or []:
          <script type="text/javascript" src="${js}"></script>
       % endfor
      
      <%block name="head" /> \
      <%block name="extrahead" />\
    </head>
  
    <body onload="${onload or ''}">
      ${next.body()}

     % for js in bottomjs or []:
       <script type="text/javascript" src="${js}"></script>
     % endfor
    </body>
</html>
