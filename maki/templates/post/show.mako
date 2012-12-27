<%inherit file="../_layout.mako" />

<div id="c1">
  <span id="breadcrumb">
       % for parent in parents:
          <span class="bparent">
	    <a href="${parent.url}">${p.name}</a>
	  </span>
	  <span id="barrow">&#8594;</span>
       % endfor
          <b class="category">${post.title}</b>
  </span>

  <div id="post">
    <span id="pdate">${post.created}</span>
    
    <h1>${post.title}</h1>
    
    <div id="postcontent">
      % if post.format.name == 'markdown':
          ${post.content.as_markdown}
      % elif post.format.name == 'textile':
          ${post.content.as_textile}
      % elif post.format == 'restructuredtext':
          ${post.content.as_restructuredtext}
      % endif 
    </div>
    
    <div id="share">
      <script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
      <script type="text/javascript">
	stLight.options({publisher:'6b2df8ee-5fd7-4a5f-a4f8-27a076045e62'});
      </script>
      <span class="st_twitter_large" st_via="cyraxjoe" displayText="Tweet"></span>
      <span class="st_facebook_large" displayText="Facebook"></span>
      <span class="st_googleplus_large" displayText="Google+"></span>
      <span class="st_linkedin_large" displayText="LinkedIn"></span>
      <span class="st_pinterest_large" displayText="Pinterest"></span>
      <span class="st_email_large" displayText="Email"></span>
      <span class="st_sharethis_large" displayText="ShareThis"></span>
    </div>

  </div>
</div>

<div id="c2">
  <%include file="../_col_2.mako" />
  <ul id="relacionados"> </ul>
</div>

<script type="text/javascript" src="https://apis.google.com/js/plusone.js">
  {lang: 'es'}
</script>


