<ul class="breadcrumbs">
  <li> <a href="/"> ${_('Home')}</a></li>
  % for i, (url, name) in enumerate(breadcrumb, 1):
  % if i == len(breadcrumb): 
    <li class="current">
  % else:
    <li>
  % endif
    <a href="${url}">${name} </a>
  </li>
  % endfor
</ul>
