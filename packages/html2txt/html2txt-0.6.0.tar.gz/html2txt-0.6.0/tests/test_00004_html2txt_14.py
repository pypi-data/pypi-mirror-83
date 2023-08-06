import pytest
from html2txt import converters

# example: 4
# section: html2txt
def test_14_00004():
  html = """<table class="standard-table"> 
 <thead> 
  <tr> 
 
   <th scope="col">Element</th> 
   <th scope="col">Description</th> 
  </tr> 
 </thead> 
 <tbody> 
  
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/caption" title="The HTML &lt;caption&gt; Element (or HTML Table Caption Element) represents the title of a table. Though it is always the first descendant of a &lt;table&gt;, its styling, using CSS, may place it elsewhere, relative to the table."><code>&lt;caption&gt;</code></a></td> 
   <td>The <strong>HTML <code>&lt;caption&gt;</code> Element</strong> (or <em>HTML Table Caption Element</em>) represents the title of a table. Though it is always the first descendant of a <a href="/en-US/docs/Web/HTML/Element/table" title="The HTML Table Element (&lt;table&gt;) represents data in two dimensions or more."><code>&lt;table&gt;</code></a>, its styling, using CSS, may place it elsewhere, relative to the table.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/col" title="The HTML Table Column Element (&lt;col&gt;) defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a &lt;colgroup&gt; element."><code>&lt;col&gt;</code></a></td> 
   <td>The <em>HTML Table Column Element</em> (<strong>&lt;col&gt;</strong>) defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a <a href="/en-US/docs/Web/HTML/Element/colgroup" title="The&#xA0;HTML Table Column Group Element&#xA0;(&lt;colgroup&gt;) defines a group of columns within a table."><code>&lt;colgroup&gt;</code></a> element.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/colgroup" title="The&#xA0;HTML Table Column Group Element&#xA0;(&lt;colgroup&gt;) defines a group of columns within a table."><code>&lt;colgroup&gt;</code></a></td> 
   <td>The&#xA0;<em>HTML Table Column Group Element</em>&#xA0;(<strong>&lt;colgroup&gt;</strong>) defines a group of columns within a table.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/table" title="The HTML Table Element (&lt;table&gt;) represents tabular data - i.e., information expressed via a two dimensional data table."><code>&lt;table&gt;</code></a></td> 
   <td>The <strong>HTML Table Element</strong> (<code>&lt;table&gt;</code>) represents tabular data - i.e., information expressed via a two dimensional data table.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/tbody" title="The HTML Table Body Element (&lt;tbody&gt;) defines one or more &lt;tr&gt; element data-rows to be the body of its parent &lt;table&gt; element (as long as no &lt;tr&gt; elements are immediate children of that table element.)&#xA0; In conjunction with a preceding &lt;thead&gt; and/or &lt;tfoot&gt; element, &lt;tbody&gt; provides additional semantic information for devices such as printers and displays. Of the parent table&apos;s child elements, &lt;tbody&gt; represents the content which, when longer than a page, will most likely differ for each page printed; while the content of &lt;thead&gt; and &lt;tfoot&gt; will be the same or similar for each page printed. For displays, &lt;tbody&gt; will enable separate scrolling of the &lt;thead&gt;, &lt;tfoot&gt;, and &lt;caption&gt; elements of the same parent &lt;table&gt; element.&#xA0; Note that unlike the &lt;thead&gt;, &lt;tfoot&gt;, and &lt;caption&gt; elements however, multiple&#xA0;&lt;tbody&gt; elements are permitted (if consecutive), allowing the data-rows in long tables to be divided into different sections, each separately formatted as needed."><code>&lt;tbody&gt;</code></a></td> 
   <td>The HTML <strong>Table Body Element (&lt;tbody&gt;)</strong> defines one or more <a href="/en-US/docs/Web/HTML/Element/tr" title="The HTML element&#xA0;table row &lt;tr&gt;&#xA0;defines a row of cells in a table. Those can be a mix of &lt;td&gt; and &lt;th&gt; elements."><code>&lt;tr&gt;</code></a> element data-rows to be the body of its parent <a href="/en-US/docs/Web/HTML/Element/table" title="The HTML Table Element (&lt;table&gt;) represents data in two dimensions or more."><code>&lt;table&gt;</code></a> element (as long as no &lt;tr&gt; elements are immediate children of that table element.)&#xA0; In conjunction with a preceding <a href="/en-US/docs/Web/HTML/Element/thead" title="The HTML Table Head Element (&lt;thead&gt;) defines a set of rows defining the head of the columns of the table."><code>&lt;thead&gt;</code></a> and/or <a href="/en-US/docs/Web/HTML/Element/tfoot" title="The HTML Table Foot Element (&lt;tfoot&gt;) defines a set of rows summarizing the columns of the table."><code>&lt;tfoot&gt;</code></a> element, &lt;tbody&gt; provides additional semantic information for devices such as printers and displays. Of the parent table&apos;s child elements, &lt;tbody&gt; represents the content which, when longer than a page, will most likely differ for each page printed; while the content of <a href="/en-US/docs/Web/HTML/Element/thead" title="The HTML Table Head Element (&lt;thead&gt;) defines a set of rows defining the head of the columns of the table."><code>&lt;thead&gt;</code></a> and <a href="/en-US/docs/Web/HTML/Element/tfoot" title="The HTML Table Foot Element (&lt;tfoot&gt;) defines a set of rows summarizing the columns of the table."><code>&lt;tfoot&gt;</code></a> will be the same or similar for each page printed. For displays, &lt;tbody&gt; will enable separate scrolling of the <a href="/en-US/docs/Web/HTML/Element/thead" title="The HTML Table Head Element (&lt;thead&gt;) defines a set of rows defining the head of the columns of the table."><code>&lt;thead&gt;</code></a>, <a href="/en-US/docs/Web/HTML/Element/tfoot" title="The HTML Table Foot Element (&lt;tfoot&gt;) defines a set of rows summarizing the columns of the table."><code>&lt;tfoot&gt;</code></a>, and <a href="/en-US/docs/Web/HTML/Element/caption" title="The HTML &lt;caption&gt; Element (or HTML Table Caption Element) represents the title of a table. Though it is always the first descendant of a &lt;table&gt;, its styling, using CSS, may place it elsewhere, relative to the table."><code>&lt;caption&gt;</code></a> elements of the same parent <a href="/en-US/docs/Web/HTML/Element/table" title="The HTML Table Element (&lt;table&gt;) represents data in two dimensions or more."><code>&lt;table&gt;</code></a> element.&#xA0; Note that unlike the &lt;thead&gt;, &lt;tfoot&gt;, and &lt;caption&gt; elements however, multiple<strong>&#xA0;</strong><span style="font-family: consolas,monaco,andale mono,monospace;">&lt;tbody&gt; </span>elements are permitted (if consecutive), allowing the data-rows in long tables to be divided into different sections, each separately formatted as needed.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/td" title="The Table cell HTML element (&lt;td&gt;) defines a cell of a table that contains data. It participates in the table model."><code>&lt;td&gt;</code></a></td> 
   <td>The <em>Table cell</em> <a href="/en-US/docs/Web/HTML">HTML</a> element (<strong><code>&lt;td&gt;</code></strong>) defines a cell of a table that contains data. It participates in the <em>table model</em>.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/tfoot" title="The HTML Table Foot Element (&lt;tfoot&gt;) defines a set of rows summarizing the columns of the table."><code>&lt;tfoot&gt;</code></a></td> 
   <td>The <em>HTML Table Foot Element</em> (<code>&lt;tfoot&gt;</code>) defines a set of rows summarizing the columns of the table.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/th" title="The HTML element table header cell &lt;th&gt; defines a cell as header of a group of table cells. The exact nature of this&#xA0;group&#xA0;is defined by the scope and headers attributes."><code>&lt;th&gt;</code></a></td> 
   <td>The HTML element <em>table header cell</em> <code>&lt;th&gt;</code> defines a cell as header of a group of table cells. The exact nature of this&#xA0;group&#xA0;is defined by the <code><a href="/en-US/docs/Web/HTML/Element/th#attr-scope">scope</a></code> and <code><a href="/en-US/docs/Web/HTML/Element/th#attr-headers">headers</a></code> attributes.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/thead" title="The HTML Table Head Element (&lt;thead&gt;) defines a set of rows defining the head of the columns of the table."><code>&lt;thead&gt;</code></a></td> 
   <td>The <em>HTML Table Head Element</em> (<code>&lt;thead&gt;</code>) defines a set of rows defining the head of the columns of the table.</td> 
  </tr> 
 
  <tr> 
 
   <td style="vertical-align: top;"><a href="/en-US/docs/Web/HTML/Element/tr" title="The HTML element&#xA0;table row &lt;tr&gt;&#xA0;defines a row of cells in a table. Those can be a mix of &lt;td&gt; and &lt;th&gt; elements."><code>&lt;tr&gt;</code></a></td> 
   <td>The HTML element<em>&#xA0;table row </em><code>&lt;tr&gt;</code>&#xA0;defines a row of cells in a table. Those can be a mix of <a href="/en-US/docs/Web/HTML/Element/td" title="The Table cell HTML element (&lt;td&gt;) defines a cell of a table that contains data. It participates in the table model."><code>&lt;td&gt;</code></a> and <a href="/en-US/docs/Web/HTML/Element/th" title="The HTML element&#xA0;table header cell &lt;th&gt;&#xA0;defines a cell that is a header for a group of cells of a table. The group of cells that the header refers to is defined by the scope and headers attribute."><code>&lt;th&gt;</code></a> elements.</td> 
  </tr> 
 
 </tbody> 
</table>
"""
  expected_markdown = """
|Element|Description|
|---|---|
|<`<caption>`>|The **HTML `<caption>` Element** (or *HTML Table Caption Element*) represents the title of a table. Though it is always the first descendant of a <`<table>`>, its styling, using CSS, may place it elsewhere, relative to the table.|
|<`<col>`>|The *HTML Table Column Element* (**<col>**) defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a <`<colgroup>`> element.|
|<`<colgroup>`>|The *HTML Table Column Group Element* (**<colgroup>**) defines a group of columns within a table.|
|<`<table>`>|The **HTML Table Element** (`<table>`) represents tabular data - i.e., information expressed via a two dimensional data table.|
|<`<tbody>`>|The HTML **Table Body Element (<tbody>)** defines one or more <`<tr>`> element data-rows to be the body of its parent <`<table>`> element (as long as no <tr> elements are immediate children of that table element.)  In conjunction with a preceding <`<thead>`> and/or <`<tfoot>`> element, <tbody> provides additional semantic information for devices such as printers and displays. Of the parent table's child elements, <tbody> represents the content which, when longer than a page, will most likely differ for each page printed; while the content of <`<thead>`> and <`<tfoot>`> will be the same or similar for each page printed. For displays, <tbody> will enable separate scrolling of the <`<thead>`>, <`<tfoot>`>, and <`<caption>`> elements of the same parent <`<table>`> element.  Note that unlike the <thead>, <tfoot>, and <caption> elements however, multiple** **<tbody> elements are permitted (if consecutive), allowing the data-rows in long tables to be divided into different sections, each separately formatted as needed.|
|<`<td>`>|The *Table cell* <HTML> element (**`<td>`**) defines a cell of a table that contains data. It participates in the *table model*.|
|<`<tfoot>`>|The *HTML Table Foot Element* (`<tfoot>`) defines a set of rows summarizing the columns of the table.|
|<`<th>`>|The HTML element *table header cell* `<th>` defines a cell as header of a group of table cells. The exact nature of this group is defined by the `<scope>` and `<headers>` attributes.|
|<`<thead>`>|The *HTML Table Head Element* (`<thead>`) defines a set of rows defining the head of the columns of the table.|
|<`<tr>`>|The HTML element* table row *`<tr>` defines a row of cells in a table. Those can be a mix of <`<td>`> and <`<th>`> elements.|


"""
  markdown = converters.Html2Markdown().convert(html)
  assert markdown == expected_markdown
