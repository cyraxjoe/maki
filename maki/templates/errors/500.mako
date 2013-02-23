<%inherit file="_base_error.mako" />

<h5>There has been problem while we were attending your request. (${status or ''})</h5>
<h5>${message}</h5>
<h6>Sorry for the inconvenience.</h6>
% if notified is not None:
   % if notified:
  <h6>"This incident has been reported"</h6>
   % else:
  <h6>Unable to notify this incident, please contact me at
    <a href="http://joel.mx/">my personal site</a>
  </h6>
  % endif
% endif

% if traceback:
<pre style="text-align: left">
  Status:  ${status or ''}
  Message:  ${message or ''}
  Version: ${version or ''}
  ${traceback}
</pre>
% endif



