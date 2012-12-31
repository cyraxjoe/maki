<%inherit file="../_base.mako" />
   <div id="c1">
     <span id="breadcrumb">
       % for part in parents:
          <span class="bparent">
	    <a href="${part.url}">${part.name}</a>
	  </span>
	  <span id="barrow">&#8594;</span>
       % endfor
         <b class="category">${category.name}</b>
     </span>
     <%include file="../_post_list.mako" />
   </div>
   <div id="c2">
      <%include file="../_col_2.mako" />
   </div>


