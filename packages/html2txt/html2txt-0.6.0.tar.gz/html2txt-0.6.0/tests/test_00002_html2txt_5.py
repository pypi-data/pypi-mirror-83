import pytest
from html2txt import converters

# example: 2
# section: html2txt
def test_5_00002():
  html = """<div class="bd-example">
  <address>
    <strong>Twitter, Inc.</strong><br />
    1355 Market St, Suite 900<br />
    San Francisco, CA 94103<br />
    <abbr title="Phone">P:</abbr> (123) 456-7890
  </address>

  <address>
    <strong>Full Name</strong><br />
    <a href="/cdn-cgi/l/email-protection#6546"><span class="__cf_email__" data-cfemail="17717e656463397b76646357726f767a677b723974787a">[email&#160;protected]</span><script data-cfhash='f9e31' type="text/javascript">/* <![CDATA[ */!function(t,e,r,n,c,a,p){try{t=document.currentScript||function(){for(t=document.getElementsByTagName('script'),e=t.length;e--;)if(t[e].getAttribute('data-cfhash'))return t[e]}();if(t&&(c=t.previousSibling)){p=t.parentNode;if(a=c.getAttribute('data-cfemail')){for(e='',r='0x'+a.substr(0,2)|0,n=2;a.length-n;n+=2)e+='%'+('0'+('0x'+a.substr(n,2)^r).toString(16)).slice(-2);p.replaceChild(document.createTextNode(decodeURIComponent(e)),c)}p.removeChild(t)}}catch(u){}}()/* ]]> */</script></a>
  </address>
</div>
"""
  expected_markdown = """
  
  <address>
    **Twitter, Inc.**  
    1355 Market St, Suite 900  
    San Francisco, CA 94103  
    
*[P:]: Phone

Phone (123) 456-7890
  </address>

  <address>
    **Full Name**  
    <[email protected]>
  </address>

  
"""
  markdown = converters.Html2Markdown().convert(html)
  assert markdown == expected_markdown
