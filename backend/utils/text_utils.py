#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
from jieba import analyse

import requests
from bs4 import BeautifulSoup

from hashlib import md5
import random
import time
import configparser
import os



class TextUtils(object):
    def __init__(self):
        pass

    def sep_sentences(self, text, max_length=50):
        """ 将中文Text分割成句子 """
        sentences = [l.strip() for l in text.split('\n') if len(l.strip()) > 0]
        final_sentences = []
        for s in sentences:
            if len(s) <= max_length:
                final_sentences.append(s)
            else:
                while len(s) > max_length:
                    trunc_s, s = self.truncate_sentence(s, truncate_length=max_length)
                    final_sentences.append(s)
                final_sentences.append(s)
        return final_sentences

    def truncate_sentence(self, sentence, truncate_length=50, stopwords=['"', '。', '“']):
        """ 根据truncate_length截断sentence，并返回未截断部分的sentence """
        stopwords_idxes = [i for i in range(len(sentence[:truncate_length])) if sentence[i] in stopwords]
        if len(stopwords_idxes)>0:
            stopwords_idx = stopwords_idxes[-1]
            truncated_sentences = [sentence[:stopwords_idx], sentence[stopwords_idx:]]
        else:
            truncated_sentences = [sentence[:truncate_length], sentence[truncate_length:]]
        return truncated_sentences

    def get_sentence_center_words(self, sentence, center_word_amt=1, model='jieba'):
        """ 获取sentence的中心词 """
        center_words = jieba.analyse.extract_tags(sentence,
                                                  topK=center_word_amt,
                                                  withWeight=True,
                                                  allowPOS=())
        return center_words

    def translate_text(self, text, from_lang, to_lang, appid, appkey):
        """ 百度api-通用翻译 """
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path
        salt = random.randint(32768, 65536)
        sign = TextUtils.make_md5(appid + text + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': text, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        time.sleep(1)
        return result

    @staticmethod
    def make_md5(s, encoding='utf-8'):
        """ md5加密 """
        return md5(s.encode(encoding)).hexdigest()

    def get_word_picture_srcs(self, word, pic_amt=1, src='colorhub'):
        """ 根据word获取配图 """
        if src == 'colorhub':
            keywords = word.split(' ')
            url = 'https://www.colorhub.me/search?tag={}'.format('+'.join(keywords))
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
            content = soup.find_all('img', limit=pic_amt)
            srcs = ['http:{}'.format(c.get('src').strip()) for c in content]
            return srcs
        else:
            return None


if __name__ == '__main__':
    # 1. sep_sentences
    txt = """
        一个男生暗恋一个女生很久了。
        一天自习课上，男生偷偷的传了小纸条给女生，上面写着“其实我注意你很久了”。
        不一会儿，女生传了另一张纸条，男生心急火燎的打开一看“拜托你不要告诉老师，我保证以后再也不嗑瓜子了”
        男生一脸懵逼。
    """
    sentences = TextUtils().sep_sentences(txt)
    print(sentences)

    # 2. get_sentence_center_words
    center_words = [TextUtils().get_sentence_center_words(s) for s in sentences]
    print(center_words)

    # 3. translate_text
    cf = configparser.ConfigParser()
    cf.read(os.path.join('.', 'backend', 'config', '3rd_party_tool.ini'))
    appid = cf.get('baidu-translate', 'appid')
    appkey = cf.get('baidu-translate', 'appkey')
    trans_result = TextUtils().translate_text('测试', 'zh', 'en', appid, appkey)
    print(trans_result)

    # 4. get_word_picture_srcs
    srcs = TextUtils().get_word_picture_srcs('Secret Love')
    print(srcs)
