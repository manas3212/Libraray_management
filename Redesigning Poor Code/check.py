class CheckInCheckout:
    """Handles book check-in and check-out operations."""

    def __init__(self, library):
        self.library = library

    def check_out_book(self, user_id, book_isbn):
        """Checks out a book for a user."""
        user = self.library.find_user(user_id=user_id)
        if not user:
            raise ValueError("User not found.")

        book = self.library.find_book(isbn=book_isbn)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available():
            raise ValueError("Book is not available for checkout.")

        if any(book.get_isbn() == book_isbn for book in user.get_borrowed_books()):
            raise ValueError("You have already borrowed this book.")
        
        user.borrow_book(book)
        self.library._save_data()
        print(f"Book '{book.get_title()}' checked out by {user.get_name()}.")

    def check_in_book(self, book_isbn):
        """Checks in a book."""
        for user in self.library.users:
            if book_isbn in [b.get_isbn() for b in user.get_borrowed_books()]:
                book = self.library.find_book(isbn=book_isbn)
                user.return_book(book)
                self.library._save_data()
                print(f"Book '{book.get_title()}' checked in.")
                return
        raise ValueError("Book not found or not checked out by any user.")  
