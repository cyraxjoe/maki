    <ul id="categorias" class="hlist">
% for cat in categories or []:
    <li>
      <a href="/post/${cat.url}"><b class="category">${cat.name}</b></a>
    </li>
% endfor
    </ul>
    <span id="blogname"><span class="firstletter orange">I</span>ntrospección</span>
% if rss_url:
    <a href="{{rss_url}}">
      <img id="rssicon"  src="/static/images/rss-icon-small.png" alt="rss" /></a>
% endif

