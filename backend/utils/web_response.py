#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    用来给前端返回请求的通用类
"""


class WebResponse(object):
    """
        用来给前端返回请求的通用类
        .success : 成功的请求
        .error   : 服务端内部错误失败的请求
        .fail    : 用户侧原因失败的请求
    """
    SUCCESS_CODE = 200
    ERROR_CODE = 300
    FAIL_CODE = 400

    @staticmethod
    def success(message, data=None):
        """
            成功的请求
        """
        resp_dict = {
            'code': WebResponse.SUCCESS_CODE,
            'message': message,
            'data': data
        }
        return resp_dict

    @staticmethod
    def error(message, data=None):
        """
            服务端内部错误失败的请求
        """
        resp_dict = {
            'code': WebResponse.ERROR_CODE,
            'message': message,
            'data': data
        }
        return resp_dict

    @staticmethod
    def fail(message, data=None):
        """
            用户侧原因失败的请求
        """
        resp_dict = {
            'code': WebResponse.FAIL_CODE,
            'message': message,
            'data': data
        }
        return resp_dict
