'''Handles routing and runs program'''
from datetime import datetime
import os
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from passlib.hash import sha256_crypt
from app import create_app, login_manager
from app.forms import LoginForm, RegistrationForm
from app.models import User

app = create_app() # create app instance
now = datetime.now() # current date/time
dt_now = now.strftime("%m/%d/%Y, %H:%M:%S") # format for display

# redirects user to login page and flashes message
# if they try to directly access a page and are not logged in
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."

@app.route("/")
def index():
    '''Render index page for users not logged in'''
    # redirect user if they're already logged in
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("userhome"))
    return render_template("guest.html", dt_now = dt_now)

@app.route("/userhome")
@login_required
def userhome():
    '''Render home page for logged-in users'''
    return render_template("userhome.html", dt_now = dt_now)

@app.route("/zebra")
@login_required
def zebra():
    '''Render Zebra page'''
    return render_template("zebra.html", dt_now = dt_now)

@app.route("/tater")
@login_required
def tater():
    '''Render Tater page'''
    return render_template("tater.html", dt_now = dt_now)

@app.route("/foodstable")
@login_required
def foodstable():
    '''Render foods table page'''
    return render_template("foodstable.html", dt_now = dt_now)

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Render login page'''
    # redirect user if they're already logged in
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("userhome"))
    # create instance of login form object
    form = LoginForm()
    # check if it is a valid POST request
    if form.validate_on_submit():
        user1 = User(username=form.username.data)
        user1.set_password(form.password.data)
        # if there are already registered users
        # the file will exist
        if os.path.exists("data.txt"):
            # read-only access
            with open("data.txt", "r", encoding="utf-8") as fr:
                for line in fr.readlines():
                    user_info = line.strip().split(",")
                    uname = user_info[0]
                    hash_pass = user_info[1]
                    # log in if correct username and password
                    if (uname == user1.username) and (
                        sha256_crypt.verify(form.password.data, hash_pass)
                        ):
                        login_user(user1)
                        flash("Login successful!")
                        return redirect(url_for("userhome")) # redirect to user home
                # if none of the username/password combos match up to user entry, try again
                flash("Sorry, login info incorrect. Please try again.")
                return redirect(url_for("login")) # redirect to login
        else:
            flash("You are the very first user! Please register now.")
            return redirect(url_for("registration"))
    return render_template("login.html", form = form, dt_now = dt_now)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    '''Render registration page'''
    # redirect user if they're already logged in
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("userhome"))
    # create instance of registration form object
    form = RegistrationForm()
    # check if it is a valid POST request
    if form.validate_on_submit():
        user1 = User(username=form.username.data)
        user1.set_password(form.password.data)
        # need append and read access to file
        # if file exists already, check existing usernames
        if os.path.exists("data.txt"):
            with open("data.txt", "a+", encoding="utf-8") as fa:
                fa.seek(0) # move cursor to beginning
                for line in fa.readlines():
                    user_info = line.strip().split(",")
                    uname = user_info[0]
                    print(uname)
                    if uname == user1.username:
                        flash("Username already exists, please enter a unique username.")
                        return render_template("registration.html", form = form, dt_now = dt_now)
                # if username doesn't already exist, append to file
                fa.seek(0,2) # move cursor to end
                fa.write(user1.username + "," + user1.password + "\n")
                login_user(user1)
                flash("Registration successful, thank you for registering!")
                return redirect(url_for("userhome"))
        # if file doesn't exist already, create file and write username/password to file
        else:
            with open("data.txt", "a+", encoding="utf-8") as fa:
                fa.write(user1.username + "," + user1.password + "\n")
                login_user(user1)
                flash("Registration successful, thank you for registering!")
                return redirect(url_for("userhome"))
    return render_template("registration.html", form = form, dt_now = dt_now)

@app.route("/logout")
def logout():
    '''Logs user out of session'''
    logout_user()
    # redirects user to index
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
