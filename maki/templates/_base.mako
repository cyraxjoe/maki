<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
% if title:
  <title>Introspection | ${title}</title>
% else:
  <title>Introspection</title>
% endif
  <link rel="stylesheet" href="${STATIC}/css/foundation.min.css">
  <link rel="stylesheet" href="${STATIC}/css/app.css">
  <script src="${STATIC}/js/modernizr.foundation.js"></script>
</head>
<body>
  <!-- Nav Bar -->
  <div class="row">
    <div class="twelve columns">
      
      <h4 id="blogbanner">
	<span class="orange">I</span>ntrospection
      </h4>
    </div>
  </div>
  <!-- End Nav -->
  <!-- Main Page Content and Sidebar -->
  <div class="row">
    <!-- Main Content -->
    <div class="nine columns" role="content">
      ${next.body()}
    </div>
    <!-- End Main Content -->
    
    <!-- Sidebar -->
    <aside class="three columns">
  <%block name="sidebar">
      <h5 style="margin-bottom: 4px;">Categories</h5>
      <ul class="side-nav" style="padding-top: 4px;">
	% for category in CATEGORIES:
        <li><a href="/post/?category=${category.slug}">${category.name}</a></li>
	% endfor
      </ul>

      <div class="panel">
        <h5>Who am I?</h5>
        <p><strong>Joel Rivera</strong>, just another programmer from Monterrey, Mexico.</p>
        <a href="http://joel.mx/"><strong>More about me &rarr;</strong></a>
      </div>

 </%block>
    </aside>
    <!-- End Sidebar -->
  </div>

  <!-- End Main Content and Sidebar -->

  <!-- Footer -->
  <footer class="row">
<%block name="footer">
    <div class="twelve columns">
      <hr />
      <div class="row">
        <div id="license" class="eight columns">
	  <p>
	    <a rel="license"  href="http://creativecommons.org/licenses/by/3.0/deed.en_US">
	      <img alt="Creative Commons License" style="border-width:0"
		   src="http://i.creativecommons.org/l/by/3.0/80x15.png" /></a>
	    <br>
	    This work is licensed under a
	    <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.en_US">
	      Creative Commons Attribution 3.0 Unported License</a>.
	  </p>
        </div>
        <div class="four columns">
          <ul class="link-list right">
	    <li style="padding: 5px 0;">
	      <a href="http://www.webfaction.com?affiliate=thejoe">
		<img src="http://www.webfaction.com/banners/80x15.png" border="0"  alt="Hospedado en web faction" title="Proudly hosted at webfaction"/></a>
	    </li>
            <li>
	      <a href="http://www.cherrypy.org/">
		<img src="${STATIC}/images/made_with_cherrypy.png" 
		     border="0" alt="Made with cherrypy." title="Made with cherrypy" />
	      </a>
	    </li>
          </ul>
        </div>
      </div>
    </div>
</%block>
  </footer>
  <!-- End Footer -->
  <!-- Included JS Files (Compressed) -->
  <script src="${STATIC}/js/jquery.js"></script>
  <script src="${STATIC}/js/foundation.min.js"></script>
  <!-- Initialize JS Plugins -->
  <script src="${STATIC}/js/app.js"></script>
  % if not IN_DEVELOPMENT:
      <%include file="_google_analytics.mako" />
  % endif
</body>
</html>

