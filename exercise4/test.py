import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT)''')

def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully.")

def find_book():
    book_id = input("Enter BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if not book:
        print("Book not found.")
        return

    print("Book Details:")
    print("BookID:", book[0])
    print("Title:", book[1])
    print("Author:", book[2])
    print("ISBN:", book[3])
    print("Status:", book[4])

    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    reservation = c.fetchone()

    if reservation:
        user_id = reservation[2]
        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()
        print("Reserved by:")
        print("UserID:", user[0])
        print("Name:", user[1])
        print("Email:", user[2])

def find_reservation_status():
    text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if text.startswith('LB'):
        c.execute("SELECT * FROM Books WHERE BookID=?", (text,))
        book = c.fetchone()

        if not book:
            print("Book not found.")
            return

        print("Reservation status for BookID", book[0])
        print("Status:", book[4])

    elif text.startswith('LU'):
        user_id = text
        c.execute("SELECT * FROM Reservations WHERE UserID=?", (user_id,))
        reservations = c.fetchall()

        if not reservations:
            print("No reservations found for UserID", user_id)
            return

        print("Reservations for UserID", user_id)
        for reservation in reservations:
            book_id = reservation[1]
            c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
            book = c.fetchone()
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])

    elif text.startswith('LR'):
        reservation_id = text
        c.execute("SELECT * FROM Reservations WHERE ReservationID=?", (reservation_id,))
        reservation = c.fetchone()

        if not reservation:
            print("Reservation not found for ReservationID", reservation_id)
            return

        book_id = reservation[1]
        user_id = reservation[2]

        c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
        book = c.fetchone()

        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()

        print("Reservation details for ReservationID", reservation_id)
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        print("UserID:", user[0])
        print("Name:", user[1])
        print("Email:", user[2])

    else:
        title = text
        c.execute("SELECT * FROM Books WHERE Title=?", (title,))
        books = c.fetchall()

        if not books:
            print("No books found with Title", title)
            return

        print("Books with Title", title)
        for book in books:
            book_id = book[0]
            c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
            reservation = c.fetchone()
            if reservation:
                user_id = reservation[2]
            else:
                user_id = None

            c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
            user = c.fetchone()

            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            if user:
                print("Reserved by:")
                print("UserID:", user[0])
                print("Name:", user[1])
                print("Email:", user[2])

def all_books():
    c.execute("SELECT * FROM Books")
    books = c.fetchall()

    if not books:
        print("No books found.")
        return

    print("All Books:")
    for book in books:
        book_id = book[0]
        c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
        reservation = c.fetchone()
        if reservation:
            user_id = reservation[2]
        else:
            user_id = None

        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()

        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        if user:
            print("Reserved by:")
            print("UserID:", user[0])
            print("Name:", user[1])
            print("Email:", user[2])

def update_book():
    book_id = input("Enter BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if not book:
        print("Book not found.")
        return

    status = input("Enter new status: ")

    c.execute("UPDATE Books SET Status=? WHERE BookID=?", (status, book_id))
    conn.commit()

    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    reservation = c.fetchone()

    if reservation:
        user_id = reservation[2]
        c.execute("UPDATE Reservations SET BookID=?, UserID=?, ReservationDate=? WHERE BookID=?",
                  (book_id, user_id, reservation[3], book_id))
        conn.commit()

        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()

        print("Reservation Details Updated:")
        print("BookID:", book_id)
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", status)
        print("Reserved by:")
        print("UserID:", user[0])
        print("Name:", user[1])
        print("Email:", user[2])
    else:
        print("Book Details Updated:")
        print("BookID:", book_id)
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", status)

def delete_book():
    book_id = input("Enter BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if not book:
        print("Book not found.")
        return

    c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
    conn.commit()

    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    reservation = c.fetchone()

    if reservation:
        user_id = reservation[2]
        c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
        conn.commit()

        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()

        print("Book and Reservation Deleted:")
        print("BookID:", book_id)
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        print("Reserved by:")
        print("UserID:", user[0])
        print("Name:", user[1])
        print("Email:", user[2])
    else:
        print("Book Deleted:")
        print("BookID:", book_id)
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all the books")
    print("5. Modify/update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        add_book()
    elif choice == '2':
        find_book()
    elif choice == '3':
        find_reservation_status()
    elif choice == '4':
        all_books()
    elif choice == '5':
        update_book()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()