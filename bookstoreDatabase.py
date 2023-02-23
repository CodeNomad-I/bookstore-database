'''This program is designed to keep track of the books that are in stock.
The details assigned to them are their unique id which is automatically assigned to them, their title, their author
and the quantity of them in stock.
Within this program you should be able to:
- Add a book to the database
- Update a book within the database
- Delete a book in the database
- Search for a book in the database, either using its id, title or author. If you search by author then all books by that 
author will be revealed to you.
- Finally, exit the program.'''
#=========== BOOKSTORE PROGRAM ===========
import sqlite3

#=========== Function Central ============

# Establishing a table, but ignoring this if one already exists
def create_table():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            quantity INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Adding a book
def add_book():
    # Connect to the database and create a cursor
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    
    # Input the books information, except id which is automatically assigned.
    print("Enter the information for the new book:")
    new_title = input("Title: ")
    new_author = input("Author: ")
    new_quantity = input("Quantity: ")
    
    # Attempts to convert the quantity to an integer, if failed then the operation is aborted.
    try:
        new_quantity = int(new_quantity)
        
        # If successful, confirm_update() runs which displays the new information and asks if you are sure you want to add it.
        if confirm_update(None, new_title, new_author, new_quantity):
            c.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)", (new_title, new_author, new_quantity))
            conn.commit()
            print("\nBook added successfully.")
        
        # Here are the two failsafes
        else:
            print("\nAdding book cancelled.")
    except ValueError:
        print("\nQuantity must be an integer, adding book failed.")
    conn.close()

# Updating book information
def update_book():
    # Connect to the database and create a cursor
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    
    # Since the id is the only thing the user won't change, this is what is being used to select the book.
    book_id = input("Enter the ID of the book to update: ")
    
    # Another failsafe just in case the id isn't an integer
    try:
        book_id = int(book_id)
        
        # Retrieves the book with that id
        c.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = c.fetchone()
        
        # This checks if there was a book with that id
        if book:
            
            # The current information is displayed
            print("Current information:")
            display_book(book)
            
            # The user is prompted to input the updated information, with the ability to skip over sections if no change needed
            print("\nEnter the new information:")
            new_title = input("Title (or leave blank to keep the current title): ")
            new_author = input("Author (or leave blank to keep the current author): ")
            new_quantity = input("Quantity (or leave blank to keep the current quantity): ")
            
            # This checks if you did indeed skip over certain sections
            if new_title == "":
                new_title = book[1]
            if new_author == "":
                new_author = book[2]
            
            # Another integer check
            try:
                if new_quantity != "":
                    new_quantity = int(new_quantity)
                else:
                    new_quantity = book[3]
                
                # A function is called to display the new information and confirm whether you want the changes to be made.
                if confirm_update(book_id, new_title, new_author, new_quantity):
                    c.execute("UPDATE books SET title=?, author=?, quantity=? WHERE id=?", (new_title, new_author, new_quantity, book_id))
                    conn.commit()
                    print("\nBook updated successfully.")
                
                # The failsafes
                else:
                    print("\nUpdating book cancelled.")
            except ValueError:
                print("\nQuantity must be an integer, Updating book failed.")
        else:
            print("\nBook not found.")
    except ValueError:
        print("\nID must be an integer.")
    conn.close()

# Deleting book information
def delete_book():
    # Ask user for an id.
    book_id = input("Enter the ID of the book to delete: ")

    # More defensive programming to ensure the id is an integer
    try:
        book_id = int(book_id)
    except ValueError:
        print("\nID must be an integer.")
        return

    conn = sqlite3.connect("ebookstore.db")
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = c.fetchone()

    # If there is no book, throw this
    if book is None:
        print("Book not found.")
        return

    # If there is a book, display book info and confirm with the user if they would like to delete it
    if confirm_deletion(book):
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        
        # This resets the index of all values after a deleted value, meaning that there are no gaps in the id
        c.execute("UPDATE books SET id = id - 1 WHERE id > ?", (book_id,))
        conn.commit()
        print("Book successfully deleted.")
        
    # The failsafe
    else:
        print("Deletion cancelled.")

# Searching for a book
def search_book():
    # Ask the user to specify what identifier they would like to search for
    search_by = input("Search by (id/title/author): ").lower()

    # This checks they actually selected a valid search criteria
    if search_by not in ["id", "title", "author"]:
        print("Invalid search criteria.")
        return

    # Specify what you would like to search for
    search_term = input("Enter search term: ").lower()

    conn = sqlite3.connect("ebookstore.db")
    c = conn.cursor()

    # This checks if the entered id is an integer and then also retrieves the info at that id
    if search_by == "id":
        try:
            book_id = int(search_term)
        except ValueError:
            print("ID must be a positive integer.")
            return

        c.execute("SELECT * FROM books WHERE id=?", (book_id,))

    # Retrieves books with the title specified
    elif search_by == "title":
        c.execute("SELECT * FROM books WHERE LOWER(title)=?", (search_term,))

    # Retrieves all books written by the specified author
    elif search_by == "author":
        c.execute("SELECT * FROM books WHERE LOWER(author)=?", (search_term,))

    books = c.fetchall()

    # Executes if no books were retrieved
    if len(books) == 0:
        print("Book not found.")
        return

    # I added this loop so then if someone were to search by author, then they would recieve all books written by said author
    print('-' * 20)
    print("Results:")
    print('-' * 20)
    for book in books:
        display_book(book)

# This function prints the new information and asks for confirmation if it correct before adding to the database
def confirm_update(book_id, new_title, new_author, new_quantity):
    print("\nNew book information:")
    print("ID:", book_id)
    print("Title:", new_title)
    print("Author:", new_author)
    print("Quantity:", new_quantity)
    confirmation = input("\nIs this information correct? (yes/no): ")
    return confirmation.lower() == "yes"

# This function also prints the information of a book and asks if you are sure you want to delete from the database
def confirm_deletion(book):
    print("You are about to delete the following book:")
    display_book(book)
    confirmation = input("Are you sure you want to delete this book? (yes/no): ")
    return confirmation.lower() == "yes"

# Displays book information
def display_book(book):
    print("ID:", book[0])
    print("Title:", book[1])
    print("Author:", book[2])
    print("Quantity:", book[3])
    print("-" * 20)

#   Displays exit message with a bit of ASCII art to make it look nice
def display_exit_message():
    print("""

\n\n\n  _________________________________________
 /                                         \\
|   Thank you for using the eBookstore!    |
|  ======================================  |
|            Have a great day!             |
 \\_________________________________________/


""")

# Displays menu, also with ASCII art since it will be seen often and therefore might as well look nice too
def display_menu():
    print("""
 ___________________________________________
/                                           \\
|   Welcome to the eBookstore Database!     |
|                                           |
|  ======================================   |
|  [1] Enter book                           |
|  [2] Update book                          |
|  [3] Delete book                          |
|  [4] Search books                         |
|  [0] Exit                                 |
|  ======================================   |
|                                           |
\___________________________________________/
""")

# Menu function
def menu():
       
    while True:
        display_menu()
        choice = input("Please choose an option (0-4): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "0":
            display_exit_message()
            break
        else:
            print("Invalid choice.")
    

# ===== Main program =====
create_table()
menu()