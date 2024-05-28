import re

class LibraryItem:
    """Base class for library items."""

    def __init__(self, title, available=True):
        self._title = title
        self._available = available

    def get_title(self):
        return self._title

    def is_available(self):
        return self._available

    def set_available(self, status):
        self._available = status

class Book(LibraryItem):
    """Represents a book in the library system."""

    def __init__(self, title, author, isbn, available=True):
        super().__init__(title, available)
        if not author.strip():
            raise ValueError("Author cannot be empty.")
        if not Book.is_valid_isbn(isbn):
            raise ValueError("Invalid ISBN format.")
        self._author = author
        self._isbn = isbn

    def get_author(self):
        return self._author

    def get_isbn(self):
        return self._isbn

    @staticmethod
    def is_valid_isbn(isbn):
        """Validates ISBN format (simplified to only check for 10 digits)."""
        return isbn.isdigit() and len(isbn) == 10 


class LibraryItemFactory:
    """Factory class to create library items."""

    @staticmethod
    def create_item(item_type, **kwargs):
        if item_type == "book":
            return Book(**kwargs)
        # ... (Add more cases for other item types in the future)
        else:
            raise ValueError("Invalid item type")


