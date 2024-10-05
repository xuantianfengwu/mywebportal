#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request
import flask

pdf_bp = Blueprint('pdf', __name__)

from ..service.pdf_transformer import PDFTransformer
from ..utils.web_response import WebResponse

@pdf_bp.route('/transformer/delpage', methods=['POST'])
def pdf_transformer_del_specific_pages():
    """
        从原PDF生成新的PDF，具体操作类型看oper_type参数
    """
    # 解析参数
    oper_type = request.form['operate_type']     # str: 1
    oper_params = eval(request.form['operate_params']) # dict: {to_del_pages: ''}
    upload_files = eval(request.form['upload_files'])  # list:
    upload_files = [f['name'] for f in upload_files]
    # 执行operate_type
    res = PDFTransformer(upload_files).operate(oper_type, oper_params)
    # 返回结果
    data = {'operate_res': res}
    return WebResponse.success('文件处理成功！', data=data)

@pdf_bp.route('/transformer/res/preview')
def preview_pdf_transformer_res_file():
    # 解析参数
    oper_type = request.args['oper_type']  # str: 1
    preview_file = request.args['prev_file']  # str:
    # 执行
    res = PDFTransformer(preview_file).get_result_file_path(oper_type)
    # 返回
    return flask.send_from_directory(res['res_file_dir'], res['res_file_name'])
    #return flask.send_from_directory(res['res_file_dir'], res['res_file_name'], as_attachment=False)

@pdf_bp.route('/transformer/res/download', methods=['POST'])
def download_pdf_transformer_res_files():
    # 解析参数
    oper_type = request.form['oper_type']  # str: 1
    download_type = request.form['download_type']
    download_files = eval(request.form['download_files'])  # list:
    # 执行
    res = PDFTransformer(download_files).get_result_files_path(oper_type, download_type)
    # 返回
    # data = {
    #     'download_f': flask.send_from_directory(res['res_file_dir'], res['res_file_name']),
    #     'download_f_type': res['res_file_type'],
    #     'download_f_name': res['res_file_name']
    # }
    # return WebResponse.success('压缩文件生成成功', data=data)
    return flask.send_from_directory(res['res_file_dir'], res['res_file_name'])
