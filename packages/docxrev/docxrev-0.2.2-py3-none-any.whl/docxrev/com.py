"""
Classes that expose aspects of the Microsoft Word Component Object Model (COM).
"""

from __future__ import annotations

import pathlib
import shutil
from collections import abc
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Callable, Dict, Iterator, List, Optional, Union
from warnings import warn

import pywintypes
import win32com.client
from win32com.client import constants

# * -------------------------------------------------------------------------------- * #
# * SETUP

# Get the instance of Word running on this machine. Start it if necessary.
try:
    COM_WORD = win32com.client.gencache.EnsureDispatch("Word.Application")
except AttributeError:
    # We end up here if this cryptic error occurs.
    # https://stackoverflow.com/questions/52889704/python-win32com-excel-com-model-started-generating-errors
    # https://mail.python.org/pipermail/python-win32/2007-August/006147.html
    shutil.rmtree(win32com.__gen_path__)
    COM_WORD = win32com.client.gencache.EnsureDispatch("Word.Application")

# * -------------------------------------------------------------------------------- * #
# * CLASSES * #


class Document(AbstractContextManager):
    """A Word document.

    Represents a Word document. Certain attributes, such as ``name``, are always
    available. Others are only available "in context". Throughout this documentation,
    "in context" means that the object is being handled by a context manager. For
    example, an object is "in context" inside an indented block beneath a ``with <item>
    [as <target>]:`` clause.

    The context-specific attribute ``com`` exposes the ``win32com.<...>.Document`` class
    directly, a COM object representation of the document which has slightly different
    syntax and access rules than regular Python. For example, collections are
    one-indexed rather than zero-indexed. The ``comments`` attribute exposes certain
    aspects of the ``win32com.<...>.Comments`` class in a convenient, Pythonic
    :py:class:`Comments` class.

    Parameters
    ----------
    path: Union[str, pathlib.Path]
        Path to the document. May be a string.
    save_on_exit: Optional[bool]
        Whether to save the document when leaving context. Informs the attribute
        :py:attr:`save_on_exit`.  **Default**: True.
    close_on_exit: Optional[bool]
        Whether to close the document when leaving context. Informs the attribute
        :py:attr:`close_on_exit`. **Default**: Closes documents that were not already
        open.

    Attributes
    ----------
    com: win32com.<...>.Document
        The COM object representation of the document. Only exists in context.
        :py:class:`AttributeError` is raised when attempting to access it out of
        context.
    comments: Comments
        The comments in the document. Only exists in context. :py:class:`AttributeError`
        is raised when attempting to access it out of context.
    name: str
        The filename of the document.
    save_on_exit: bool
        Informed by the parameter ``save_on_exit``.
    close_on_exit: bool
        Informed by the parameter ``close_on_exit``.
    """

    def __init__(
        self,
        path: Union[str, pathlib.Path],
        save_on_exit: Optional[bool] = True,
        close_on_exit: Optional[bool] = None,
    ):

        self.path = pathlib.Path(path)
        self.name = self.path.name
        self.save_on_exit = save_on_exit
        self.close_on_exit = close_on_exit

        # Check if the document is already open, set close_on_exit accordingly
        if self.close_on_exit is None:
            already_open_documents = [doc.Name for doc in COM_WORD.Documents]
            if self.path.name in already_open_documents:
                self.close_on_exit = False
            else:
                self.close_on_exit = True

        # Track nested levels of context
        self.context_count = 0

    def __getattr__(self, name):
        """Only called on an ``AttributeError``. Handle context-specific attributes."""

        if name in {"com", "comments"}:
            message = "Attribute only exists in context."
        else:
            message = None

        raise AttributeError(message)

    def __enter__(self) -> Document:
        """Activate the document and enforce visibility when entering context."""

        self.context_count += 1
        visible_on_enter = not self.close_on_exit

        # These attributes are meant to only exist in context
        # pylint: disable=attribute-defined-outside-init
        self.com = COM_WORD.Documents.Open(
            str(self.path.resolve()), Visible=visible_on_enter
        )
        self.comments = Comments(self)
        # pylint: enable=attribute-defined-outside-init

        self.com.Activate()
        self.com.ActiveWindow.Visible = visible_on_enter  # enforce visibility

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Optionally save and close the document when leaving the outermost context."""

        if self.context_count > 1:
            self.context_count -= 1
        else:
            self.context_count = 0  # Probably redundant, but let's be explicit

            if self.save_on_exit:
                self.com.Save()

            if self.close_on_exit:
                self.com.Close(SaveChanges=False)

            del self.com, self.comments  # Delete context-specific attributes

    def delete_comments(self):
        """Delete all comments in the document."""

        warning_message = (
            "Cannot delete all comments."
            " There may have been no comments in the first place."
        )

        with self:
            try_com(
                com_method=self.com.DeleteAllComments,
                except_errors=ERRORS["command_not_available"],
                messages=warning_message,
            )


class Comments(abc.Sequence):
    """The comments in an open Word document.

    Parameters
    ----------
    document: Document
        The document from which to retrieve comments.  Informs the attribute
        :py:attr:`in_document`.

    Attributes
    ----------
    in_document: Document
        The document in which the comments reside. Informed by the parameter
        ``document``.
    com: win32com.<...>.Comments
        The COM object representation of the comments.
    """

    def __init__(self, document: Document):
        self.in_document = document
        self.com = self.in_document.com.Comments

    def __getitem__(self, index):  # pylint: disable=inconsistent-return-statements
        """Get comments.

        The native COM object is one-indexed and has nothing analogous to Python's
        ``slice`` indexing. This method enables zero-indexed, single-item or ``slice``
        access to :py:class:`Comment` instances in :py:class:`Comments`.
        """

        if isinstance(index, int):
            key = index
            com_comment = self.com(key + 1)  # COM is 1-indexed
            comment = Comment(com_comment, self)
            return comment

        if isinstance(index, slice):
            keys = range(*index.indices(len(self)))  # coerce keys to object bounds
            comments = [self[key] for key in keys]  # recursive call on each key
            return comments

    def __iter__(self) -> Iterator:
        return (Comment(com_comment, self) for com_comment in self.com)

    def __len__(self) -> int:
        return len(self.com)


class Comment:
    """A comment in an open Word document.

    Parameters
    ----------
    com_comment: win32com.<...>.Comment
        The COM object representation of the comment. Informs the attribute
        :py:attr:`com`.
    comments
        The list of comments in which this comment resides. Informs the attribute
        :py:attr:`in_comments`.

    Attributes
    ----------
    in_comments: Comments
        The list of comments in which this comment resides. Informed by the parameter
        ``comments``.
    in_document: Document
        The document in which this comment resides.
    com: win32com.<...>.Comment
        The COM object representation of the comment. Informed by the parameter
        ``com_comment``.
    """

    def __init__(self, com_comment, comments):
        self.com = com_comment
        self.in_comments = comments
        self.in_document = self.in_comments.in_document

    @property
    def range(self):
        """
        :win32com.<...>.Range: Convenience property returning this
        comment's range.
        """
        return Range(self.com.Range)

    @property
    def text(self):
        """:str: Convenience property returning this comment's text."""
        return self.range.text

    def delete(self):
        """Delete the comment and its children."""
        self.com.DeleteRecursively()

    def update(self, text: str):
        """Update the text of the comment.

        Parameters
        ----------
        text: str
            The full text replacement of the comment.
        """

        # Shorthand to various COM objects
        com_active_window = self.in_document.com.ActiveWindow
        com_active_selection = com_active_window.Selection
        original_cursor_position = com_active_selection.Range

        # Check whether the cursor is inside any comment
        com_active_window.Panes(1).Activate()  # Ensure we're in the main pane
        cursor_in_any_comment = (
            original_cursor_position.StoryType == constants.wdCommentsStory
        )
        # If it is, move the cursor to the text that the particular comment is
        # referencing. Note that this is *a* comment, not necessarily *this* comment.
        # This sidesteps an issue where a comment range cannot be selected while the
        # cursor is inside another comment.
        if cursor_in_any_comment:
            com_active_selection.Comments(1).Reference.Select()
            com_active_selection.Font.Reset()  # Prevent leaking comment's font format
            original_cursor_position = com_active_selection.Range

        # Select and replace the text of the comment
        self.range.com.Select()
        com_active_selection.Text = text

        # Restore print view and cursor position
        com_active_window.ActivePane.Close()  # Close the comments pane that comes up
        com_active_window.ActivePane.View.Type = constants.wdPrintView
        original_cursor_position.Select()


class Range:
    """A text range in an open Word document.

    Parameters
    ----------
    com_range: win32com.<...>.Range
        The COM object representation of the text range. Informs the attribute
        :py:attr:`com`.

    Attributes
    ----------
    com: win32com.<...>.Range
        The COM object representation of the text range. Informed by the parameter
        ``com_range``.
    """

    @property
    def text(self) -> str:
        """:str: Convenience property returning thisrange's text."""
        return self.com.Text

    def __init__(self, com_range):
        self.com = com_range


# * -------------------------------------------------------------------------------- * #
# * COM ERROR HANDLING * #


@dataclass
class ComError:
    """Represents a COM Error by a unique identifying pair of ``hresult`` and ``scode``.

    See EXCEPINFO documentation for reference.
    https://docs.microsoft.com/en-us/windows/win32/api/oaidl/ns-oaidl-excepinfo
    """

    hresult: int
    """An error identifier. Negative in case of an error."""

    scode: int
    """A more specific error identifier. Negative in case of an error."""


def try_com(
    com_method: Callable,
    except_errors: Optional[Union[ComError, List[ComError]]] = None,
    messages: Optional[Union[str, List[str]]] = None,
    **kwargs,
):
    """Try a COM method, warn about specified COM errors, and raise the rest.

    This function tries a COM method specified by ``com_method``, catching generic COM
    errors and handling specific cases. COM errors are specified by a
    :py:class:`ComError` instance rather than a Python exception type. In order to catch
    a specific error, supply the :py:class:`ComError` specification of the error and the
    ``message`` to be displayed as a warning when the error is first caught. The
    ``except_errors`` and ``messages`` parameters also accept lists of errors to convert
    to warnings. If no message is provided, only the generic COM error will appear in
    the warning.

    Parameters
    ----------
    com_method
        The COM method.
    except_errors
        Error or list of errors to convert to warnings, as specified as
        :py:class:`ComError` instance(s). **Default:** Don't convert any errors to
        warnings.
    messages
        Warning or list of warnings to be printed when the error(s) is/are caught.
        **Default:** Just print the generic COM errors as warnings.
    **kwargs
        The keyword arguments to be passed to the COM method.

    Returns
    -------
    Any
        Whatever is returned from the COM method.
    """

    if not except_errors:
        except_errors = []
    elif not isinstance(except_errors, list):
        except_errors = [except_errors]

    if not messages:
        messages = [""] * len(except_errors)
    if not isinstance(messages, list):
        messages = [messages]

    try:
        returns = com_method(**kwargs)

    except pywintypes.com_error as error:  # pylint: disable=no-member
        returns = None
        error_caught = False
        for except_error, user_message in zip(except_errors, messages):
            if (
                error.hresult == except_error.hresult
                and error.excepinfo[-1] == except_error.scode
            ):
                com_error_message = f"COM Error: {error}"
                if user_message:
                    message = user_message + " " + com_error_message
                else:
                    message = com_error_message
                warn(message)
                error_caught = True

        if not error_caught:
            raise error

    return returns


ERRORS: Dict[str, ComError] = {
    "command_not_available": ComError(-2147352567, -2146823683)
}
""":Dict[str, ComError]: A :py:class:`dict` of named :py:class:`ComError` errors."""
