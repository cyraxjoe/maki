<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
% if title:
  <title>${_("Introspection")} | ${title}</title>
% else:
  <title>${_("Introspection")}</title>
% endif
  <link rel="stylesheet" href="${STATIC}/css/foundation.min.css">
  <link rel="stylesheet" href="${STATIC}/css/app.css">
  <script src="${STATIC}/js/modernizr.foundation.js"></script>
</head>
<body>
  <!-- Nav Bar -->
  <div class="row">
    <div class="eight columns">
      <h4 id="blogbanner">
	<span class="orange">I</span>${_("ntrospection")}
      </h4>
    </div>
    <div class="four columns" id="lang-block">
      <span class="right" >
	<ul class="button-group square" style="margin-bottom: 10px;">
	  % for name, code in [('English', 'en'), ('Español', 'es')]:
	    <li>
	       <a \
		  % if not LOCALE.showall and code == LOCALE.lang.code: 
		   id="active-lang" \
		  % endif  
		  href="/lang/${code}" title="${name}" 
		  class="has-tip tiny secondary button square">
		 ${code}
	       </a>
	    </li>
	  % endfor
	  <li>
	    <a \
	       % if LOCALE.showall:
               id="active-lang" \
	       % endif 
	       href="/lang/ANY" title="${_('Any')}" class="has-tip tiny secondary button square">
	      &#x2736;&#x2736;
	    </a>
	  </li>
	</ul>
	<small id="what-is-this" class="right orange has-tip" 
	       title="${_('The visibility of the posts is filtered by the selected option')}.">
	  ${_('what is this?')}</small>
      </span>
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
      <h5 style="margin-bottom: 4px;">${_("Categories")}</h5>
      <ul class="side-nav" style="padding-top: 4px;">
	% for category in CATEGORIES:
            <li>
	% if LOCALE.showall:
	      <a href="/post/?category=${category.slug}&amp;lang=${category.lang.code}">
        % else:
	      <a href="/post/?category=${category.slug}">
        % endif
		${category.name}
	      </a>
 	    </li>
	% endfor
      </ul>

      <div class="panel">
        <h5>${_("Who am I?")}</h5>
        <p><strong>Joel Rivera</strong>, ${_("just another programmer from Monterrey, Mexico")}.</p>
        <a href="http://joel.mx/"><strong>${_("More about me")} &rarr;</strong></a>
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
	    <a rel="license"  href="${_('http://creativecommons.org/licenses/by/3.0/deed.en_US')}">
	      <img alt="Creative Commons License" style="border-width:0"
		   src="http://i.creativecommons.org/l/by/3.0/80x15.png" /></a>
	    <br>
	    ${_("This work is licensed under a")}
	    <a rel="license" href="${_('http://creativecommons.org/licenses/by/3.0/deed.en_US')}">
	      ${_("Creative Commons Attribution 3.0 Unported License")}</a>.
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
  <script src="${STATIC}/js/foundation.min.js"></script>
  <script src="${STATIC}/js/app.js"></script>
  % if not IN_DEVELOPMENT:
      <%include file="_google_analytics.mako" />
  % endif
</body>
</html>

