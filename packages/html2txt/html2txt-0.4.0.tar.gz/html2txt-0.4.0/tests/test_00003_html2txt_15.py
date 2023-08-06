import pytest
from html2txt import converters

# example: 3
# section: html2txt
def test_15_00003():
  html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>html_tags.html</title><style></style></head><body id="preview">
<ul>
<li class="has-line-data" data-line-start="0" data-line-end="1"><input type="checkbox" id="checkbox6804" checked="true"><label for="checkbox6804">@mentions, #refs, </label><a href="">links</a>, <strong>formatting</strong>, and &lt;del&gt;tags&lt;/del&gt; supported</li>
<li class="has-line-data" data-line-start="1" data-line-end="2"><input type="checkbox" id="checkbox6805" checked="true"><label for="checkbox6805">list syntax required (any unordered or ordered list supported)</label></li>
<li class="has-line-data" data-line-start="2" data-line-end="3"><input type="checkbox" id="checkbox6806" checked="true"><label for="checkbox6806">this is a complete item</label></li>
<li class="has-line-data" data-line-start="3" data-line-end="4"><input type="checkbox" id="checkbox6807"><label for="checkbox6807">this is an incomplete item</label></li>
</ul>
<p style="font-size:100px">&#129409;</p>
<p>I will display &#129409;</p>
<p>I will display &#x1F981;</p> 
</body></html>
"""
  expected_markdown = """
* [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
* [x] list syntax required (any unordered or ordered list supported)
* [x] this is a complete item
* [ ] this is an incomplete item

🦁

I will display 🦁

I will display 🦁
 



"""
  markdown = converters.Html2Markdown().convert(html)
  assert markdown == expected_markdown
