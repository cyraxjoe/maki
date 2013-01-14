<%inherit file="../_base.mako" />

<ul class="breadcrumbs">
  <li> <a href="/"> Home </a></li>
  <li class="current">
    <a href="/post/?category=${category.slug}" >${category.name}</a>
  </li>
</ul>
<%include file="../_post_list.mako" />
