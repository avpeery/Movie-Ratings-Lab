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

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter((User.email == email), (User.password == password)).first()

    if user: 
        session['user_email'] = user.email
        session['user_id'] = user.user_id

        flash("Succesfully logged in!")
        return render_template("user_info.html", user=user)

    flash("That is not a valid email and password")
    return redirect('/login')


@app.route("/logout")
def logout_user():

    del session['user_email']
    del session['user_id']
    flash('Succesfully logged out!')

    return redirect('/')


@app.route("/movie")
def show_movie_title():

    movie_info = Movie.query.first()

    return render_template("movie_info.html",
                            movie_info = movie_info)


@app.route("/movies")
def list_movies():

    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie_info(movie_id):

    movie = Movie.query.filter_by(movie_id = movie_id).first()

    return render_template("movie_info.html",
                            movie = movie)


@app.route("/user-page")
def show_logged_in(user_id):

    user = User.query.filter_by(user_id = session['user_id']).first()

    return render_template("user_info.html",
                            user = user)


@app.route("/users/<int:user_id>")
def show_user_info(user_id):

    user = User.query.filter_by(user_id = user_id).first()

    return render_template("user_info.html",
                            user = user)

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
