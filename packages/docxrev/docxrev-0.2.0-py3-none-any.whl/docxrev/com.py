"""
Classes that expose aspects of the Microsoft Word Component Object Model (COM) for
Microsoft Word.
"""

import pathlib
import shutil
from collections import abc
from contextlib import AbstractContextManager, nullcontext
from dataclasses import dataclass
from typing import Callable, List, Optional, Union
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


@dataclass
class ComError:
    """Represents a COM Error with uniquely identifying `hresult` and `scode`.

    See EXCEPINFO documenation for reference.

    https://docs.microsoft.com/en-us/windows/win32/api/oaidl/ns-oaidl-excepinfo

    Parameters
    ----------
    hresult: int
        An error identifier. A result handle that returns negative for an error.
    scode:
        Another error identifier. A return value that describes the error.
    """

    hresult: int
    scode: int


# Hresults for COM errors
errors = {"command_not_available": ComError(-2147352567, -2146823683)}

# * -------------------------------------------------------------------------------- * #
# * CLASSES * #


class Document(AbstractContextManager):
    """An open Word document.

    Parameters
    ----------
    path
        Path to the document.
    save_on_exit
        Whether to save the document when exiting a `with` context.
    close_on_exit
        Whether to close the document when exiting a `with` context. By default, closes
        documents that were not already open.

    Attributes
    ----------
    path
        Path to the document, guaranteed to be a `pathlib.Path`.
    com
        The COM object representation of the document. Only exists in a `with` context.
    comments
        The comments in the document. Only exists when in a `with` context.
    context_count
        The count of nested contexts. Ensures only the outermost context wraps up.
    """

    def __init__(
        self,
        path: Union[str, pathlib.Path],
        save_on_exit: bool = True,
        close_on_exit: Optional[bool] = None,
    ):

        self.path = pathlib.Path(path)
        self.save_on_exit = save_on_exit
        self.close_on_exit = close_on_exit

        # Check if the document is already open, set close_on_exit accordingly
        if self.close_on_exit is None:
            already_open_documents = [doc.Name for doc in COM_WORD.Documents]
            if self.path.name in already_open_documents:
                self.close_on_exit = False
            else:
                self.close_on_exit = True

        # These attributes only exist in context of a `with` block
        self.context_count = 0
        self.com = None
        self.name = None
        self.comments = None

    def __enter__(self):
        self.context_count += 1
        self.com = COM_WORD.Documents.Open(
            str(self.path.resolve()), Visible=self.visible_on_enter
        )
        self.com.Activate()
        self.com.ActiveWindow.Visible = self.visible_on_enter  # enforce visibility
        self.name = self.com.Name
        self.comments = Comments(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.context_count > 1:
            self.context_count -= 1
        else:
            if self.save_on_exit:
                self.com.Save()
            if self.close_on_exit:
                self.com.Close(SaveChanges=False)
            self.com = None
            self.name = None
            self.comments = None

    def delete_comments(self):
        """Delete all comments in the document."""

        warning_message = (
            "Cannot delete all comments."
            " There may have been no comments in the first place."
        )

        with self:
            try_com(
                com_method=self.com.DeleteAllComments,
                except_errors=errors["command_not_available"],
                messages=warning_message,
            )

    @property
    def visible_on_enter(self) -> bool:
        """Whether to make the document visible when entering context."""
        return not self.close_on_exit


class Comments(abc.Sequence):
    """The comments in an open Word document.

    Parameters
    ----------
    document
        The document from which to retrieve comments.

    Attributes
    ----------
    in_document
        The document in which the comments reside.
    com
        The COM object representation of the comments.

    """

    def __init__(self, document: Document):
        self.in_document = document
        self.com = self.in_document.com.Comments

    def __getitem__(self, index):
        if isinstance(index, slice):
            keys = range(*index.indices(len(self)))  # coerce keys to object bounds
            comment = [self[key] for key in keys]  # call __getitem__ w/ single elem
        else:
            key = index
            com_comment = self.com(key + 1)  # COM is 1-indexed
            comment = Comment(com_comment, self)
        return comment

    def __iter__(self):
        return (Comment(com_comment, self) for com_comment in self.com)

    def __len__(self):
        return len(self.com)


class Comment:
    """A comment in an open Word document.

    Parameters
    ----------
    com_comment
        The COM object representation of the comment.
    comments
        The list of comments in which this comment resides.

    Attributes
    ----------
    in_comments
        The list of comments in which this comment resides.
    in_document
        The document in which this comment resides.
    com
        The COM object representation of the comment.
    range
    text
    """

    def __init__(self, com_comment, comments):
        self.com = com_comment
        self.in_comments = comments
        self.in_document = self.in_comments.in_document

    @property
    def range(self):
        """
        range
            Convenience property returning this comment's range.
        """
        return Range(self.com.Range)

    @property
    def text(self):
        """
        text
            Convenience property returning this comment's text.
        """
        return self.range.text

    def delete(self):
        """Delete the comment and its children."""
        self.com.DeleteRecursively()

    def update(self, text: str):
        """Update the text of this comment.

        Parameters
        ----------
        text
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
        com_active_window.Selection.Text = text

        # Restore print view and cursor position
        com_active_window.ActivePane.Close()  # Close the comments pane that comes up
        com_active_window.ActivePane.View.Type = constants.wdPrintView
        original_cursor_position.Select()


class Range:
    """A text range in an open Word document.

    Parameters
    ----------
    com_range
        The COM object representation of the text range.

    Attributes
    ----------
    com
        The COM object representation of the text range.
    text
    """

    def __init__(self, com_range):
        self.com = com_range

    @property
    def text(self) -> str:
        """
        text
            Convenience property returning this range's text.
        """
        return self.com.Text


# * -------------------------------------------------------------------------------- * #
# * COM ERROR HANDLING * #


def try_com(
    com_method: Callable,
    except_errors: Optional[Union[ComError, List[ComError]]] = None,
    messages: Optional[Union[str, List[str]]] = None,
    **kwargs,
):
    """Try a COM method, warn about specified COM errors, and raise the rest.

    This function tries a COM method specified by `com_method`, catching generic COM
    errors and handling specific cases. COM errors are specified by their `com_error`
    rather than a Python exception type. In order to catch a specific error, supply the
    `com_error` of the error and the `message` to be displayed as a warning when the
    error is first caught. The `except_errors` and `messages` parameters also accept
    lists. If no message is provided, only the generic COM error will appear in the
    warning.

    Parameters
    ----------
    com_method
        The COM object representation of the comment.
    except_errors
        The `hresults` or list of `com_error` to catch
    messages
        The warning to be printed when the error is caught.
    **kwargs
        The keyword arguments to be passed to the COM method.

    Returns
    -------
    returns
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
