from flask import Blueprint, render_template

view = Blueprint('view', __name__, url_prefix='/')


@view.route('/')
def index():
    return render_template('index.html')


@view.route('/login')
def login():
    return render_template('login.html')


@view.route('/register')
def register():
    return render_template('register.html')


@view.route('/challenges')
def challenges():
    return render_template('challenges.html')
