% for post in posts:
<article>
  <span class="right white ">${post.created_fmt}</span>
  <h4><a href="/post/${post.slug}">${post.title}</a> </h4>
  <p>${post.abstract}</p>  
</article>
% endfor 


