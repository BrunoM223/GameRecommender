from models.user import User
from models.errors import UserError
from flask import Blueprint as bt, request as rq, render_template as rt, session, redirect, url_for

user_blueprint = bt('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if rq.method == 'POST':
        username = rq.form['username']
        password = rq.form['password']
        try:
            User.register_user(username, password)
            session['username'] = username
            return redirect(url_for("games.rated"))
        except UserError as e:
            return e.messagge
    return rt("users/register.html")


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if rq.method == 'POST':
        username = rq.form['username']
        password = rq.form['password']
        try:
            if User.login_valid(username, password):
                session['username'] = username
                return redirect(url_for("games.rated"))
        except UserError as e:
            return e.message
    return rt("users/login.html")


@user_blueprint.route('/logout', methods=['GET'])
def logout():
    if session['username'] != '':
        session.pop('username')
        return rt("home.html")