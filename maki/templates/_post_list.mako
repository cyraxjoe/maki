% for post in posts or []:
    <div class="shortpost">
      <div id="ctag" class="inverted">
	${post.category.name}
      </div>
      <span id="shortpdate">${post.created}</span>
      <h3><a href="/post/${post.category.url }/${post.url}">${post.title}</a></h3>
      <p>${post.abstract}</p>
      <b id="ccount">${post.comment_count} comentarios</b>
      <ul class="taglist hlist" title="Tags">
    % for tag in post.tags:
	<li class="tag">${tag}</li>
    % endfor 
      </ul>
    </div>        
% endfor
