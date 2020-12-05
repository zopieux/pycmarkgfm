from pycmarkgfm import cmark, options


def test_markdown_to_html():
    assert (
        cmark.markdown_to_html(
            """
Hello *world*. This is ~nice~.

# A nice heading

- [ ] I am
- [ ] a list
"""
        )
        == """<p>Hello <em>world</em>. This is ~nice~.</p>
<h1>A nice heading</h1>
<ul>
<li>[ ] I am</li>
<li>[ ] a list</li>
</ul>
"""
    )


def test_gfm_to_html():
    assert (
        cmark.gfm_to_html(
            """
Hello *world*. This is ~deleted~.

# A nice heading

- [ ] I am
- [x] a tasklist with a [http://example.org](https://example.com)
"""
        )
        == """<p>Hello <em>world</em>. This is <del>deleted</del>.</p>
<h1>A nice heading</h1>
<ul>
<li data-gfm-task="6:1-6:10"><input type="checkbox" disabled="" /> I am</li>
<li data-gfm-task="7:1-7:65"><input type="checkbox" checked="" disabled="" /> a tasklist with a <a href="https://example.com">http://example.org</a></li>
</ul>
"""
    )


def test_gfm_get_tasklist():
    text = """
- [ ] I am
- [x] a tasklist
"""
    with cmark.parse_gfm(text) as document:
        tasks = list(document.get_tasks())
        assert len(tasks) == 2
        assert tasks[0].identifier == "2:1-2:10"
        assert tasks[0].checked is False
        assert tasks[1].identifier == "3:1-3:16"
        assert tasks[1].checked is True


def test_gfm_toggle_tasklist_noop():
    text = """
Text.

- [ ] I am
- [x] a tasklist

Extra text.
"""
    assert (
        cmark.gfm_toggle_task_by_id(text, "does-not-exist", False).strip()
        == text.strip()
    )
    assert cmark.gfm_toggle_task_by_id(text, "2:1-2:10", False).strip() == text.strip()


def test_gfm_toggle_tasklist():
    text = """
- [ ] I am
- [x] a tasklist
"""
    assert (
        cmark.gfm_toggle_task_by_id(text, "2:1-2:10", True).strip()
        == """
- [x] I am
- [x] a tasklist
""".strip()
    )

    assert (
        cmark.gfm_toggle_task_by_id(text, "3:1-3:16", cmark.TOGGLE).strip()
        == """
- [ ] I am
- [ ] a tasklist
""".strip()
    )


def test_option_sourcepos():
    text = "# Foo\n\nBar."
    html = cmark.markdown_to_html(text, options=options.sourcepos)
    assert 'data-sourcepos="1' in html
    assert html != cmark.markdown_to_html(text)


def test_option_hardbreaks():
    text = "Line 1.\nLine 2.\n"
    assert cmark.markdown_to_html(text) == "<p>Line 1.\nLine 2.</p>\n"
    html = cmark.markdown_to_html(text, options=options.hardbreaks)
    assert html == "<p>Line 1.<br />\nLine 2.</p>\n"


def test_option_unsafe():
    text = "Line. <img src='doge.png'> Line."
    assert (
        cmark.markdown_to_html(text) == "<p>Line. <!-- raw HTML omitted --> Line.</p>\n"
    )
    html = cmark.markdown_to_html(text, options=options.unsafe)
    assert html == "<p>Line. <img src='doge.png'> Line.</p>\n"


def test_option_nobreaks():
    text = "Line 1.\nLine 2.\n"
    html = cmark.markdown_to_html(text, options=options.nobreaks)
    assert html == "<p>Line 1. Line 2.</p>\n"


def test_option_smart():
    text = 'She said --- "Smart -- but not too wise".'
    assert (
        cmark.markdown_to_html(text)
        == "<p>She said --- &quot;Smart -- but not too wise&quot;.</p>\n"
    )
    html = cmark.markdown_to_html(text, options=options.smart)
    assert html == "<p>She said \N{EM DASH} “Smart \N{EN DASH} but not too wise”.</p>\n"


def test_option_github_pre_lang():
    text = """Some code.

```c
int main(void) { return 42; }
```"""
    assert (
        cmark.markdown_to_html(text)
        == '<p>Some code.</p>\n<pre><code class="language-c">int main(void) { return 42; }\n</code></pre>\n'
    )
    html = cmark.markdown_to_html(text, options=options.github_pre_lang)
    assert (
        html
        == '<p>Some code.</p>\n<pre lang="c"><code>int main(void) { return 42; }\n</code></pre>\n'
    )


def test_option_footnotes():
    text = """Woke up on the wrong foot[^1].\n\n[^1]: Note."""
    assert (
        cmark.markdown_to_html(text)
        == '<p>Woke up on the wrong foot<a href="Note.">^1</a>.</p>\n'
    )
    html = cmark.markdown_to_html(text, options=options.footnotes)
    assert '<sup class="footnote-ref"><a href="#fn1" id="fnref1">1</a>' in html
    assert '<li id="fn1">\n<p>Note. <a href="#fnref1"' in html


def test_option_strikethrough_double_tilde():
    text = """This is ~so~ ~~very~~ extremely smart."""
    assert (
        cmark.gfm_to_html(text)
        == "<p>This is <del>so</del> <del>very</del> extremely smart.</p>\n"
    )
    html = cmark.gfm_to_html(text, options=options.strikethrough_double_tilde)
    assert html == "<p>This is ~so~ <del>very</del> extremely smart.</p>\n"
