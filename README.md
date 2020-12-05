# pycmarkgfm

Lightweight Python bindings to GitHub Flavored Markdown (GFM) library, [cmark-gfm](https://github.com/github/cmark-gfm),
with enhanced support for task lists.

## Features

* By design, rendering is compliant with GitHub's, since this package wraps GitHub's own C parser and serializer.  
* As opposed to most cmark-gfm bindings out there, this package supports
  [parsing and toggling task lists](#dealing-with-task-lists).
* Compatibility: 
  [![](https://github.com/Zopieux/pycmarkgfm/workflows/Test%20and%20package/badge.svg)](https://github.com/Zopieux/pycmarkgfm/actions?query=workflow%3A%22Test+and+package%22) 
  with Python 3.5, 3.6, 3.7, 3.8, 3.9 on Linux-like platforms. If you need Windows support, please contribute a PR.

## Installation

This packages is [available on PyPi](https://pypi.org/project/pycmarkgfm/).

    $ pip install pycmarkgfm

## Usage

```python
import pycmarkgfm

# CommonMark (not GitHub flavored):
html = pycmarkgfm.markdown_to_html("Hello *world*")

# GitHub flavored Markdown:
html = pycmarkgfm.gfm_to_html("Hello ~world~")
```

### Options

cmark and cmark-gfm come with a bunch of customization options (also known as *flags*) which are made available through
the [`pycmarkgfm.options` module](pycmarkgfm/options.py). To use one or multiple options, use the `options=` argument 
with a mask (bitwise-or combination) of `pycmarkgfm.options`. Each option is documented.

```python
text = "hello\n<img src='doge.png'>"

print(pycmarkgfm.markdown_to_html(text))
# <p>hello
# <!-- raw HTML omitted --></p>

from pycmarkgfm import options
print(pycmarkgfm.markdown_to_html(text, options=options.unsafe | options.hardbreaks))
# <p>hello<br />
# <img src='doge.png'></p>
``` 

### Dealing with task lists

One of the distinctive features of this package is support for task lists.
You can get the list of tasks with their checked state, and update that state before rendering:

```python
import pycmarkgfm

md = """
- [ ] eggs
- [x] milk
"""

with pycmarkgfm.parse_gfm(md) as document: 
    eggs, milk = document.get_tasks()
    assert not eggs.checked
    assert milk.checked

    # Toggle! 
    eggs.checked = True
    print(document.to_commonmark())
    # - [x] eggs
    # - [x] milk
``` 

There is a convenience method to easily toggle a task state from the rendered HTML. The typical use-case is that your
database stores the source GFM, renders it to HTML with `gfm_to_html()`, then you have some client Javascript snippet
that is invoked when a checkbox is clicked. Thanks to the unique `data-gfm-task` HTML attribute, you can update the 
source GFM on the server:

```python
import pycmarkgfm

md = """
- [ ] eggs
- [x] milk
"""

print(pycmarkgfm.gfm_to_html(md))
# <ul>
# <li data-gfm-task="2:1-2:10"><input type="checkbox" disabled="" /> eggs</li>
# <li data-gfm-task="3:1-3:10"><input type="checkbox" checked="" disabled="" /> milk</li>
# </ul>

# When user clicks a checkbox, get the parent 'data-gfm-task', then on the server, do:
new_md = pycmarkgfm.gfm_toggle_task_by_id(md, "2:1-2:10", checked=pycmarkgfm.TOGGLE)
print(new_md)
# - [x] eggs
# - [x] milk
```
 
You can also use `checked=True/False` instead of `TOGGLE` to force a particular state.

### How is this package different from `cmarkgfm`?

[cmarkgfm](https://pypi.org/project/cmarkgfm/) is similar to this package, in fact cmarkgfm's cffi build script
is partially re-used in this project – in compliance with its MIT license.

As of October 2020, cmarkgfm is still a well-maintained project and I recommend using it if you don't need the extra
features provided by pycmarkgfm, most notably the support for task lists.

## License

GNU GPLv3.

The project includes components under a different copyright under the [third_party](./third_party/) directory.
