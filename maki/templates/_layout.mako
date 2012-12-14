<%inherit file="_base.mako" />

<div id="container">

  <div id="head">
    <%block name="header">
      <%include file="_header.mako" />
    </%block>
  </div>
  
  <div id="ibody">
    ${next.body()}
  </div>

  <div id="footer">
    <%block name="footer" >
       <%include file="_footer.mako" />
    </%block>
  </div>

</div>
