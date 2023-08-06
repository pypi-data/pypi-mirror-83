"""Microsoft Word review tools (comments, markup, etc.) with Python."""

from typing import Optional

from docxrev import com


def quit_word():
    """Quit Word."""
    com.COM_WORD.Quit()


def quit_word_safely():
    """Quit Word if no documents are open."""
    if not com.COM_WORD.Documents:
        quit_word()


def get_active_document(
    save_on_exit: Optional[bool] = True, close_on_exit: Optional[bool] = False
) -> com.Document:
    """Get the currently active document.

    Parameters
    ----------
    save_on_exit: test
        Whether to save the document when exiting a ``with`` context. **Default:**
        ``True``.
    close_on_exit
        Whether to close the document when exiting a ``with`` context. **Default:**
        Don't close the document on exit.
    """

    return com.Document(
        com.COM_WORD.ActiveDocument.FullName, save_on_exit, close_on_exit
    )
