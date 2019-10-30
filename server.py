"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route("/users")
def user_list():
    """Show list of users/"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register")
def register_form():

    return render_template("register_form.html")

@app.route("/register", methods= ["POST"])
def register_process():
    input_email = request.form.get('email')
    input_password = request.form.get('password')

    if User.query.filter_by(email = input_email).first():
        pass
    else:
        input_email = User(email = input_email, password = input_password)
        db.session.add(input_email)
        db.session.commit()

    return redirect("/")

@app.route("/login")
def login_user():

    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_process():

    login_email = request.form.get("email")
    login_password = request.form.get("password")
    print(login_password)

    check_login = User.query.filter_by(email = login_email).first()

    if check_login == None:
        flash("Incorrect input! You are stuck on this page. There is no redirect.")
        return render_template("login.html")

    if (login_email == check_login.email) and (login_password == check_login.password):
        flash("You were successfully logged in!")
        return redirect('/')

@app.route("/users/<int:user_id>")
def show_user_info():

    user_info = db.session.query.filter(User.user_id == user_id)
    user_rating = user_info.ratings

    for r in user_rating:
        print(r.movie.title)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
