from tkinter import *
from tkinter import messagebox

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

    def signup_button():
        username = str(customer_email.get())
        password = str(customer_pword.get())
        first_name = str(customer_fname.get())
        last_name = str(customer_lname.get())

        # TODO: Verify if user's email address is already in database
        # TODO: Verify that user's email address is correctly formatted

        if username == "" or password == "" or first_name == "" or last_name == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        else:
            try:
                insert_stmt = "insert into customer (email, password, first_name, last_name) values (%s, %s, %s, %s)"
                cursor.execute(insert_stmt, (username, password, first_name, last_name))

                customer_email.delete(0, END)
                customer_pword.delete(0, END)
                customer_fname.delete(0, END)
                customer_lname.delete(0, END)
                messagebox.showinfo(" ", "Sign up successful.\nPlease log in")
                window.destroy()
                customer_login()

            except:
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

# TODO: Customer login page
def customer_login():

    def login_button():
        username = str(customer_email.get())
        password = str(customer_pword.get())

        # TODO: Verify if user's email address and password match database


        if username == "" or password == "":
            messagebox.showwarning(" ", "All fields must be filled.")

# TODO: Customer home page
    # Home page has current movies being shown and buttons
    # Buttons should allow customers to book tickets, view their tickets booked, delete their bookings

# TODO: Customer book ticket page

# TODO: Customer view bookings page
    # Customer should only be able to view their tickets that are booked. They can delete their ticket.

# TODO: Manager login page

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

Button(window, text="Login", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), login_page()]).pack(pady=(300, 0))
Button(window, text="Sign Up", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), customer_signup()]).pack(pady=(20, 0))
Button(window, text="Quit", height=2, width=15, bg='black', fg='white', command=window.destroy).pack(pady=(20, 0))

window.mainloop()
