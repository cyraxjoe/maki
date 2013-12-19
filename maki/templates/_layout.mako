<%inherit file="_base.mako" />

  <!-- Nav Bar -->
  <div class="row">
    <div class="eight columns">
      <div id="blogbanner">
	<span class="orange">I</span>${_("ntrospection")}
      </div>
    </div>
    <div class="four columns" id="lang-block">
      <div class="right" >
	<ul class="button-group square" style="margin-bottom: 10px;">
	  % for name, code in [('English', 'en'), ('Español', 'es')]:
	    <li>
	       <a \
		  % if not LOCALE.showall and LANG_IN_REQ and LANG_IN_REQ == code:
		     id="active-lang" \
		  % elif not LOCALE.showall and code == LOCALE.lang.code: 
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
      </div>
    </div>
    
  </div>
  <!-- End Nav -->
  <!-- Main Page Content and Sidebar -->
  <div class="row">
    <!-- Main Content -->
    <div class="nine columns" role="main">
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
	      <a href="/posts/${category.slug}?l=${category.lang.code}">
		${category.name} / <small>${category.lang.name}<small>
        % elif LANG_IN_REQ is not None:
  	      <a href="/posts/${category.slug}?l=${category.lang.code}">
		${category.name} 
        % else:
	      <a href="/posts/${category.slug}">
		${category.name} 
        % endif
	      </a>
 	    </li>
	% endfor
      </ul>

      <div class="panel">
        <h5>${_("Who am I?")}</h5>
        <p><strong>Joel Rivera</strong>, ${_("just another software developer from Monterrey, Mexico")}.</p>
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
		<img src="${STATIC}/images/webfaction.png" alt="Webfaction" title="${_('Proudly hosted at webfaction')}"/></a>
	    </li>
            <li>
	      <a href="http://www.cherrypy.org/">
		<img src="${STATIC}/images/made_with_cherrypy.png"  alt="CherryPy" title="${_('Made with cherrypy')}" />
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
