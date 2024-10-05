import functools
import requests
import flask

class Login(object):
    def __init__(self):
        self.tokens = {}  # token : userid
        self.user_info = {
            '123': {'username' : "璇天凤舞",
                    'password' : "123"
                    }
        }

    def validate_session(self, token):
        username = self.tokens.get(token)
        return username

    def login(self, userid, password):

        res = {
            'code': 404,
            'msg':  'Login Failed!',
            'data': {}
        }
        if userid in self.user_info:
            if password == self.user_info.get(userid)['password']:
                username = self.user_info.get(userid)['username']
                token    = self._generate_new_token(userid)
                res = { 'code': 200,
                        'msg':  'Login Success!',
                        'data': {'username' : username,
                                 'token'    : token
                                }
                }
        return res

    def _generate_new_token(self, userid):
        new_token = 'T'+userid
        self.tokens[new_token] = userid
        return new_token

class SSO(object):
    def __init__(self):
        self.validate_error_callback = None

    def error_handler(self, f):
        """
            鉴权流程异常时的处理函数
        """
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            """
                生成401错误
            """
            res = f(*args, **kwargs)
            if type(res) == str:
                res = flask.make_response(res)
                res.status_code = 401
            return res

        self.validate_error_callback = decorated
        return decorated

    def _sso(self):
        """
        sso 登陆
        """
        flask.flash('No ticket, redirect to UUAP ...')
        url = '{}?url={}'.format(flask.url_for('login'), flask.request.path)
        return flask.redirect(url)

    def _validate_session(self, token):
        """
        验证token(p/s),获取用户信息
        :param   token:
        :return  user:  str|None
        """
        res = requests.get('/api/login/validate_token')
        if res['code'] == 200 and res['msg'] == 'success':
            return res['result']
        else:
            return None

    def login_required(self, f):
        """
            用于在request前进行登录检测，具体流程参见下方
        """
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            """
            1.检查session中username是否存在，如果存在表示已登陆，否则进入【2】
                2.检查token是否存在，存在进入【3】，否则进入【4】
                    3.token存在：验证token并获取用户信息，username写入session，返回response
                    4.token不存在：验证登录
                        5.通过ticket获取s_token 进入步骤【3】
                    6.验证不通过跳转到验证失败页面
            :param args:
            :param kwargs:
            :return:
            """
            flag = False
            # 1.检查session中username是否存在，如果存在表示登陆，否则进入【2】
            username = flask.session.get('username')
            if username:
                return f(*args, **kwargs)
            else:
                # 2.session中username不存在，检查token是否存在，存在则进入【3】，否则进入【4】
                token = flask.request.cookies.get('APP_TOKEN', '')
                print(flask.request.path)
                if not token:
                    # 4.token不存在：跳转登录界面
                    return self._sso()
                else:
                    # 3.token存在：验证token并获取用户信息，username写入session，返回response
                    user = self._validate_session(token)
                    if not user:
                        return self.validate_error_callback()
                    flask.session['username'] = user['username']
                    resp = f(*args, **kwargs)

                    if flag:
                        resp.set_cookie('APP_TOKEN', token, 60*10) # Token过期时间10分钟
                    return resp

        return decorated