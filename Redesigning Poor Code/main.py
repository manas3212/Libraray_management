import argparse
import uuid
from functools import wraps  

from book import LibraryItemFactory, Book
from user import User
from storage import LibraryStorage
from check import CheckInCheckout


class Library:
    """Manages the library's collection of books and users."""

    def __init__(self, storage=LibraryStorage()):
        self.storage = storage
        self.books = []
        self.users = []
        self._load_data()

    
    def _save_data(self):
        """Saves books and users to storage."""
        data = {
            "books":[book.__dict__ for book in self.books],
            "users": [
                {k.strip("_"): v for k, v in user.__dict__.items() if k != "borrowed_books"}  # Use "borrowed_books" for clarity
                for user in self.users
            ],
        }
        self.storage.save_data(data)

    def _load_data(self):
        """Loads books and users from storage."""
        data = self.storage.load_data()
        self.books = [
            LibraryItemFactory.create_item(
                "book", 
                **book_data  # Pass the entire book_data dictionary, including available
            )
            for book_data in data["books"] 
            if book_data.get("author") is not None  # Only process books with an author
        ]
        self.users = [User(**user_data) for user_data in data["users"]]

   
    def _log_operation(func):
        """Decorator for logging library operations."""
        @wraps(func)  # Preserve function metadata
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result is not None:  # Only log if result is not None
                print(
                    f"Operation: {func.__name__}, Arguments: {args}, {kwargs}, Result: {result}"
                )
            else:
                print(
                    f"Operation: {func.__name__}, Arguments: {args}, {kwargs}, Result: Not found"
                )
            return result

        return wrapper

    @_log_operation
    def add_book(self, title, author, isbn):
        """Adds a new book to the library."""
        if not title.strip() or not author.strip():
            raise ValueError("Title and author cannot be empty.")
        if not Book.is_valid_isbn(isbn):
            raise ValueError("Invalid ISBN format.")
        # Check if a book with the same ISBN already exists
        if self.find_book(title=title, author=author, isbn=isbn):
            raise ValueError("Book with this title, author, and ISBN already exists.")
        if self.find_book(isbn=isbn):
            raise ValueError("Book with this ISBN already exists.")

        new_book = LibraryItemFactory.create_item("book", title=title, author=author, isbn=isbn)
        self.books.append(new_book)
        self._save_data()
        return new_book  # Return the added book object for logging
    
    def find_book(self, **kwargs):
        """Finds books based on specified criteria (title, author, ISBN)."""
        return next(
            (
                book
                for book in self.books
                if all(
                    getattr(book, f"_{key}") == value
                    for key, value in kwargs.items()
                )
            ),
            None,
        )

    def list_books(self):
        """Lists all books in the library."""
        if not self.books:
            print("List feature will be added")
            return
        for book in self.books:
            print(
                f"Title: {book.get_title()}, Author: {book.get_author()}, "
                f"ISBN: {book.get_isbn()}, Available: {book.is_available()}"
            )

    @_log_operation
    def update_book(self, isbn, **kwargs):
        """Updates book information based on ISBN."""
        book = self.find_book(isbn=isbn)
        if book:
            for key, value in kwargs.items():
                if hasattr(book, f"_{key}"):
                    setattr(book, f"_{key}", value)
            self._save_data()
            return book  # Return the updated book object for logging
        else:
            raise ValueError(f"Book with ISBN {isbn} not found.")

    @_log_operation
    def delete_book(self, isbn):
        """Deletes a book by ISBN."""
        book_to_delete = self.find_book(isbn=isbn)
        if book_to_delete:
            self.books.remove(book_to_delete)
            self._save_data()
            return book_to_delete  # Return the deleted book object for logging
        else:
            raise ValueError(f"Book with ISBN {isbn} not found.")

    @_log_operation
    def add_user(self, name):
        """Adds a new user to the library."""
        """Adds a new user to the library, checking for duplicates."""
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if self.find_user(name=name):  # Check for existing user with the same name
            raise ValueError("User with this name already exists.")
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        new_user = User(name, user_id)
        self.users.append(new_user)
        self._save_data()
        return new_user  # Return the added user object for logging

    def find_user(self, **kwargs):
        """Finds users based on specified criteria (name, user_id)."""
        return next(
            (
                user
                for user in self.users
                if all(
                    getattr(user, f"_{key}") == value
                    for key, value in kwargs.items()
                )
            ),
            None,
        )

    def list_users(self):
        """Lists all users in the library."""
        if not self.users:
            print("No users in the library.")
            return
        for user in self.users:
            print(f"Name: {user.get_name()}, User ID: {user.get_user_id()}")

    @_log_operation
    def update_user(self, user_id, new_name):
        """Updates a user's name based on user_id."""
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        user = self.find_user(user_id=user_id)
        if user:
            user._name = new_name
            self._save_data()
            return user  # Return the updated user object for logging
        else:
            raise ValueError(f"User with ID {user_id} not found.")

    @_log_operation
    def delete_user(self, user_id):
        """Deletes a user by user_id."""
        user_to_delete = self.find_user(user_id=user_id)
        if user_to_delete:
            if user_to_delete.get_borrowed_books():
                raise ValueError("Cannot delete user with borrowed books.")
            self.users.remove(user_to_delete)
            self._save_data()
            return user_to_delete  # Return the deleted user object for logging
        else:
            raise ValueError(f"User with ID {user_id} not found.")


# ... (The rest of the main function with the CLI code remains the same)
def main():
    parser = argparse.ArgumentParser(description="Library Management System")
    subparsers = parser.add_subparsers(dest="command")

    # Book Commands
    book_parser = subparsers.add_parser("book", help="Manage books")
    book_subparsers = book_parser.add_subparsers(dest="action")
    book_add = book_subparsers.add_parser("add", help="Add a new book")
    book_add.add_argument("title", help="Title of the book")
    book_add.add_argument("author", help="Author of the book")
    book_add.add_argument("isbn", help="ISBN of the book")
    book_list = book_subparsers.add_parser("list", help="List all books")
    book_update = book_subparsers.add_parser("update", help="Update a book")
    book_update.add_argument("isbn", help="ISBN of the book to update")
    book_update.add_argument("--title", help="New title of the book")
    book_update.add_argument("--author", help="New author of the book")
    book_delete = book_subparsers.add_parser("delete", help="Delete a book")
    book_delete.add_argument("isbn", help="ISBN of the book to delete")

    # User Commands
    user_parser = subparsers.add_parser("user", help="Manage users")
    user_subparsers = user_parser.add_subparsers(dest="action")
    user_add = user_subparsers.add_parser("add", help="Add a new user")
    user_add.add_argument("name", help="Name of the user")
    user_list = user_subparsers.add_parser("list", help="List all users")
    user_update = user_subparsers.add_parser("update", help="Update a user")
    user_update.add_argument("user_id", help="User ID to update")
    user_update.add_argument("new_name", help="New name of the user")
    user_delete = user_subparsers.add_parser("delete", help="Delete a user")
    user_delete.add_argument("user_id", help="User ID to delete")

    # Check In/Out Commands
    check_parser = subparsers.add_parser("check", help="Check in/out books")
    check_subparsers = check_parser.add_subparsers(dest="action")
    check_out = check_subparsers.add_parser("out", help="Check out a book")
    check_out.add_argument("user_id", help="User ID")
    check_out.add_argument("book_isbn", help="ISBN of the book")
    check_in = check_subparsers.add_parser("in", help="Check in a book")
    check_in.add_argument("book_isbn", help="ISBN of the book")

    args = parser.parse_args()

    library = Library()
    check = CheckInCheckout(library)

    # Command Handling Logic
    if args.command == "book":
        if args.action == "add":
            try:
                library.add_book(args.title, args.author, args.isbn)
            except ValueError as e:
                print(f"Error: {e}")
        elif args.action == "list":
            library.list_books()
        elif args.action == "update":
            try:
                library.update_book(args.isbn, title=args.title, author=args.author)
            except ValueError as e:
                print(f"Error: {e}")
        elif args.action == "delete":
            try:
                library.delete_book(args.isbn)
            except ValueError as e:
                print(f"Error: {e}")
    elif args.command == "user":
        if args.action == "add":
            try:
                library.add_user(args.name)
            except ValueError as e:
                print(f"Error: {e}")
        elif args.action == "list":
            library.list_users()
        elif args.action == "update":
            try:
                library.update_user(args.user_id, args.new_name)  
            except ValueError as e:
                print(f"Error: {e}")
        elif args.action == "delete":
            try:
                library.delete_user(args.user_id)
            except ValueError as e:
                print(f"Error: {e}")
    elif args.command == "check":
        if args.action == "out":
            try:
                check.check_out_book(args.user_id, args.book_isbn)
            except ValueError as e:
                print(f"Error: {e}")
        elif args.action == "in":
            try:
                check.check_in_book(args.book_isbn)
            except ValueError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()




# # Add a book
# python main.py book add "The Lord of the Rings" "J.R.R. Tolkien" "9780618640157"

# # List all books
# python main.py book list

# # Update a book's title
# python main.py book update 9780618640157 --title "The Fellowship of the Ring"

# # Delete a book
# python main.py book delete 9780618640157

# # Add a user
# python main.py user add "Alice"

# # List all users
# python main.py user list

# # Update a user's name
# python main.py user update <user_id> "New Name"  

# # Delete a user
# python main.py user delete <user_id>

# # Check out a book
# python main.py check out <user_id> <book_isbn>

# # Check in a book
# python main.py check in <book_isbn>
