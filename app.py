from flask import Flask
from flask import Flask, render_template, request
from database import *

app = Flask(__name__)

# Render the home page
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Setting the page for a sign in choice
        chkSignIn = request.form.get("chkSignIn")
        if chkSignIn == 1:
            return render_template("signIn.html")

        # Setting the page for a new user choice
        chkCreate = request.form.get("chkCreate")
        if chkCreate == 1:
            return render_template("newUser.html")

    return render_template("index.html")

# Render the sign in page
@app.route("/signIn", methods=['GET', 'POST'])
def signIn():
    # To track login attempts
    attempts = 1

    if request.method == 'POST':
        # Getting input for the sign in
        userName = request.form.get("txtNetId")
        password = request.form.get("txtPassword")

        # Running verification functions on it
        var = sign_in(userName, password, attempts)
        if var == 2:
            print("You are being locked out")
            return 0
        elif var == 1:
            attempts += 1

        if var == 0:
            return render_template("success.html")

    # Default render
    return render_template("signIn.html")

# Render the newUser page
@app.route("/newUser", methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        # Getting input for the sign in
        userName = request.form.get("txtNetIdNew")
        password = request.form.get("txtPasswordNew")
        chkRandPw = request.form.get("chkRandPw")

        # If the user wants a randomly generated password
        if chkRandPw == 1:
            # Generating the password
            password = rand_pw()

            # Adding the user
            var = add_user(userName, password) != 1

            # Checking if user was added and returning the success page if so
            if var != 1:
                return render_template("success.html")
            else:
                return render_template("newUser.html")

        # Regular sign in process without the choice of random
        password_creation(password)
        var = add_user(userName, password)

        # Checking if user was added and returning the success page if so
        if var != 1:
            return render_template("success.html")

    # Default render
    return render_template("newUser.html")