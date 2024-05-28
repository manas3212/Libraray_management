import json

class LibraryStorage:
    """Handles storage and retrieval of library data using JSON."""

    def __init__(self, filename="library.json"):
        self.filename = filename

    def load_data(self):
        """Loads library data from the JSON file."""
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"books": [], "users": []}
        return data

    def save_data(self, data):
        """Saves library data to the JSON file."""
        # Load existing data 
        existing_data = self.load_data()
        new_books = []
        if existing_data["books"]: # Check if there are any existing books
            new_books = [
                book
                for book in data["books"]
                
                if not any(
                    existing_book["_title"] == book["_title"]
                    and existing_book["_author"] == book["_author"]
                    and existing_book["_isbn"] == book["_isbn"]
                    for existing_book in existing_data["books"]
                )

                    ]
        else:
            new_books = data["books"]

        new_users = [
            user for user in data["users"] if user not in existing_data["users"]]

        # Append new data to existing data
        existing_data["books"].extend(new_books)
        existing_data["users"].extend(new_users)

        # Write the updated data back to the file
        with open(self.filename, "w") as file:
            json.dump(existing_data, file, indent=4)

