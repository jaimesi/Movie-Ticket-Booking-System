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
        s1 = str(se1.get())
        s2 = str(se2.get())
        s3 = str(se3.get())
        s4 = str(se4.get())

        # TODO: Verify if user's email address is already in database
        # TODO: Verify that user's email address is correctly formatted

        if s1 == "" or s2 == "" or s3 == "" or s4 == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        else:
            try:
                insert_stmt = "insert into customer (email, password, first_name, last_name) values (%s, %s, %s, %s)"
                cursor.execute(insert_stmt, (s1, s2, s3, s4))

                se1.delete(0, END)
                se2.delete(0, END)
                se3.delete(0, END)
                se4.delete(0, END)
                messagebox.showinfo(" ", "Sign up successful.\nPlease log in")
                window.destroy()
                # login_page()

            except:
                messagebox.showwarning(" ", "Values entered are either not unique or empty.")

        connection.commit()

    # Customer sign up window
    window = Tk()

    window.geometry('800x800')

    window.title("New User Sign Up")
    window.option_add("*font", "aerial 15")

    Label(window, text="Email Address", fg='white', bg='black', width=20).pack(pady=(200, 0))
    se1 = Entry(window)
    se1.pack()

    Label(window, text="Password", fg='white', bg='black', width=20).pack(pady=(20, 0))
    se2 = Entry(window)
    se2.pack()

    Label(window, text="First Name", fg='white', bg='black', width=20).pack(pady=(20, 0))
    se3 = Entry(window)
    se3.pack()

    Label(window, text="Last Name", fg='white', bg='black', width=20).pack(pady=(20, 0))
    se4 = Entry(window)
    se4.pack()

    Button(window, text="Sign Up", fg='white', bg='black', height=1, width=10, command=signup_button).pack(
        pady=(20, 0))
    Button(window, text="Back", fg='white', bg='black', height=1, width=10,
           command=lambda: [window.destroy(), login_page()]).pack(pady=(10, 0))

    window.mainloop()

# TODO: Customer login page

# TODO: Manager login page

# TODO: Customer home page
    # Customer should be able to view current movies, book tickets, view their tickets booked, delete their bookings

# TODO: Manager home page
    # Manager should be able to view all tickets booked, add showings, delete showings

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
