# Movie Ticket Booking System w/ Tkinter GUI
Welcome to our movie ticket reservation application!  

Our project uses pymysql for our database connection and Python for our application (including tkinter, a
Python interface, to create the GUI). To ensure that the project is created and run properly, please follow
these steps:  

1) Ensure you have Python downloaded onto your system. You can check which version of Python 
is installed by simply typing 'python' into the command terminal. We recommend [adding Python to your system's PATH](https://www.makeuseof.com/python-windows-path/)
to ensure no errors occur when running the program. 
If Python does not exist on your system, please [install it](https://www.tomshardware.com/how-to/install-python-on-windows-10-and-11).  

2) Tkinter should be automatically installed with Python. To check if your system has tkinter, run
*python -m tkinter* from the command terminal. This should open a window demonstrating a
simple Tk interface, letting you know that tkinter is properly installed, and also showing what
version installed. For more information about tkinter, visit [this website](https://docs.python.org/3/library/tkinter.html).  

3) Ensure that you have downloaded PyMySql onto your system. To download with pip: enter the
command python -m pip install pymysql into the command terminal. For more information about
PyMySql, visit [this website](https://pypi.org/project/PyMySQL/).  

4) Download the zip file and extract all the contents from it. We recommend storing the folder in an easily accessible location (Desktop, Downloads, etc.)  

5) With the downloaded database dump provided (movie_final), import the database into MySQL Workbench. Make sure you have your connection username and password 
handy to run the Python app.  

6) Refresh the Schema window in MySQL. A new database, movie_final, should appear. Ensure that all functions and procedures are present:  
   - **Stored Procedures**
      - *addCustomer*
      - *addShowing*
      - *addTicket*
      - *deleteShowing*
      - *deleteTicket*
      - *getCustId*
      - *selectShowing*
      - *showAllShowings*
      - *showAllTicket*
      - *showShowing*
      - *showTicket*
      - *updateShowing*
   - **Functions**
      - *customerExist*
      - *customerSignin*
      - *getPriceId*
      - *managerSignin*  

7) In the command terminal, navigate to main.py. You can do so by typing “cd” followed by the filepath.  

8) Once you have navigated to the appropriate file location, run the app by typing "python main.py"  

9) The application will ask you for your database connection username and password. Once the application has successfully connected to the database, 
the tkinter GUI will appear.  

10) We have included two test users for our application (one customer, one manager).
    - Customer email: customer@test.com
    - Customer password: test123
    - Manager username: test_manager
    - Manager password: test1234  

11) Feel free to create a new customer account as well, and use that information to log in.

## Demo Video  
[![Movie Ticket Booking System Demo](https://github.com/jaimesi/Movie-Ticket-Booking-System/master/assets/thumbnail.jpg)](https://youtu.be/7uTTbUk_my0)
