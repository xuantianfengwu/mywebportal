#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aip import AipSpeech
import configparser
import os
import librosa
import soundfile as sf
import numpy as np

class AudioUtils(object):
    def __init__(self):
        pass

    def get_audio_duration(self, audio_path, audio_type='mp3'):
        """ 获取音频时长 """
        duration = librosa.get_duration(filename=audio_path)
        return duration

    def generate_audio_from_text(self, text, output_file_path, source='baidu', param_dict=None):
        """ 从文本生成音频 """
        if source == 'baidu':
            cf = configparser.ConfigParser()
            cf.read(os.path.join('.', 'backend', 'config', '3rd_party_tool.ini'))
            app_id = cf.get('baidu-audio', 'app_id')
            api_key = cf.get('baidu-audio', 'api_key')
            secret_key = cf.get('baidu-audio', 'secret_key')
            # 实例化AipSpeech
            client = AipSpeech(app_id, api_key, secret_key)
            # 获取结果MP3
            result = client.synthesis(text, 'zh', 1, param_dict)
            # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
            if not isinstance(result, dict):
                # 保存结果mp3
                with open(output_file_path, 'wb') as f:
                    f.write(result)
            return True

    def combine_audio_files(self, input_dir, audio_files, output_dir, output_file, output_type='PCM_24'):
        """ 按顺序合并多个音频文件 """
        audio_paths = [os.path.join(input_dir, f) for f in audio_files]
        ys = []
        for audio_path in audio_paths:
            #print(audio_path)
            # 1.加载音频文件
            y, sr = librosa.load(audio_path)
            dur = librosa.get_duration(y, sr=sr)
            #print('数据x类型和采样率sr类型', type(y), type(sr))
            #print('数据x尺寸和采样率', y.shape, sr)
            #print('该音频的时长为：', dur)
            ys.append(y)
        audio_dst = np.hstack(ys)
        output_path = os.path.join(output_dir, output_file)
        sf.write(output_path, audio_dst, sr, subtype=output_type)
        return True

if __name__ == '__main__':
    # 1. generate_audio_from_text
    text = '不一会儿，女生传了另一张纸条，男生心急火燎的打开一看“拜托你不要告诉老师，我保证以后再也不嗑瓜子了”'
    output_file_path = '1.mp3'
    param_dict = {
        'vol': 5,
        'per': 5003
    }
    AudioUtils().generate_audio_from_text(text, output_file_path, param_dict=param_dict)

    # 2. get_audio_duration
    duration = AudioUtils().get_audio_duration('./1.mp3')
    print(duration)
