This program creates a sign in/adding user webpage. The initial page that is loaded is the index page. in the index page
there are two checkboxes that prompt the user to choose between the two: sign in or create a new account. Depending on which
option is selcted changes what happens and what is loaded next. Currently I am hitting an Error 500 whenever I connect to the
website and I am having an issue with finding the core to the problem so I have not been able to access the actual webpage
format of this program.

To prep this assignment, uncomment the final few lines in the database.py file and run it. This will create a database
that has the necessary fields and is started with a few baseline entries. This function will also salt the provided 
passwords before loading them into the database through the password_verification function.

- Sign In Page -
In the sign in page, there are two text boxes for the user to type into. It will take in the users netId and password. After
clicking the 'submit' button, the program will keep track of the amount of login attempts that the user has used, ending the 
session after exceeding 3. In the case of a successful login, the process that allows happens by loading in the two parameters
from the login page (as well as the login attempts) to the sign_in function. This function connects with the databse and runs
through the rows looking for an entry that matches the provided username as well as the salted version of the provided password.
In the case of a successful login, the user is taken to the "success" page where it will provide a message that the attempt was
successful. Otherwise, if the users session isnt ended and there is not a successful login, then the user will simply stay on
the page and try again.

-Create New User Page-
In this page the user can simply write into the provdied textboxes and hit submit to create an account, or the user can select
for a randomly generated password. If the checkbox is checked, even if the user wrote in a password, then the used password
will be the randomly generated one. After submitting the form, the password will be run through the password_creation function which
will check the strength of the password, and if it passes it will return the salted form of the password. The username will be checked 
by the add_user function to make sure it as at least three characters. After these checks are run and passed, the user will be added.
In the case of a random password, the random_pw function will be called in place of the provided password. This function randomly generates
a length between 8 and 25 and then rendomly chooses two indexes to place a randomly chosen special character and a randomy chosen
number. If these two indexes are accidentally the same, the program will see if there is room to increment the numbers location, and if
not, it will reduce the numbers location. After the placings and size are determined, a for loop is run that places the number
and special character in their respective locations, and then randomly chooses a letter for every other one, alternating between
uppercase and lowercase.