import contextlib
from typing import Optional, Iterable, Union, ContextManager, Iterator

from pycmarkgfm import _cmark  # type: ignore

# Sentinel object for toggling task state.
TOGGLE = object()

GFM_EXTENSIONS = [
    "autolink",
    "strikethrough",
    "table",
    "tagfilter",
    "tasklist",
]


class CMarkException(Exception):
    pass


class Document:
    class Iterator:
        def __init__(self, root):
            self.it = _cmark.lib.cmark_iter_new(root)

        def __del__(self):
            _cmark.lib.cmark_iter_free(self.it)

        def __next__(self):
            event_type = _cmark.lib.cmark_iter_next(self.it)
            if event_type == _cmark.lib.CMARK_EVENT_DONE:
                raise StopIteration()
            return event_type, _cmark.lib.cmark_iter_get_node(self.it)

    class TaskNode:
        def __init__(self, node):
            self.node = node

        @property
        def checked(self) -> bool:
            return _cmark.lib.cmark_gfm_extensions_get_tasklist_item_checked(self.node)

        @checked.setter
        def checked(self, checked: bool):
            _cmark.lib.cmark_gfm_extensions_set_tasklist_item_checked(
                self.node, checked
            )

        @property
        def identifier(self) -> str:
            return "{}:{}-{}:{}".format(
                _cmark.lib.cmark_node_get_start_line(self.node),
                _cmark.lib.cmark_node_get_start_column(self.node),
                _cmark.lib.cmark_node_get_end_line(self.node),
                _cmark.lib.cmark_node_get_end_column(self.node),
            )

        def __repr__(self):
            return "<TaskNode {} ID '{}'>".format(
                "checked" if self.checked else "unchecked", self.identifier
            )

    def __init__(self, parser, options, root):
        self.parser = parser
        self.options = options
        self.root = root

    def __iter__(self):
        return Document.Iterator(self.root)

    def get_tasks(self) -> Iterable["Document.TaskNode"]:
        for event, node in self:
            if event == _cmark.lib.CMARK_EVENT_EXIT:
                type_str = _cmark.ffi.string(
                    _cmark.lib.cmark_node_get_type_string(node)
                )
                if type_str == b"tasklist":
                    yield Document.TaskNode(node)

    def get_task_by_id(self, identifier: str) -> Optional["Document.TaskNode"]:
        """Returns the TaskNode identified by 'identifier', or None if doesn't exist.

        :param identifier: the task identifier
        :return: the corresponding TaskNode, or None
        """
        return next(
            (task for task in self.get_tasks() if task.identifier == identifier),
            None,
        )

    def to_html(self) -> str:
        """Renders the document to HTML."""
        extensions = _cmark.lib.cmark_parser_get_syntax_extensions(self.parser)
        if extensions is None:
            extensions = _cmark.ffi.NULL
        raw_result = _cmark.lib.cmark_render_html(self.root, self.options, extensions)
        return _cmark.ffi.string(raw_result).decode("utf-8")

    def to_commonmark(self, width=0) -> str:
        """Renders the document to CommonMark."""
        raw_result = _cmark.lib.cmark_render_commonmark(self.root, self.options, width)
        return _cmark.ffi.string(raw_result).decode("utf-8")


@contextlib.contextmanager
def parse_markdown(
    text: str, options: int = 0, extensions: Optional[Iterable[str]] = None
) -> Iterator["Document"]:
    """Parses CommonMark into a Document.

    :param text: source Markdown (CommonMark)
    :param options: options flags, passed to cmark-gfm
    :param extensions: extension names to use
    :return: a Document
    """

    def find_syntax_extension(name: str):
        encoded_name = name.encode("utf-8")
        extension = _cmark.lib.cmark_find_syntax_extension(encoded_name)
        if extension == _cmark.ffi.NULL:
            return None
        return extension

    def load_extensions(extension_names: Iterable[str]):
        _cmark.lib.cmark_gfm_core_extensions_ensure_registered()

        for extension_name in extension_names:
            extension = find_syntax_extension(extension_name)
            if extension is None:
                raise CMarkException("Unknown extension '{}'".format(extension_name))
            yield extension

    loaded_extensions = load_extensions(extensions or [])
    parser = _cmark.lib.cmark_parser_new(options)

    for extension in loaded_extensions:
        _cmark.lib.cmark_parser_attach_syntax_extension(parser, extension)

    encoded_text = text.encode("utf-8")
    _cmark.lib.cmark_parser_feed(parser, encoded_text, len(encoded_text))
    root = _cmark.lib.cmark_parser_finish(parser)
    if _cmark.lib.cmark_node_get_type(root) == _cmark.lib.CMARK_NODE_NONE:
        _cmark.lib.cmark_parser_free(parser)
        raise CMarkException("Error parsing markdown")

    yield Document(parser, options, root)

    _cmark.lib.cmark_parser_free(parser)


def parse_gfm(text: str, options: int = 0) -> ContextManager[Document]:
    """Parses GitHub Flavored Markdown into a Document.

    :param text: source Markdown (GFM)
    :param options: options flags, passed to cmark-gfm
    :return: a Document
    """
    return parse_markdown(
        text,
        options,
        extensions=GFM_EXTENSIONS,
    )


def markdown_to_html(
    text: str, options: int = 0, extensions: Optional[Iterable[str]] = None
) -> str:
    """Renders CommonMark to HTML.

    :param text: source Markdown (CommonMark)
    :param options: options flags, passed to cmark-gfm
    :param extensions: extension names to use
    :return: HTML string
    """
    with parse_markdown(text, options, extensions) as document:
        return document.to_html()


def gfm_to_html(text: str, options: int = 0) -> str:
    """Renders GitHub Flavored Markdown to HTML.

    :param text: source Markdown (GFM)
    :param options: options flags, passed to cmark-gfm
    :return: HTML string
    """
    with parse_gfm(text, options) as document:
        return document.to_html()


def gfm_toggle_task_by_id(
    text: str, task_id: str, checked: Union[bool, object] = TOGGLE, options: int = 0
) -> str:
    """Returns 'text' modified with 'task_id' task toggled to state 'checked'.

    If the specified task does not exist, this is a no-op.

    Warning: this function does a parse+serialize round, so as a side-effect
    the returned CommonMark is a *normalized* version of 'text', as if you did::

        with parse_gfm(text) as doc:
            return doc.to_commonmark()

    :param text: Markdown source to modify
    :param task_id: the task identifier (`data-gfm-task` in HTML) to toggle
    :param checked: True, False or the special `pycmarkgfm.TOGGLE` value to toggle
    :param options: cmark options
    :return: a CommonMark string similar to the source 'text' but with the task toggled.
    """
    with parse_gfm(text, options) as document:
        task = document.get_task_by_id(task_id)
        if task is None:
            return text
        if checked is TOGGLE:
            task.checked = not task.checked
        else:
            task.checked = bool(checked)
        return document.to_commonmark()
