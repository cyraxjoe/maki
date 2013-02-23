<%inherit file="../_base.mako" />
<%!
 from functools import partial
 from textile import textile
 from docutils.core import publish_parts
 textile = partial(textile, html_type='html')
 rst  = lambda cnt: publish_parts(cnt, writer_name='html4css1')['fragment']
%>
<%include file="_breadcrumb.mako" />

<article id="post-body">
  <span class="right white">${post.created_fmt}</span>
  <h4 class="orange"> ${post.title} </h4>
  % if post.format.name == 'rst':
      ${post.content | rst}
  % elif post.format.name == 'textile':
      ${post.content | textile}
  % else:
      ${post.content}
  % endif 

 % if post.tags:
  <div>
    <span  style="padding-right: 10px;">Tags:</span>
    % for tag in post.tags:
    <span class="radius secondary label">${tag.name}</span>
    % endfor
  </div>
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

