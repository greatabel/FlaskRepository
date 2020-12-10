"""App entry point."""
import os
import json

import flask_login
from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint, render_template

from movie import create_app
from movie.domain.model import Director, User, Review, Movie


app = create_app()
app.secret_key = "ABCabc123"
app.debug = True


login_manager = flask_login.LoginManager(app)
user_pass = {}

@app.route("/statistics", methods=['GET'])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, 'data.json')
    with open(filename) as test_file:
        d = json.load(test_file)
    print(type(d), '#'*10, d)
    return d

@login_manager.user_loader
def load_user(email):
    return user_pass.get(email, None)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = user_pass.get(email, None)
    if stored_user and password == stored_user.password:

        flask_login.login_user(stored_user)
        print(stored_user.is_active, 'login')
        return redirect(url_for('review'))
    else:
        print('login fail')
    return redirect(url_for('home_bp.home',pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home_bp.home',pagenum=1))
    # if DB.get_user(email):
    if email in user_pass:
        print('already existed user')
        return redirect(url_for('home_bp.home',pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print('register', email, pw1)
    user = User(email, pw1)
    user_pass[email] = user
    print('register', user_pass, '#'*5)
    return redirect(url_for('home_bp.home',pagenum=1))


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for('home_bp.home',pagenum=1))

reviews = []
@app.route("/review", methods=["GET", "POST"])
@flask_login.login_required
def review():
    if request.method == "POST":
        
        movie_name = request.form['movie_name']
        movie_id = request.form['movie_id']
        rtext = request.form['rtext']
        rating = request.form['rating']

        movie = Movie(movie_name, 1990, int(movie_id))
        review = Review(movie, rtext, int(rating))
        reviews.append(review)


    return render_template(
        'review.html',
        reviews=reviews,
        
    )



@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)

