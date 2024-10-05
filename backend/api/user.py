
from flask import Blueprint, session

user_bp = Blueprint('user', __name__)

@user_bp.route("/test")
def api_get_user_info():
    return 'test api'

@user_bp.route("/userinfo/get")
def api_get_userinfo():
    userinfo = {
        'username': session.get('username', 'Not Login!')
    }
    return userinfo