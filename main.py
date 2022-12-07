import tkinter
import webbrowser
from tkinter import *
from tkinter import messagebox
import re
from tkinter.ttk import Treeview

import pymysql.cursors

# Define global variables
customer_email = " "

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
                check_existing_user_stmt = "SELECT customerExist(%s)"
                cursor.execute(check_existing_user_stmt, email)

                num_rows = cursor.fetchone()

                # If a row is found, the customer account already exists
                if list(num_rows.values())[0] >= 1:
                    messagebox.showwarning(" ", "There is already an account associated with this email address. "
                                                "Please login instead.")
                else:
                    # Insert values into customer table
                    insert_stmt = "CALL addCustomer(%s, %s, %s, %s)"
                    cursor.execute(insert_stmt, (email, password, first_name, last_name))

                    # Delete text box contents
                    customer_email.delete(0, END)
                    customer_pword.delete(0, END)
                    customer_fname.delete(0, END)
                    customer_lname.delete(0, END)
                    messagebox.showinfo(" ", "Sign up successful.\nPlease log in")
                    window.destroy()

                    # Automatically bring new user to login page
                    customer()

            except Exception as e:
                messagebox.showwarning(" ", "Values entered are either not unique or empty.")
                print(e)

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
           command=lambda: [window.destroy(), customer()]).pack(pady=(10, 0))

    window.mainloop()


# Customer functions
def customer():
    # Customer login page
    def login_button():
        customer_login_email = str(cust_email.get())
        customer_login_password = str(cust_pword.get())

        global customer_email
        customer_email = str(cust_email.get())

        # No input can be left blank
        if customer_login_email == "" or customer_login_password == "":
            messagebox.showwarning(" ", "All fields must be filled.")
        else:
            try:
                # Verify if customer's email address and password match database
                select_stmt = "SELECT customerSignin(%s, %s)"
                cursor.execute(select_stmt, (customer_login_email, customer_login_password))

                # Check to see if a value is returned
                num_rows = cursor.fetchone()

                # If no rows are found, the customer account does not exist
                if list(num_rows.values())[0] == 0:
                    messagebox.showwarning(" ", "There is no account associated with this email address.")

                # If the account exists and the password matches, go to home page of the customer
                else:
                    window.destroy()
                    customer_home_page()
                connection.commit()

            except Exception as e:
                messagebox.showwarning(" ", "An error occurred.")
                print(e)

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

    # Customer home page
    def customer_home_page():
        # Customer homepage window
        window = Tk()

        window.geometry('1180x550')

        window.title("Home Page")

        # Opening images of the movie posters
        black_adam_poster = PhotoImage(file='assets/black_adam_poster.gif')
        black_panther_wakanda_forever_poster = PhotoImage(file='assets/black_panther_wakanda_forever_poster.gif')
        the_menu_poster = PhotoImage(file='assets/the_menu_poster.gif')
        ticket_to_paradise_poster = PhotoImage(file='assets/ticket_to_paradise_poster.gif')

        # Header for movies currently playing
        movie_showings_text = Label(window, text="Movies Currently Playing", fg='black', height=3,
                                    font='Helvetica 18 bold')
        movie_showings_text.grid(columnspan=2, column=0, row=1)

        # Manage bookings button
        manage_bookings_button = Button(window, text="Manage Bookings", fg='white', bg='maroon',
                                        height=2, width=20, font='Helvetica 12 bold',
                                        command=lambda: [window.destroy(), customer_manage_bookings()])
        manage_bookings_button.grid(column=2, row=1, pady=20)

        # Logout button
        logout_button = Button(window, text="Logout", fg='white', bg='maroon',
                               height=2, width=10, font='Helvetica 12 bold',
                               command=lambda: [window.destroy(), customer()])
        logout_button.grid(column=3, row=1, pady=20)

        # Functions to open movie trailers on button click
        def black_adam_trailer():
            webbrowser.open_new(r"https://youtu.be/X0tOpBuYasI")

        def black_panther_trailer():
            webbrowser.open_new(r"https://youtu.be/_Z3QKkl1WyM")

        def the_menu_trailer():
            webbrowser.open_new(r"https://youtu.be/C_uTkUGcHv4")

        def ticket_to_paradise_trailer():
            webbrowser.open_new(r"https://youtu.be/hkP4tVTdsz8")

        # Creating buttons with the movie posters as the image
        black_adam_button = Button(window, image=black_adam_poster, command=black_adam_trailer)
        black_adam_button.grid(column=0, row=2, padx=10)

        black_panther_button = Button(window, image=black_panther_wakanda_forever_poster,
                                      command=black_panther_trailer)
        black_panther_button.grid(column=1, row=2, padx=10)

        the_menu_button = Button(window, image=the_menu_poster, command=the_menu_trailer)
        the_menu_button.grid(column=2, row=2, padx=10)

        ticket_to_paradise_button = Button(window, image=ticket_to_paradise_poster,
                                           command=ticket_to_paradise_trailer)
        ticket_to_paradise_button.grid(column=3, row=2, padx=10)

        window.mainloop()


# TODO: Customer manage bookings page
def customer_manage_bookings():
    # TODO: dropdown of all movies. Customer can pick a movie. List of showings for that day will appear.
    # TODO: back button to go back to home page
    # TODO: frame to view all their current reservations. They can delete these tickets
    # TODO: ticket info shown should be their first name, last name, movie name, day of showing, time of showing, auditorium number, number of seats booked

    # Customer book ticket window
    window = Tk()
    window.geometry('700x700')
    window.title("Book Tickets")

    # Movie booking header
    movie_booking_header = Label(window, text="Book Tickets", fg='white', bg='black', width=40,
                                 font='Helvetica 18 bold')
    movie_booking_header.grid(row=0, column=0, columnspan=8, pady=10)

    pick_movie = Label(window, text="Select a Movie:", fg='black', font='Helvetica 12')
    pick_movie.grid(row=1, column=0, columnspan=2)

    # Function to display showing info when user selects a dropdown menu item
    def display_selected(choice):

        # Get user's movie choice
        choice = var.get()

        # Treeview to display all showings of that movie
        treeview = Treeview(window)
        treeview['columns'] = ('Time', 'Date', 'Price')
        treeview.column('#0', width=0, stretch=NO)
        treeview.column('Time', anchor=CENTER, width=80)
        treeview.column('Date', anchor=CENTER, width=80)
        treeview.column('Price', anchor=CENTER, width=80)

        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('Time', text='Time', anchor=CENTER)
        treeview.heading('Date', text='Date', anchor=CENTER)
        treeview.heading('Price', text='Price', anchor=CENTER)

        # treeview.insert(parent='', index=0, iid=0, text='', values=('values[0]', 'values[1]', 'values[2]'))
        # treeview.insert(parent='', index=1, iid=1, text='', values=('1430', '2022 - 11 - 28', '$13'))
        # treeview.insert(parent='', index=2, iid=2, text='', values=('1030', '2022 - 11 - 29', '$15'))
        treeview.grid(row=100, column=2, columnspan=4)

        cursor.callproc('showShowing', (choice, ))

        i = 0

        for row in cursor.fetchall():
            values = list(row.values())
            treeview.insert(parent='', index=i, iid=i, text='', values=values)
            i = i + 1

        # # Iterate through each row of the procedure and create a label
        # i = 201
        # for row in cursor.fetchall():
        #     for j in range(len(list(row.values()))):
        #         e = Label(window, width=10, text=list(row.values())[j], anchor='w', borderwidth=2, relief='ridge')
        #         e.grid(row=i, column=j)
        #         # show the delete button
        #         e = Button(window, width=10, text='Delete Ticket', fg='red', relief='ridge',
        #                        anchor="w", command=lambda k=list(row.values())[0]: delete_ticket(k))
        #         e.grid(row=i, column=8)
        #     i = i + 1

    # Dropdown menu to choose movie
    movie_choices = ["Black Adam", "Black Panther: Wakanda Forever", "The Menu", "Ticket to Paradise"]
    var = StringVar()  # Stringvar to store the value of options
    var.set(movie_choices[0])  # sets the default option of options

    movie_options = OptionMenu(window, var, *movie_choices, command=display_selected)
    movie_options.grid(row=1, column=2, columnspan=4)

    # Showing all tickets purchased by the customer
    booked_tickets_header = Label(window, text="Your Tickets", fg='white', bg='black', width=40,
                                  font='Helvetica 18 bold')
    booked_tickets_header.grid(row=199, column=0, columnspan=8, pady=10)

    # Retrieve customer_id number from customer_email
    def display():
        get_customer_id = "SELECT customer_id FROM customer WHERE email = %s"
        cursor.execute(get_customer_id, customer_email)

        cust_id_row = cursor.fetchone()

        # Set customer id
        cust_id = int(cust_id_row['customer_id'])

        cursor.callproc('showTicket', (cust_id,))

        # Headers for each column
        e = Label(window, width=10, text='Ticket ID', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=0)
        e = Label(window, width=10, text='First Name', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=1)
        e = Label(window, width=10, text='Last Name', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=2)
        e = Label(window, width=10, text='Movie', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=3)
        e = Label(window, width=10, text='Auditorium', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=4)
        e = Label(window, width=10, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=5)
        e = Label(window, width=10, text='Time', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=6)
        e = Label(window, width=10, text='# Seats', borderwidth=2, relief='ridge', anchor='w', bg='grey')
        e.grid(row=200, column=7)

        # Iterate through each row of the procedure and create a label
        i = 201
        for row in cursor.fetchall():
            for j in range(len(list(row.values()))):
                e = Label(window, width=10, text=list(row.values())[j], anchor='w', borderwidth=2, relief='ridge')
                e.grid(row=i, column=j)
            # show the delete button
            e = Button(window, width=10, text='Delete Ticket', fg='red', relief='ridge',
                       anchor="w", command=lambda k=list(row.values())[0]: delete_ticket(k))
            e.grid(row=i, column=8)
            i = i + 1

    display()

    # Helper function to delete ticket in database
    def delete_ticket(t_id):
        try:
            popup = messagebox.askyesnocancel("Delete Record",
                                              "Are you sure you want to delete your reservation? ", icon='warning')
            if popup:
                delete_ticket_stmt = "DELETE FROM ticket WHERE ticket_id = %s"
                ticket_id = [t_id]
                cursor.execute(delete_ticket_stmt, ticket_id)
                print("Row Deleted  ")

                for ticket in window.grid_slaves():  # remove widgets
                    ticket.grid_forget()
                display()  # refresh the list
        except Exception as e:
            print(e)

    window.mainloop()


# Manager login page
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
                    manager_home_page()
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


# TODO: Manager home page with all tickets booked (can delete) and add/update/delete showings


# Starting page with login, sign up, and quit buttons
window = Tk()

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

window.title("Moving Ticket Booking Program")
window.option_add("*font", "aerial 15")

Button(window, text="Customer Login", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), customer()]).pack(pady=(200, 0))
Button(window, text="Manager Login", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), manager_login()]).pack(pady=(20, 0))
Button(window, text="Customer Sign Up", height=2, width=15, bg='black', fg='white',
       command=lambda: [window.destroy(), customer_signup()]).pack(pady=(100, 0))
Button(window, text="Quit", height=2, width=15, bg='black', fg='white', command=window.destroy).pack(pady=(20, 0))

window.mainloop()
