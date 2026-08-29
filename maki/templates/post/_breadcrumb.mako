<nav aria-label="${_('Breadcrumb')}">
  <ul class="breadcrumbs">
    <li><a href="/">${_('Home')}</a></li>
    % for i, (url, name) in enumerate(breadcrumb, 1):
    % if i == len(breadcrumb):
    <li class="current"><a href="${url}">${name}</a></li>
    % else:
    <li><a href="${url}">${name}</a></li>
    % endif
    % endfor
  </ul>
</nav>
