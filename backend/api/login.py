
from flask import Blueprint, session, request
import json
from ..utils import Auth
login_bp = Blueprint('login', __name__)

login_dealer = Auth.Login()

@login_bp.route("/test")
def login_test():
    b = 1/0
    return 'test'

@login_bp.route("/login", methods=['POST'])
def api_login():
    """
        点击Login页面的登录时触发
    """
    params = json.loads(request.data)
    userid = params['userid']
    password = params['password']
    res = login_dealer.login(userid, password)
    # 若登录成功，更新session的username
    if res['code']==200:
        session['username']=res['data'].get('username')
    return res