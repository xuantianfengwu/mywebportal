#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import requests
import os
import configparser

class PictureTools(object):
    def __init__(self):
        """ 初始化 """
        self.picture_letter_rec_tool = None

    @staticmethod
    def picture_letter_rec(file_path, model_type):
        """ 文字ORC识别 """
        with open(file_path, 'rb') as f:
            img = base64.b64encode(f.read())
            if model_type == 'baidu':
                request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
                params = {"image": img}
                access_token = PictureTools.get_baidu_access_token()
                request_url = request_url + "?access_token=" + access_token
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                response = requests.post(request_url, data=params, headers=headers)
                if response:
                    json_result = response.json()
                    words_result = json_result['words_result']
                    res_text = '\n'.join([word_l['words'] for word_l in words_result])
                    return res_text
                else:
                    return ''

    @staticmethod
    def get_baidu_access_token():
        """ 根据配置文件获取BAIDU ORC的APP_KEY和SECRET_KEY，进而获取access_token，用于调起相关服务 """
        cf = configparser.ConfigParser()
        cf.read(os.path.join('.', 'backend', 'config', '3rd_party_tool.ini'))
        app_key = cf.get('baidu_ORC', 'BAIDU_APP_KEY')
        secret_key = cf.get('baidu_ORC', 'BAIDU_SECRET_KEY')
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(app_key, secret_key)
        response = requests.get(host)
        if response:
            print(response.json())
            return response.json()['access_token']