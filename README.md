# Libraray_management
Once you run the script, you'll be presented with the interactive CLI. Here's how to use it:

**python <full path of main.py> <command> <subcommand> [arguments]**



Commands:
book: Manages books in the library.
user: Manages users in the library.
check: Handles book check-in and check-out operations.




Subcommands:

add: Adds a new book or user.
list: Lists all books or users.
update: Updates a book or user.
delete: Deletes a book or user.


Example:
# Add a book
python <full path of main.py> book add "The Lord of the Rings" "J.R.R. Tolkien" "1234567890"

# Add a user
python <full path of main.py> user add "Alice"

# List all users
python <full path of main.py> user list
