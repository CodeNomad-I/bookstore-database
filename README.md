# Bookstore Database
## Project description
I wanted to create a program that allowed you to create and manipulate a database, made using sqlite, that stored the information of books in the store.
I wanted the program to allow the user to:
* Add a book, along with all it's information.
* Edit a books information, in case there was an error or change.
* Delete a book, if you wanted it completely off the database.
* Search for a book, using either its ID, title or author.
* And finally, the option to leave the program.

The information that is stored by the database is:
* ID (which is automatically assigned when entered into the database)
* Title
* Author
* Quantity

Since I had the image of a customer using this program, I made sure to include as many safety measures as possible, which included adding an obscene amount of
'try-except' blocks.
