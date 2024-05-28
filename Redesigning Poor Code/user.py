class User:
    """Represents a user in the library system."""

    def __init__(self, name, user_id):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self._name = name
        self._user_id = user_id
        #self._borrowed_books = []

    def get_name(self):
        return self._name

    def get_user_id(self):
        return self._user_id

    # def get_borrowed_books(self):
    #     return self._borrowed_books

    # def borrow_book(self, book):
    #     if book in self._borrowed_books:
    #         raise ValueError("You have already borrowed this book.")
    #     self._borrowed_books.append(book)
    #     book.set_available(False)

    # def return_book(self, book):
    #     if book in self._borrowed_books:
    #         self._borrowed_books.remove(book)
    #         book.set_available(True)
    #     else:
    #         raise ValueError("You haven't borrowed this book.")
