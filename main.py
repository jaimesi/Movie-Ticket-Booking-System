from tkinter import *
from tkinter import messagebox
import re

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             database='movie_final',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

cursor = connection.cursor()


# Customer signup page
def customer_signup():
    # Expression for validating an email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def signup_button():
        email = str(customer_email.get())
        password = str(customer_pword.get())
        first_name = str(customer_fname.get())
        last_name = str(customer_lname.get())

        # Verify that all fields are filled for the sign-up sheet
        if email == "" or password == "" or first_name == "" or last_name == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        # Verify that the user's email address is correctly formatted
        elif re.fullmatch(regex, email) is None:
            messagebox.showwarning(" ", "Please enter a valid email address.")
        else:
            try:
                # Check if the email address already has an account associated with it
                check_existing_user_stmt = "SELECT COUNT(*) FROM customer WHERE email = %s"
                cursor.execute(check_existing_user_stmt, email)

                num_rows = cursor.fetchone()

                # If a row is found, the customer account already exists
                if num_rows['COUNT(*)'] >= 1:
                    messagebox.showwarning(" ", "There is already an account associated with this email address. "
                                                "Please login instead.")
                else:
                    # Insert values into customer table
                    insert_stmt = "INSERT INTO customer (email, password, first_name, last_name) " \
                                  "VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_stmt, (email, password, first_name, last_name))

                    # Delete text box contents
                    customer_email.delete(0, END)
                    customer_pword.delete(0, END)
                    customer_fname.delete(0, END)
                    customer_lname.delete(0, END)
                    messagebox.showinfo(" ", "Sign up successful.\nPlease log in")
                    window.destroy()

                    # Automatically bring new user to login page
                    customer_login()

            except Exception as e:
                messagebox.showwarning(" ", "Values entered are either not unique or empty.")

        connection.commit()

    # Customer sign up window
    window = Tk()

    window.geometry('800x800')

    window.title("New User Sign Up")
    window.option_add("*font", "aerial 15")

    Label(window, text="Email Address", fg='white', bg='black', width=20).pack(pady=(200, 0))
    customer_email = Entry(window)
    customer_email.pack()

    Label(window, text="Password", fg='white', bg='black', width=20).pack(pady=(20, 0))
    customer_pword = Entry(window)
    customer_pword.pack()

    Label(window, text="First Name", fg='white', bg='black', width=20).pack(pady=(20, 0))
    customer_fname = Entry(window)
    customer_fname.pack()

    Label(window, text="Last Name", fg='white', bg='black', width=20).pack(pady=(20, 0))
    customer_lname = Entry(window)
    customer_lname.pack()

    Button(window, text="Sign Up", fg='white', bg='black', height=1, width=10, command=signup_button).pack(
        pady=(20, 0))
    Button(window, text="Back", fg='white', bg='black', height=1, width=10,
           command=lambda: [window.destroy(), customer_login()]).pack(pady=(10, 0))

    window.mainloop()


# Customer login page
def customer_login():
    def login_button():
        customer_login_email = str(cust_email.get())
        customer_login_password = str(cust_pword.get())

        # No input can be left blank
        if customer_login_email == "" or customer_login_password == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        else:
            try:
                # Verify if customer's email address and password match database
                select_stmt = "SELECT COUNT(*) FROM customer WHERE email = %s AND password = %s"
                cursor.execute(select_stmt, (customer_login_email, customer_login_password))

                # Check to see if a value is returned
                num_rows = cursor.fetchone()

                # If no rows are found, the customer account does not exist
                if num_rows["COUNT(*)"] == 0:
                    messagebox.showwarning(" ", "There is no account associated with this email address.")

                # If the account exists and the password matches, go to home page of the customer
                else:
                    window.destroy()
                    home_page(customer_login_email)
                connection.commit()

            except Exception as e:
                messagebox.showwarning(" ", "An error occurred.")

    # Customer login window
    window = Tk()

    window.geometry('800x800')

    window.title("Customer Login")
    window.option_add("*font", "aerial 15")

    Label(window, text="Email Address", fg='white', bg='black', width=20).pack(pady=(250, 0))
    cust_email = Entry(window)
    cust_email.pack()

    Label(window, text="Password", fg='white', bg='black', width=20).pack(pady=(10, 0))
    cust_pword = Entry(window)
    cust_pword.pack()

    Button(window, text="LOGIN", fg='white', bg='black', height=1, width=20, command=login_button).pack(pady=(20, 0))
    Button(window, text="CREATE ACCOUNT", fg='white', bg='black', height=1, width=20,
           command=lambda: [window.destroy(), customer_signup()]).pack(pady=(10, 0))
    Button(window, text="QUIT", fg='white', bg='black', height=1, width=20, command=window.destroy).pack(pady=(10, 0))


# TODO: Customer home page
# Home page has current movies being shown and buttons
# Buttons should allow customers to book tickets, view their tickets booked, delete their bookings

# TODO: Customer book ticket page

# TODO: Customer view bookings page
# Customer should only be able to view their tickets that are booked. They can delete their ticket.

# TODO: Manager login page
def manager_login():
    def manager_login_button():
        manager_username = str(manager_user.get())
        manager_password = str(manager_pword.get())

        # No input can be left blank
        if manager_username == "" or manager_password == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        else:
            try:
                # Verify if manager's username and password match database
                manager_select_stmt = "SELECT COUNT(*) FROM manager WHERE username = %s AND password = %s"
                cursor.execute(manager_select_stmt, (manager_username, manager_password))

                # Check to see if a value is returned
                num_rows = cursor.fetchone()

                # If no rows are found, the manager account does not exist
                if num_rows["COUNT(*)"] == 0:
                    messagebox.showwarning(" ", "Incorrect manager login information. Try again.")

                # If the account exists and the password matches, go to home page of the manager
                else:
                    window.destroy()
                    manager_home_page(manager_username)
                connection.commit()

            except Exception as e:
                messagebox.showwarning(" ", "An error occurred.")

    # Manager login window
    window = Tk()

    window.geometry('800x800')

    window.title("Manager Login")
    window.option_add("*font", "aerial 15")

    Label(window, text="Username", fg='white', bg='black', width=20).pack(pady=(250, 0))
    manager_user = Entry(window)
    manager_user.pack()

    Label(window, text="Password", fg='white', bg='black', width=20).pack(pady=(10, 0))
    manager_pword = Entry(window)
    manager_pword.pack()

    Button(window, text="LOGIN", fg='white', bg='black', height=1, width=20, command=manager_login_button).pack(
        pady=(20, 0))
    Button(window, text="QUIT", fg='white', bg='black', height=1, width=20, command=window.destroy).pack(
        pady=(10, 0))


# TODO: Manager home page
# Buttons to view all tickets booked, manage showings

# TODO: Manager view bookings page
# Manager should be able to view all tickets booked in database

# TODO: Manager manage showings page
# Manager should be able to add or delete showings


# Starting page with login, sign up, and quit buttons
window = Tk()

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

window.title("Moving Ticket Booking Program")
window.option_add("*font", "aerial 15")

Button(window, text="Customer Login", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), customer_login()]).pack(pady=(200, 0))
Button(window, text="Manager Login", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), manager_login()]).pack(pady=(20, 0))
Button(window, text="Customer Sign Up", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), customer_signup()]).pack(pady=(100, 0))
Button(window, text="Quit", height=2, width=15, bg='black', fg='white', command=window.destroy).pack(pady=(20, 0))

window.mainloop()
