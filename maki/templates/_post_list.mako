% for post in posts:
<article>
  <span class="right white ">${post.created_fmt}</span>
  <h5><a href="/post/${post.slug}">${post.title}</a> </h5>
  <p>${post.abstract}</p>  
  <div style="padding: 0 0 1px 0;">

% if category is UNDEFINED:
    <span class="left">
      % for tag in post.tags:
      <span class="radius secondary label">${tag.name}</span>
      % endfor
    </span>
    <span class="right label" style="margin-left: 10px;font-size: 100%" >
      ${post.category.name}
    </span>
% else:
    <span class="right">
      % for tag in post.tags:
      <span class="radius secondary label">${tag.name}</span>
      % endfor
    </span>
% endif
  </div>

</article>
<hr>
% endfor 
% if pages >= 2:
<ul class="pagination right">
% for pagenum in range(1, pages):
    % if pagenum == currpage:
       <li class="current">  <a href="javascript:void()">${pagenum}</a> </li>
    % else:
       % if category is UNDEFINED:
           <li><a href="?page=${pagenum}">${pagenum}</a></li>
       % else:
	   % if LOCALE.showall:
           <li>
	     <a href="?category=${category.slug}&amp;lang=${category.lang.code}&amp;page=${pagenum}">
	       ${pagenum}</a>
	   </li>
	   % else:
          <li><a href="?category=${category.slug}&amp;page=${pagenum}">${pagenum}</a></li>
	   % endif
           
       % endif

    % endif
% endfor
</ul>
% endif

