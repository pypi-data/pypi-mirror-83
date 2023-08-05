"""Microsoft Word review tools (comments, markup, etc.) with Python."""

from typing import Optional

from . import com
from .com import Document


def quit_word():
    """Quit Word."""
    com.COM_WORD.Quit()


def quit_word_safely():
    """Quit Word if no documents are open."""
    if not com.COM_WORD.Documents:
        quit_word()


def get_active_document(
    save_on_exit: bool = True, close_on_exit: Optional[bool] = None
) -> Document:
    """Get the current document."""
    return Document(com.COM_WORD.ActiveDocument.FullName, save_on_exit, close_on_exit)
