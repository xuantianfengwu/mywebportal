#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from backend.utils.web_response import WebResponse
from backend.utils.osfile_utils import OSFileUtils
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/pdf/transformer', methods=['POST'])
def pdf_transformer_upload_file():
    """ PDF Transformer 中上传文件 """
    file = request.files.get('file')
    to_dir = os.path.join('.', 'backend', 'static', 'upload', 'pdf_tools')
    filename = file.filename
    to_path = os.path.join(to_dir, filename)
    OSFileUtils(to_path).save_file(file)
    return ''

@upload_bp.route('/picturetools/picture', methods=['POST'])
def picture_tools_upload_file():
    """ Picture Tools 中上传文件 """
    to_dir = os.path.join('.', 'backend', 'static', 'upload', 'picture_tools')
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    # 1.获取上传文件，2.获取Headers里的from信息，并构造文件名
    file = request.files.get('file')
    headers = request.headers
    filename = '{}_{}'.format(headers['FROM'], file.filename)
    # 保存文件到对应路径
    file.save(os.path.join(to_dir, filename))
    return WebResponse.success('文件上传成功！')
