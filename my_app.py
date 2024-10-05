#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
from flask import Flask, render_template, Response
import os
import logging

from backend.utils.web_response import WebResponse

def init_app():
    app = Flask(__name__, template_folder='./frontend/build', static_folder='./frontend/build/static')
    app.config['SECRET_KEY']=os.urandom(24)

    from flask_cors import CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    from backend.utils import Auth
    auth_dealer = Auth.SSO()

    # 绑定api路由，全部不走鉴权跳转
    from backend.api import bind_blueprint
    bind_blueprint(app)

    # 登录页面不走鉴权
    @app.route('/login')
    def login():
        """
            login页面无需鉴权，直接访问
            其他页面要走 @auth_dealer.login_required 逻辑
        """
        return Response(render_template('index.html'))

    # 其他页面都走auth_dealer.login_required逻辑
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    @auth_dealer.login_required
    def index(path):
        return Response(render_template('index.html'))

    # 统一异常处理，返回WebResponse.error
    @app.errorhandler(Exception)
    def python_error_handler(error):
        """ 处理标准Python异常 """
        logging.getLogger().info(error)
        return WebResponse.error(str(error))
    return app

if __name__ == "__main__":
    app = init_app()
    #app.run('0.0.0.0', port=9000, debug=True)
    app.run('0.0.0.0', port=80)