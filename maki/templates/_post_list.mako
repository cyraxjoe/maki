% for post in posts:
<article class="shortpost">
  <span class="post-date">${post.created_fmt}</span>
  <h2><a href="/posts/${post.slug}">${post.title}</a></h2>
  <p>${post.abstract}</p>
  <div class="post-meta">
    <ul class="taglist">
      % for tag in post.tags:
      <li class="tag">${tag.name}</li>
      % endfor
    </ul>
% if category is UNDEFINED:
    <a class="category-label"
       href="/posts/?cat=${post.category.slug}">${post.category.name}</a>
% endif
  </div>
</article>
% endfor
% if pages >= 2:
<nav aria-label="${_('Pagination')}">
  <ul class="pagination">
% for pagenum in range(1, pages):
    % if pagenum == currpage:
    <li class="current"><a href="#" aria-current="page">${pagenum}</a></li>
    % elif category is UNDEFINED:
    <li><a href="?page=${pagenum}">${pagenum}</a></li>
    % elif LOCALE.showall:
    <li>
      <a href="/posts/?cat=${category.slug}&amp;l=${category.lang.code}&amp;page=${pagenum}">
        ${pagenum}</a>
    </li>
    % else:
    <li><a href="/posts/?cat=${category.slug}&amp;page=${pagenum}">${pagenum}</a></li>
    % endif
% endfor
  </ul>
</nav>
% endif
