import sqlite3
from datetime import datetime, timedelta


# 1.	Project should have a functioning menu. Done
# 2.	Project should have adequate functions (minimum 3 functions.) Done
# 3.	Project should make use of files to save the data. Done
# 4.	Project should handle adequate exceptions. Done
# 5.	Project should display information formatted adequately.  Done
# 6.	Project should make use of lists or dictionaries as appropriate.  Done
# 7.	Project should follow adequate naming conventions for variables and functions and should have comments as appropriate.  Done

# 8.	Project should use an object-oriented approach, (inheritance is optional)
# 9.	Project should use a database Done

# o	The user should be able to rent one or more books in any combination of authors, titles, categories, etc. The quantity and availability of the book must be updated according to each renting transaction.
# o	The application should generate and display a receipt stating the list of books selected and their return due dates (30 days from the rent day).


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


def insert_data():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('DUCKS: TWO YEARS IN THE OIL SANDS', 'Kate Beaton', 'Graphic', 4)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('HANG THE MOON', 'Jeannette Walls', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('GREENWOOD', 'Michael Christie', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('THE BEGGAR GARDEN', 'Michael Christie', 'fiction', 5)")
    c.execute(
        "INSERT OR REPLACE INTO Books (title, author, category, quantity) VALUES ('IF HE HAD BEEN WITH ME', 'Laura Nowlin', 'fiction', 3)")

    conn.commit()
    conn.close()


def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(
        "SELECT * FROM Books WHERE title LIKE ? OR author LIKE ? OR category LIKE ?",
        ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    books = c.fetchall()
    conn.close()
    return books


def print_books(books):
    if books:
        for book in books:
            print(
                f"Book id:{book[0]}\n" + f"Title: {book[1]}\n" + f"Author:{book[2]}\n" + f"Genre:{book[3]}\n" + f"Copies:{book[4]}\n")
    else:
        print('No results found.')


def print_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Books")
    books = c.fetchall()
    conn.close()
    print('\nBook Database:')
    for book in books:
        print(f"Book id:{book[0]}\n" + f"Title: {book[1]}\n" +f"Author:{book[2]}\n" + f"Genre:{book[3]}\n" + f"Copies:{book[4]}\n")


def save_book():
    while True:
        book_id = input("Enter the id of the book you want to save (must be a number): ")
        if book_id.isdigit():
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("SELECT * FROM Books WHERE id=?", (book_id,))
            book = c.fetchone()
            conn.close()
            if book:
                with open(f"book_{book_id}.txt", "w") as f:
                    f.write(f"Title: {book[1]}\nAuthor: {book[2]}\nCategory: {book[3]}\nQuantity: {book[4]}")
                print(f"Book {book[1]} saved to file book_{book_id}.txt")
            else:
                print(f"No book found with id {book_id}")
            break
        else:
            print("Invalid input. Please enter a number.")


def rent_books():
    print('\nRent Books:')
    rented_books = []
    while True:
        book_id = input("Enter the id of the book you want to rent (must be a number, 'q' to quit): ")
        if book_id == 'q':
            break
        elif not book_id.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Books WHERE id=?", (book_id,))
        book = c.fetchone()
        if not book:
            print(f"No book found with id {book_id}")
            conn.close()
            continue
        if not isinstance(book[4], int):
            book = list(book)
            book[4] = int(book[4])
            book = tuple(book)
        if book[4] == 0:
            print(f"Book {book_id} is not available for rent.")
            conn.close()
            continue
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
        if rent_qty > book[4]:
            print(f"Only {book[4]} copies of '{book[1]}' are available for rent.")
            conn.close()
            continue
        due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        rented_books.append((book[1], rent_qty, due_date))
        c.execute("UPDATE Books SET quantity=? WHERE id=?", (book[4] - rent_qty, book_id))
        # display receipt
    if rented_books:
        print("\nRented Books:")
        for rented_book in rented_books:
            book_title, rent_qty, due_date = rented_book
            print(f"{book_title} - {rent_qty} copies, return date: {due_date}")
        conn.commit()
        conn.close()


def menu():
    while True:
        print('\nLibrary Menu:')
        print('1. View Database')
        print('2. Search book')
        print('3. Rent books')
        print('4. Save Book')
        print('5. Quit')
        choice = input('Enter your choice: ')

        if choice == '1':
            print_database()
        elif choice == '2':
            query = input("Enter a search query: ")
            books = search_books(query)
            print_books(books)
        elif choice == '3':
            rent_books()
        elif choice == '4':
            save_book()
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    create_table()
    insert_data()
    menu()
