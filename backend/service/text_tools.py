#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..utils.text_utils import TextUtils
from ..utils.audio_utils import AudioUtils
from ..utils.osfile_utils import OSFileUtils
from ..utils.video_utils import VideoUtils

import os
import configparser
import requests
import numpy as np

class TextTools(object):
    def __init__(self):
        self.crawl_dir = os.path.join('.', 'backend', 'static', 'crawl', 'text_tools')
        self.output_dir = os.path.join('.', 'backend', 'static', 'output', 'text_tools')
        self.__mkdirs()

    def __mkdirs(self):
        """ 创建静态文件文件夹 """
        OSFileUtils.mkdir(self.crawl_dir)
        OSFileUtils.mkdir(self.output_dir)

    def generate_video_from_text(self, text, video_name):
        """ 从文本生成视频 """
        video_dict = {
            'text': text,
            'sentences': [],
            'keywords': [],
            'en_keywords': [],
            'pic_files': [],
            'mp3_files': [],
            'mp3_durations': []
        }
        textutils, audioutils, videoutils = TextUtils(), AudioUtils(), VideoUtils()

        # 1. sep_sentences
        print('1 ====> Start Sep_Sentences...')
        sentences = textutils.sep_sentences(text)
        video_dict['sentences'] = sentences

        # 2. get keywords
        print('2 ====> Start Get Keywords...')
        cf = configparser.ConfigParser()
        cf.read(os.path.join('.', 'backend', 'config', '3rd_party_tool.ini'))
        appid = cf.get('baidu-translate', 'appid')
        appkey = cf.get('baidu-translate', 'appkey')

        center_words = [textutils.get_sentence_center_words(s)[0][0] for s in sentences]
        en_center_words = [textutils.translate_text(w, 'zh', 'en', appid, appkey)['trans_result'][0]['dst'] for w in center_words]

        video_dict['keywords'] = center_words
        video_dict['en_keywords'] = en_center_words

        # 3. download_pictures
        print('3 ====> Start Download Pictures...')
        for i, keyword, en_keyword in zip(range(len(center_words)), center_words, en_center_words):
            pic_name = '{}_{}.jpg'.format(i, en_keyword)
            pic_path = os.path.join(self.crawl_dir, pic_name)
            print('{}_{}_{}.jpg'.format(i, keyword, en_keyword))
            video_dict['pic_files'].append(pic_name)
            # 已有图片不重复下载
            if not os.path.exists(pic_path):
                srcs = textutils.get_word_picture_srcs(keyword, src='colorhub')
                if not srcs:
                    srcs = textutils.get_word_picture_srcs(en_keyword, src='colorhub')
                # 兜底srcs
                if not srcs:
                    srcs = textutils.get_word_picture_srcs('大笑', src='colorhub')
                src = srcs[0]
                resp = requests.get(src)
                with open(pic_path, 'wb') as f:
                    f.write(resp.content)

        # 4. Generate Audio From Text
        # 度小宇=1，度小美=0，度逍遥（基础）=3，度丫丫=4
        # 度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
        print('4 ====> Start Generate Audio From Text...')
        param_dict = {
            'vol': 5,
            'per': 5003
        }
        for i, keyword, en_keyword, sentence in zip(range(len(center_words)),
                                                    center_words, en_center_words, sentences):
            mp3_file_name = '{}_{}.mp3'.format(i, en_keyword)
            mp3_file_path = os.path.join(self.crawl_dir, mp3_file_name)
            print('{}_{}_{}.jpg'.format(i, keyword, en_keyword))
            # 已有mp3不重复生成
            if not os.path.exists(mp3_file_path):
                audioutils.generate_audio_from_text(sentence, mp3_file_path, param_dict=param_dict)
            duration = audioutils.get_audio_duration(mp3_file_path)
            video_dict['mp3_files'].append(mp3_file_name)
            video_dict['mp3_durations'].append(duration)

        # 5. Images->Videos & Mp3s->Mp3(base on the duration of mp3s)
        print('5 ====> Start Images2Video...')
        videoutils.images2video(self.crawl_dir, video_dict['pic_files'],
                                self.crawl_dir, 'video.avi', 5,
                                input_durations=video_dict['mp3_durations'],
                                need_size=(1920, 1080))
        audioutils.combine_audio_files(self.crawl_dir, video_dict['mp3_files'],
                                       self.crawl_dir, 'video.wav')

        # 6. combine_mp3 & pictures
        print('6 ====> Start Combine Video & Audio...')
        videoutils.video_add_mp3(self.crawl_dir, 'video.avi', 'video.wav',
                                 self.output_dir, video_name)

        # 7. Add Subtitles
        print('7 ====> Start Add SubTitles...')
        mp3_durations = video_dict['mp3_durations']
        start_times = [np.sum(mp3_durations[:i]) for i in range(len(mp3_durations))]
        videoutils.video_add_subtitles(self.output_dir, video_name,
                                       self.output_dir, '(subtitled)'+video_name,
                                       video_dict['sentences'], start_times, mp3_durations)
        print('Finished!')
        return True

if __name__ == '__main__':
    text = """
        地理老师问：河水往哪里流啊？
        一学生猛站起来唱到：大河向东流啊！
        老师没理会他接着说：天上有多少颗星星啊？
        那学生又唱到：天上的星星参北斗啊！
        老师气急：你给我滚出去！
        学生：说走咱就走啊！
        老师无奈：你有病吧？
        学生：你有我有全都有啊！
        老师：你再唱一句试试！
        学生：路见不平一声吼啊！
        老师：你信不信我揍你？
        学生：该出手时就出手啊！
        老师怒：我让你退学！
        学生：风风火火闯九州啊。
    """
    video_name = '1.mp4'
    TextTools().generate_video_from_text(text, video_name)