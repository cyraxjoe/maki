<%inherit file="../_base.mako" />
<%!
 from functools import partial
 from textile import textile
 textile = partial(textile, html_type='html')
%>
<article>
  <h4>
    <a href="#">${post.title}</a> <br>
    <small style="color: white;" class="right">${post.created.strftime('%b %e, %Y')}</small>
  </h4>
  % if post.format.name == 'textile':
      ${post.content | textile}
  % endif 
</article>
<div class="right">
  <script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
  <script type="text/javascript">
    stLight.options({publisher:'6b2df8ee-5fd7-4a5f-a4f8-27a076045e62'});
  </script>
  <span class="st_twitter_large" st_via="cyraxjoe" displayText="Tweet"></span>
  <span class="st_facebook_large" displayText="Facebook"></span>
  <span class="st_googleplus_large" displayText="Google+"></span>
  <span class="st_linkedin_large" displayText="LinkedIn"></span>
  <span class="st_sharethis_large" displayText="ShareThis"></span>
</div>

