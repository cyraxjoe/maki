<%inherit file="_base_error.mako" />
<h5>${message or ''}</h5>
<h5>${status or ''}</h5>
% if traceback:
<pre style="text-align: left">
  Status:  ${status or ''}
  Message:  ${message or ''}
  Version: ${version or ''}
  ${traceback}  
</pre>
% endif

