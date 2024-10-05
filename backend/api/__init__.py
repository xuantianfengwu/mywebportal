#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .user import user_bp
from .upload import upload_bp
from .pdf import pdf_bp
from .login import login_bp
from .video import video_bp
from .todos import todos_bp
from .picture import picture_bp
from .trading import trading_bp
from .miniprogram import minip_bp

def bind_blueprint(app):
    print('Start binding Blueprint...')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(pdf_bp, url_prefix='/api/pdf')
    app.register_blueprint(login_bp, url_prefix='/api/login')
    app.register_blueprint(video_bp, url_prefix='/api/video')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
    app.register_blueprint(picture_bp, url_prefix='/api/picture')
    app.register_blueprint(trading_bp, url_prefix='/api/trading')
    app.register_blueprint(minip_bp, url_prefix='/api/minip')
