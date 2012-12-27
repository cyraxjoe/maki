% for post in posts or []:
    <div class="shortpost">
      <div id="ctag" class="inverted">
	${post.category.name}
      </div>
      <span id="shortpdate">${post.created}</span>
      <h3><a href="/post/${post.slug}">${post.title}</a></h3>
      <p>${post.abstract}</p>
      <ul class="taglist hlist" title="Tags">
    % for tag in post.tags:
	<li class="tag">${tag.name}</li>
    % endfor 
      </ul>
    </div>
% endfor
