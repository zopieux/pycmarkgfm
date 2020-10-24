from pycmarkgfm import cmark


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
