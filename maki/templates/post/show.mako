<%inherit file="../_layout.mako" />
<%!
 from docutils.core import publish_parts
 rst  = lambda cnt: publish_parts(cnt, writer_name='html4css1',
                                  settings_overrides={
                                     'initial_header_level': 2,
                                     'syntax_highlight': 'short'
                                  }).get('fragment')
%>
<%include file="_breadcrumb.mako" />
<%block name="pygments">
    <link rel="stylesheet" href="${STATIC}/css/pygments/monokai.css">
</%block>

<article id="post-body">
  <span class="post-date">${post.created_fmt}</span>
  <h1>${post.title}</h1>
  % if post.format.name == 'rst':
      ${post.content | rst}
  % else:
      ${post.content}
  % endif

  % if post.tags:
  <div class="post-tags">
    <span>Tags:</span>
    <ul class="taglist">
      % for tag in post.tags:
      <li class="tag">${tag.name}</li>
      % endfor
    </ul>
  </div>
  % endif
</article>
