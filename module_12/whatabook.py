"""
    Developer: Sebastian Baillie
    Class: CYBR410-318A
    Date: July 23, 2022
"""

from functools import partial
import tkinter as tk
import os
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}
#### COMMAND LINE SECTION ###
# Menu Function
def show_menu():
    os.system("clear")
    print("Welcome to WhatABooks!\n")
    print("1.\tView Books")
    print("2.\tView Store Locations")
    print("3.\tMy Account")
    print("4.\tExit")
    choice = input("\nWhat would you like to do today? ")
    if choice == "1":
        return show_books(cursor)
    elif choice == "2":
        return show_locations(cursor)
    elif choice == "3":
        return validate_user(cursor)
    elif choice == "4":
        print("Thanks for choosing WhatABooks! Goodbye!")
        db.close()
    else:
        return show_menu()

# Show Books function
# When user selection option 1 from main menu
def show_books(cursor):
    os.system("clear")

    cursor.execute("SELECT book_id, book_name, details, author FROM book")
    books = cursor.fetchall()

    print("DISPLAYING AVAILABLE BOOKS\n")
    for book in books:
        print("Book ID: {}".format(book[0]))
        print("Book Name: {}".format(book[1]))
        print("Book Details: {}".format(book[2]))
        print("Book Author: {}\n".format(book[3]))

    input("Press ENTER to return to main menu. ")
    return show_menu()

# Show Locations function
# When user selects option 2 from main menu
def show_locations(cursor):
    os.system("clear")

    cursor.execute("SELECT store_id, locale FROM store")
    locations = cursor.fetchall()

    print("DISPLAYING LOCATIONS\n")
    for location in locations:
        print("Location ID: {}".format(location[0]))
        print("Location Address: {}\n".format(location[1]))

    input("Press ENTER to return to main menu.")
    return show_menu()

#Validate User function
#Validates the user by looping through the IDs in the User table
def validate_user(cursor):
    #os.system("clear")
    userId = input("Please input a user id: ")
    cursor.execute("SELECT user_id FROM user")
    users = cursor.fetchall()
    for user in users:
        if str(userId) == str(user[0]):
            return show_account_menu(cursor, userId)
    input("Invalid User ID. Press ENTER to try again.")
    return validate_user(cursor)
            

# Show Account Menu funciton
# When a user selects option 3 from main menu after validation
def show_account_menu(cursor, userId):
    os.system("clear")
    print("Account Menu\n")
    print("1.\tWishlist")
    print("2.\tAdd Books")
    print("3.\tMain Menu")
    accountOption = input("\nWhat would you like to do? ")
    if accountOption == "1":
        return show_wishlist(cursor, userId)
    elif accountOption == "2":
        return show_books_to_add(cursor, userId)
    elif accountOption == "3":
        return show_menu()
    else:  
        input("Invalid Option. Press ENTER to return to account menu.")
        return show_account_menu(cursor, userId)

# Show Wishlist function
# When user selects option 1 from account menu
def show_wishlist(cursor, user_id):
    os.system("clear")

    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(user_id))
    wishlist = cursor.fetchall()

    print("WISHLIST\n")
    for book in wishlist:
        print("Book Name: {}".format(book[4]))
        print("Author: {}\n".format(book[5]))
    

    input("Press ENTER to return to account menu.")
    return show_account_menu(cursor, user_id)

# Show Available Books to Add to Wishlist
# When user selects option 2 from account menu
def show_books_to_add(cursor, user_id):
    os.system("clear")

    cursor.execute("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(user_id))
    books_to_add = cursor.fetchall()
    
    print("AVAILABLE BOOKS TO ADD TO WISHLIST\n")
    for book in books_to_add:
        print("Book Id: {}".format(book[0]))
        print("Book Name: {}\n".format(book[1]))

    book_id = input("What book would you like to add to your wishlist? ")
    add_book_to_wishlist(cursor, books_to_add, user_id, book_id)
    return show_wishlist(cursor, user_id)

# Add Book to Wishlist function
# When user selects option 3 from main menu
# If user enters invalid book, it takes them back to their wishlist
def add_book_to_wishlist(cursor, books, user_id, book_id):
    bookFound = False
    for book in books:
        if str(book_id) == str(book[0]):
            bookFound = True
            cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(user_id, book_id))
            return
    if bookFound == False:
        input("Book not found. Press ENTER to return to wishlist.")

### GRAPHICAL USER INTERFACE ###
# Switches view to the Books section
def showBooks():
    locationFrame.grid_forget()
    accountFrame.grid_forget()
    bookFrame.grid(row = 1)

# Switches view to the Locations section
def showLocations():
    bookFrame.grid_forget()
    accountFrame.grid_forget()
    locationFrame.grid(row = 1)

# Switches view to the Accounts section
def showAccounts():
    bookFrame.grid_forget()
    locationFrame.grid_forget()
    accountFrame.grid(row = 1)

# Exits the program and closes database
def stopProgram():
    db.close()
    root.destroy()
    
# On account menu, when the user presses go, this will verify the user entered in valid ID
def getAccount():
    userId = accountEntry.get()
    cursor.execute("SELECT user_id, first_name, last_name FROM user")
    users = cursor.fetchall()
    for user in users:
        if str(userId) == str(user[0]):
            return showAccountGUI(user)

# This destroys the Account frame allowing them to view another account (Logout)
def logout(frame):
    frame.destroy()
    accountInstructLabel.grid(row = 0, column = 0, pady = 2)
    accountEntry.grid(row = 0, column = 1, pady = 2)
    accountGet.grid(row = 0, column = 2, pady = 2)

# When user enters valid ID, their account options show up.
def showAccountGUI(user):
    accountInfo = tk.Frame(accountFrame)
    accountInfo.grid(row = 1, column = 0, pady = 2)

    accountInstructLabel.grid_forget()
    accountEntry.grid_forget()
    accountGet.grid_forget()

    accountWelcomeLabel = tk.Label(accountInfo, text = "Welcome, " + str(user[1]) + "!")
    accountWelcomeLabel.grid(row = 1, column = 0, pady = 2)
    accountLogout = tk.Button(accountInfo, text = "Logout", command = partial(logout, accountInfo))
    accountLogout.grid(row = 1, column = 1)

    accountWishlistLabel = tk.Label(accountInfo, text = "Add to WishList: ")
    accountWishListEntry = tk.Entry(accountInfo)
    accountAddBook = tk.Button(accountInfo, text ="Go", command = partial(addWishlistGUI, user, accountWishListEntry, accountInfo))
    accountCurrentWishlistName = tk.Label(accountInfo, text = "Current Wishlist:\nBook Name")
    accountCurrentWishlistAuthor = tk.Label(accountInfo, text = "\nAuthor")

    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(user[0]))
    wishlist = cursor.fetchall()

    for book in wishlist:
        accountCurrentWishlistName["text"] = accountCurrentWishlistName["text"] + "\n" + str(book[4])
        accountCurrentWishlistAuthor["text"] = accountCurrentWishlistAuthor["text"] + "\n" + str(book[5])

    accountWishlistLabel.grid(row = 2, column = 0, pady = 2)
    accountWishListEntry.grid(row = 2, column = 1, pady = 2)
    accountAddBook.grid(row = 2, column = 2, pady = 2)
    accountCurrentWishlistName.grid(row = 3, column = 0, pady = 2)
    accountCurrentWishlistAuthor.grid(row = 3, column = 1, pady = 2)

# Verifies the book is valid and adds it to wishlist
def addWishlistGUI(user, bookEntry, frame):
    book_id = bookEntry.get()
    for book in books:
        if str(book_id) == str(book[0]):
            cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(user[0], book_id))
            frame.destroy()
            showAccountGUI(user)

#### MAIN PROGRAM ####
try:
    """ try/catch block for handling potential MySQL database errors """ 
    db = mysql.connector.connect(**config) # connect to the pysports database 
    # get the cursor object
    cursor = db.cursor()
except mysql.connector.Error as err:
    """ handle errors """ 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)
finally:
    os.system("clear")
    # First shows a welcome screen, asking user if wanting to run in CLI or GUI mode
    print("Welcome!")
    print("\n\t1.\tCommand Line Interface (CLI)")
    print("\n\t2.\tGraphcial User Interface (GUI)\n")
    option = input("How would you like to run the program? ")
    if option == "1":
        # Starts CLI mode by running Show Menu
        show_menu()
    elif option == "2":
        # Creation of GUI menu (using tkinter)
        root = tk.Tk()
        root.geometry('800x400')

        # MENU BUTTON CREATION

        menuBar = tk.Frame(root)
        menuBar.grid(row = 0)

        viewBooks = tk.Button(menuBar, text ="View Books", command = partial(showBooks))
        viewLocations = tk.Button(menuBar, text ="View Locations", command = partial(showLocations))
        viewAccount = tk.Button(menuBar, text ="View Account", command = partial(showAccounts))
        exitProgram = tk.Button(menuBar, text ="Exit", command = stopProgram)

        viewBooks.grid(row = 0, column = 0, padx = 10, pady = 2)
        viewLocations.grid(row = 0, column = 1, padx = 10, pady = 2)
        viewAccount.grid(row = 0, column = 2, padx = 10, pady = 2)
        exitProgram.grid(row = 0, column = 3, padx = 10, pady = 2)

        # BOOK VIEW

        bookFrame = tk.Frame(root)
        bookFrame.grid(row = 1)

        cursor.execute("SELECT book_id, book_name, details, author FROM book")
        books = cursor.fetchall()

        bookIdLabel = tk.Label(bookFrame, text = "Book ID")
        bookNameLabel = tk.Label(bookFrame, text = "Book Name")
        bookDetailsLabel = tk.Label(bookFrame, text = "Book Details")
        bookAuthorLabel = tk.Label(bookFrame, text = "Book Author")

        for book in books:
            bookIdLabel["text"] = bookIdLabel["text"] + "\n" + str(book[0])
            bookNameLabel["text"] = bookNameLabel["text"] + "\n" + str(book[1])
            bookDetailsLabel["text"] = bookDetailsLabel["text"] + "\n" + str(book[2])
            bookAuthorLabel["text"] = bookAuthorLabel["text"] + "\n" + str(book[3])

        bookIdLabel.grid(row = 0, column = 0, pady = 2)
        bookNameLabel.grid(row = 0, column = 1, pady = 2)
        bookDetailsLabel.grid(row = 0, column = 2, pady = 2)
        bookAuthorLabel.grid(row = 0, column = 3, pady = 2)

        # LOCATION VIEW

        locationFrame = tk.Frame(root)
        locationFrame.grid(row = 1)

        cursor.execute("SELECT store_id, locale FROM store")
        locations = cursor.fetchall()

        locationIdLabel = tk.Label(locationFrame, text = "Location ID")
        locationNameLabel = tk.Label(locationFrame, text = "Address")

        for location in locations:
            locationIdLabel["text"] = locationIdLabel["text"] + "\n" + str(location[0])
            locationNameLabel["text"] = locationNameLabel["text"] + "\n" + str(location[1])

        locationIdLabel.grid(row = 0, column = 0, pady = 2)
        locationNameLabel.grid(row = 0, column = 1, pady = 2)

        # ACCOUNT VIEW

        accountFrame = tk.Frame(root)
        accountFrame.grid(row = 1)

        accountInstructLabel = tk.Label(accountFrame, text = "Please enter a user id: ")
        accountEntry = tk.Entry(accountFrame)
        accountGet = tk.Button(accountFrame, text ="Go", command = partial(getAccount))

        accountInstructLabel.grid(row = 0, column = 0, pady = 2)
        accountEntry.grid(row = 0, column = 1, pady = 2)
        accountGet.grid(row = 0, column = 2, pady = 2)

        showBooks()
        tk.mainloop()
    else: 
        # IF all else fails... run.
        print("Option not found. Terminating program.")
