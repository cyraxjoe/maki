% for post in posts:
<article>
  <span class="right white ">${post.created_fmt}</span>
  <h4><a href="/post/${post.slug}">${post.title}</a> </h4>
  <p>${post.abstract}</p>  
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

