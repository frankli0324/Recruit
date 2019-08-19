import functools

from flask import Blueprint, request, session
from flask_restplus import Api, Resource

import challenges
import users

challenge = Blueprint('challenge', __name__, url_prefix='/api/challenge')
user = Blueprint('user', __name__, url_prefix='/api/user')
challenge_api = Api(challenge)
user_api = Api(user)


def wrap_api(func):
    @functools.wraps(func)
    def _wrap_api(*args, **kwargs):
        if 'role' not in session.keys():
            session['role'] = 'guest'
        ret = {}
        try:
            ret['code'] = 0
            ret['message'] = 'success'
            ret['data'] = func(*args, **kwargs)
        except PermissionError:
            ret['code'] = -1
            ret['message'] = 'unauthorized'
        except Exception:
            ret['code'] = 500
            ret['message'] = 'error'

        return ret

    return _wrap_api


@challenge_api.route('/')
class Challenge(Resource):
    @wrap_api
    @users.online
    def get(self):
        chall_id = request.args['id'] or request.form['id'] or request.json['id']
        return challenges.challenge_details(chall_id)

    @wrap_api
    @users.admin_only
    def post(self):
        if not request.is_json():
            return 'wrong parameters'
        r = request.get_json()
        return {
            'id': challenges.create_challenge(r)
        }


@challenge_api.route('/submit')
class ChallengeSubmit(Resource):
    @wrap_api
    @users.online
    def post(self):
        if not request.is_json():
            return 'wrong parameters'
        r = request.get_json()
        for i in ['id', 'content']:
            if i not in r.keys():
                return 'wrong parameters'
        challenges.submit_submission(r, session['id'])


@user_api.route('/')
class UserLogin(Resource):
    @wrap_api
    def post(self):
        form = request.form
        session['role'], session['id'] = users.login(form['username'], form['password'])
        return {'role': session['role']}
