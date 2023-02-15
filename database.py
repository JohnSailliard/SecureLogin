import sqlite3
import random
import hashlib
import os
from datetime import datetime

# Constants for password functions
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
SPECIAL_CHAR = "!@#$%^&*"
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 25

# Function to salt a password
def password_verification(plain_text, salt=''):
    # Creates a set of random characters for the salt variable
    salt = str(os.urandom(40))
    salt = salt[:40]

    # Salting the password
    hashable = salt + plain_text  
    hashable = hashable.encode('utf-8') 
    this_hash = hashlib.sha1(hashable).hexdigest()

    # Returning the salted password
    return salt + this_hash

# Function to verify password strength, returns the password that will be used
def password_creation(password):
    # Checking if the passworth matches length requirements and if they are all text/num
    if password.isalnum() or password.isalpha():
        print("\nYour password cannot be solely numbers or characters. You need at least one of each.\n")
        return 1
    if len(password) < PASSWORD_MIN_LENGTH:
        print("\nYour password must be at least 8 characters long.\n")
        return 1
    if len(password) > PASSWORD_MAX_LENGTH:
        print("\nYour password cannot be more then 25 characters\n")
        return 1

    # Initializing bool variables
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False

    # Checks each character and sees if it satisfies one of the requirements
    for ch in password:
        if ch in SPECIAL_CHAR:
            special_char_check = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        print("\nYour password needs at least one uppercase character, one lowercase character, a digit, and a special character\n")
        return 1
    else:
        # Returning the created password with the salt
        print("Your new password is: " + password)
        return str(password_verification(password))

# Function to create a database for the program
def create_db():
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()

        # Creating a database table
        c.execute('''CREATE TABLE users
                    (
                    netId text,
                    password text,
                    accessLevel int,
                    dateAdded text
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# Function to get the current time
def get_date():
    # Generate timestamp for data inserts 
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")

# Function to generate a random password
def rand_pw():
    # Random length of the password and position of the required number and special char
        password_length = random.randint(8, 25)
        special_char_location = random.randint(0, password_length)
        number_location = random.randint(0, password_length)

        # In case the location of these two variables is the same
        if special_char_location == number_location:
            if (number_location + 1) > password_length:
                number_location = number_location - 1
            else:
                number_location = number_location + 1
        
        # Randomly generating each value of the password
        password = ("")
        for i in range (password_length):
            # Setting the value of the special char
            if i == special_char_location:
                temp = str(random.choice(SPECIAL_CHAR))
                password = password + temp
            # Setting the value of the number
            elif i == number_location:
                temp = str(random.randint(0, 9))
                password = password + temp
            # Alternating uppercase vs lowercase random letter placements
            elif (i % 2) != 0:
                temp = str(random.choice(ALPHABET))
                password = password + temp.upper()
            else:
                temp = str(random.choice(ALPHABET))
                password = password + temp
        
        # Returning the generated password for the user with the salt
        print("You new password is: " + password)
        return str(password_verification(password))

# Function to create a new user and load it into the database
def add_user(userName, password):
    # Adding username with handling
    if len(userName) < 3:
        print("Your netId has to be at least 3 characters long.")
        return 1

    # New access level which defaults to 1
    new_access_level = 1

    # Date of addition
    new_user_date = str(get_date())

    # Insert query
    data_to_insert = [(userName, password_verification(password), new_access_level, new_user_date)]

    # Try to insert into the database
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# Function to return all info in the database
def query_db():
    # Display all records in the users table
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# Function that takes the netid and pw to see if its in the database
def sign_in(userName, password, curr_attempts):
    # To track login attempts
    login_attempts = 0

    # Kicking user out if too many attempts
    if curr_attempts > 3:
        print("You have failed more then 3 login attempts. You are being locked out now.")
        return 2

    # Creating reader variable and the file try/except
    try: 
        # Accessing the database
        conn = sqlite3.connect('user.db')
        c = conn.cursor()

        # Parses each row of the database and checks if the netId matches the salted version of the password
        for row in c.execute("SELECT * FROM users"):
            row_list = row.split(", ")
            if row_list[0] == userName and row_list[1] == password_verification(password):
                return 0
            else:
                login_attempts += 1
                return 1   

    # If the database is unaccessable
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")

    # Closing access at the end
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# Creating the database
create_db() 
#add_user("jsaillia", "password")
#add_user("jeddy", "1234")
#add_user("testing", "qwerty")
#query_db()