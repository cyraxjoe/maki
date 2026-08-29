<%inherit file="_base.mako" />

<div class="wrap">
  <header class="site-header">
    <h1 id="blogbanner">
      <a href="/"><span class="orange">I</span>${_("ntrospection")}</a>
    </h1>
    <nav class="lang-nav">
      <ul class="lang-switch">
        % for name, code in [('English', 'en'), ('Español', 'es')]:
        <li>
          <a \
             % if not LOCALE.showall and LANG_IN_REQ and LANG_IN_REQ == code:
               id="active-lang" \
             % elif not LOCALE.showall and code == LOCALE.lang.code:
               id="active-lang" \
             % endif
             href="/lang/${code}" title="${name}">${code}</a>
        </li>
        % endfor
        <li>
          <a \
             % if LOCALE.showall:
               id="active-lang" \
             % endif
             href="/lang/ANY" title="${_('Any')}">&#x2736;&#x2736;</a>
        </li>
      </ul>
      <small id="what-is-this"
             title="${_('The visibility of the posts is filtered by the selected option')}.">
        ${_('what is this?')}</small>
    </nav>
  </header>

  <div class="site-body">
    <main>
      ${next.body()}
    </main>

    <aside class="sidebar">
  <%block name="sidebar">
      <h2>${_("Categories")}</h2>
      <ul class="side-nav">
        % for category in CATEGORIES:
        <li>
          % if LOCALE.showall:
          <a href="/posts/?cat=${category.slug}&amp;l=${category.lang.code}">
            ${category.name} <small>/ ${category.lang.name}</small>
          % elif LANG_IN_REQ is not None:
          <a href="/posts/?cat=${category.slug}&amp;l=${category.lang.code}">
            ${category.name}
          % else:
          <a href="/posts/?cat=${category.slug}">
            ${category.name}
          % endif
          </a>
        </li>
        % endfor
      </ul>

      <div class="panel">
        <h2>${_("Who am I?")}</h2>
        <p><strong>Joel Rivera</strong>, ${_("just another software developer from Monterrey, Mexico")}.</p>
        <a href="https://joel.mx/"><strong>${_("More about me")} &rarr;</strong></a>
      </div>
  </%block>
    </aside>
  </div>

  <footer class="site-footer">
<%block name="footer">
    <div class="footer-cols">
      <div id="license">
        <p>
          <a rel="license" href="${_('https://creativecommons.org/licenses/by/4.0/deed.en')}">
            <img alt="Creative Commons License" style="border-width:0"
                 src="https://licensebuttons.net/l/by/4.0/80x15.png"></a>
          <br>
          ${_("This work is licensed under a")}
          <a rel="license" href="${_('https://creativecommons.org/licenses/by/4.0/deed.en')}">
            ${_("Creative Commons Attribution 4.0 International License")}</a>.
        </p>
      </div>
      <div>
        <a href="https://cherrypy.dev/">
          <img src="${STATIC}/images/made_with_cherrypy.png" alt="CherryPy"
               title="${_('Made with cherrypy')}">
        </a>
      </div>
    </div>
</%block>
  </footer>
</div>
