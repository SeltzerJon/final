import sqlite3
from datetime import datetime, timedelta


# 1.	Project should have a functioning menu. Done
# 2.	Project should have adequate functions (minimum 3 functions.) Done
# 3.	Project should make use of files to save the data. Done
# 4.	Project should handle adequate exceptions. Done
# 5.	Project should display information formatted adequately.  Done
# 6.	Project should make use of lists or dictionaries as appropriate.  Done
# 7.	Project should follow adequate naming conventions for variables and functions and should have comments as appropriate.  Done

# 8.	Project should use an object-oriented approach, (inheritance is optional) Need to do
# 9.	Project should use a database Done

# o	The user should be able to rent one or more books in any combination of authors, titles, categories, etc. The quantity and availability of the book must be updated according to each renting transaction.
# o	The application should generate and display a receipt stating the list of books selected and their return due dates (30 days from the rent day).

# Creates database table with the following titles
def create_table():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Books (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL UNIQUE,
                        category  TEXT NOT NULL,
                        quantity INTEGER
                    )''')
    conn.commit()
    conn.close()


# Inserts book info in the specify sections in the table
def insert_data():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('DUCKS: TWO YEARS IN THE OIL SANDS', 'Kate Beaton', 'Graphic', 4)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('HANG THE MOON', 'Jeannette Walls', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('IT ENDS WITH US', 'Colleen Hoover', 'fiction', 3)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('THE BEGGAR GARDEN', 'Michael Christie', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('IF HE HAD BEEN WITH ME', 'Laura Nowlin', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('TWISTED LOVE', 'Ana Huang', 'romance', 3)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('MEXICAN GOTHIC', 'Silvia Moreno-Garcia', 'romance', 3)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('THINGS WE HIDE FROM THE LIGHT', 'Lucy Score', 'romance', 3)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('VERITY', 'Colleen Hoover', 'fiction', 3)")

    conn.commit()
    conn.close()


# Search function
# Search through title,author or category to see if input contains the letter or word
def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(
        "SELECT * FROM Books WHERE title LIKE ? OR author LIKE ? OR category LIKE ?",
        ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    books = c.fetchall()
    conn.close()
    return books


# Function for printing a book
# Prints the book index position 0,1,2,3,4
def print_books(books):
    if books:
        for book in books:
            print(
                f"Book id:{book[0]}\n" + f"Title: {book[1]}\n" + f"Author:{book[2]}\n" + f"Genre:{book[3]}\n" + f"Copies:{book[4]}\n")
    else:
        print('No results found.')


# Function that prints all the books in the database
def print_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Books")
    books = c.fetchall()
    conn.close()
    print('\nBook Database:')
    for book in books:
        print(
            f"Book id:{book[0]}\n" + f"Title: {book[1]}\n" + f"Author:{book[2]}\n" + f"Genre:{book[3]}\n" + f"Copies:{book[4]}\n")


# Function for saving a book if the user wants
# Checks to if input id is equal to a book id and saves the book as a file
def save_book():
    while True:
        book_id = input("Enter the id of the book you want to save (must be a number): ")
        if book_id.isdigit():
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('SELECT * FROM Books WHERE id=?', (book_id,))
            book = c.fetchone()
            conn.close()
            # if book is found save the contents of the book in file
            if book:
                with open(f"book_{book_id}.txt", "w") as f:
                    f.write(f"Title: {book[1]}\nAuthor: {book[2]}\nCategory: {book[3]}\nQuantity: {book[4]}")
                print(f"Book {book[1]} saved to file book_{book_id}.txt")
            #     if book is not found
            else:
                print(f"No book found with id {book_id}")
            break
        else:
            print("Invalid input. Please enter a number.")


# Function for renting a book or books
def rent_books():
    print('\nRent Books:')
    # Array to store books
    rented_books = []
    while True:
        book_id = input("Enter the id of the book you want to rent (must be a number, 'q' to quit): ")
        if book_id.lower() == 'q':
            break
        #     input is not a number
        elif not book_id.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Books WHERE id=?", (book_id,))
        book = c.fetchone()
        # Not found prints not found
        if not book:
            print(f"No book found with id {book_id}")
            conn.close()
            continue
        #  Converts book index position 4 to an integer and stores it in a tuple
        if not isinstance(book[4], int):
            book = list(book)
            book[4] = int(book[4])
            book = tuple(book)
        #     When book is not available
        if book[4] == 0:
            print(f"Book {book_id} is not available for rent.")
            conn.close()
            continue
        #     Asks how many copies
        rent_qty = input(f"How many copies of '{book[1]}' would you like to rent? ")
        if not rent_qty.isdigit():
            print("Invalid input. Please enter a number.")
            conn.close()
            continue
        rent_qty = int(rent_qty)
        if rent_qty <= 0:
            print("Invalid input. Please enter a positive number.")
            conn.close()
            continue
        #     If numbers of copies is greater than the copies trying to rent
        if rent_qty > book[4]:
            print(f"Only {book[4]} copies of '{book[1]}' are available for rent.")
            conn.close()
            continue
        #  If there's enough copies of a book, calculates the due date of 30 days
        due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        # The list of tuples that stores the books details the user is renting
        rented_books.append((book[1], rent_qty, due_date))
        # Updates the database of how many copies are left
        c.execute("UPDATE Books SET quantity=? WHERE id=?", (book[4] - rent_qty, book_id))
    # Displays receipt for user
    if rented_books:
        print("\nRented Books:")
        for rented_book in rented_books:
            book_title, rent_qty, due_date = rented_book
            # Prints the book details
            print(f"{book_title} - {rent_qty} copies, return date: {due_date}")
        conn.commit()
        conn.close()


# Menu
def menu():
    while True:
        print('\nLibrary Menu:')
        print('1. View Database')
        print('2. Search book')
        print('3. Rent books')
        print('4. Save Book')
        print('5. Quit')
        choice = input('Enter your choice: ')
        # Option 1
        if choice == '1':
            # Calls the print_database function
            print_database()
        # Option 2
        elif choice == '2':
            query = input("Enter a search query: ")
            # Calls the search_books function with the input query
            books = search_books(query)
            # Calls the print_books function
            print_books(books)
        # Option 3
        elif choice == '3':
            # Calls the rent_books function
            rent_books()
        # Option 4
        elif choice == '4':
            # Calls the save_book function
            save_book()
        # Option 5
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')


create_table()
insert_data()
menu()
