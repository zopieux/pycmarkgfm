from pycmarkgfm import _cmark  # type: ignore

default = _cmark.lib.CMARK_OPT_DEFAULT
"""Default options."""

sourcepos = _cmark.lib.CMARK_OPT_SOURCEPOS
"""Include a `data-sourcepos` attribute on all block elements."""

hardbreaks = _cmark.lib.CMARK_OPT_HARDBREAKS
"""Render `softbreak` elements as hard line breaks."""

unsafe = _cmark.lib.CMARK_OPT_UNSAFE
"""Render raw HTML and unsafe links (`javascript:`, `vbscript:`, `file:`, and `data:`, except for `image/png`, 
`image/gif`, `image/jpeg`, or `image/webp` mime types).  By default, raw HTML is replaced by a placeholder HTML 
comment. Unsafe links are replaced by empty strings."""

nobreaks = _cmark.lib.CMARK_OPT_NOBREAKS
"""Render `softbreak` elements as spaces."""

validate_utf8 = _cmark.lib.CMARK_OPT_VALIDATE_UTF8
"""Validate UTF-8 in the input before parsing, replacing illegal sequences with the replacement character U+FFFD."""

smart = _cmark.lib.CMARK_OPT_SMART
"""Convert straight quotes to curly, --- to em dashes, -- to en dashes."""

github_pre_lang = _cmark.lib.CMARK_OPT_GITHUB_PRE_LANG
"""Use GitHub-style <pre lang="x"> tags for code blocks instead of <pre><code class="language-x">."""

liberal_html_tag = _cmark.lib.CMARK_OPT_LIBERAL_HTML_TAG
"""Be liberal in interpreting inline HTML tags."""

footnotes = _cmark.lib.CMARK_OPT_FOOTNOTES
"""Parse footnotes."""

strikethrough_double_tilde = _cmark.lib.CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE
"""Only parse strikethroughs if surrounded by exactly 2 tildes. Gives some compatibility with redcarpet."""

table_prefer_style_attributes = _cmark.lib.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES
"""Use style attributes to align table cells instead of align attributes."""

full_info_string = _cmark.lib.CMARK_OPT_FULL_INFO_STRING
"""Include the remainder of the info string in code blocks in a separate attribute."""
