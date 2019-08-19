import functools

from flask import Blueprint, session

from models import User, db

users = Blueprint('users', __name__, url_prefix='/users')


def hash_password(pwd: str) -> str:
    return pwd


def admin_only(func):
    @functools.wraps(func)
    def _admin_only(*args, **kwargs):
        if 'role' in session.keys() and session['role'] == 'admin':
            return func(*args, **kwargs)
        else:
            raise PermissionError('Unauthorized')

    return _admin_only


def online(func):
    @functools.wraps(func)
    def _online(*args, **kwargs):
        if 'role' in session.keys() and session['role'] != 'guest':
            return func(*args, **kwargs)
        else:
            raise PermissionError('Unauthorized')

    return _online


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return 'guest', -1
    if user.pwd_hash == hash_password(password):
        return user.role, user.id
    else:
        return 'guest', -1


def register(username, password, name):
    user = User()
    user.username = username
    user.pwd_hash = hash_password(password)
    user.name = name
    user.description = ''
    db.session.add(user)
    db.session.commit()
    return True
