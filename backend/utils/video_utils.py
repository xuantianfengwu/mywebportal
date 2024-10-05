#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import cv2
import subprocess
# from cv2 import VideoCapture, imwrite, VideoWriter_fourcc, VideoWriter, imread
from PIL import Image, ImageFont, ImageDraw
import configparser
from moviepy.editor import (VideoFileClip, TextClip, CompositeVideoClip)
from .image_utils import ImageUtils
from moviepy.editor import *

class VideoUtils(object):
    def __init__(self):
        self.FPS = None
        self.ffmpeg_path = None
        self.image_util = None

    def _init_ffmpeg_path(self):
        """ 初始化加载ffmpeg的驱动路径 """
        if not self.ffmpeg_path:
            cf = configparser.ConfigParser()
            cf.read(os.path.join('.', 'backend', 'config', '3rd_party_tool.ini'))
            self.ffmpeg_path = cf.get('ffmpeg', 'path')

    def _init_image_util(self):
        if not self.image_util:
            self.image_util = ImageUtils()

    def video2txtvideo(self, input_dir, input_file, output_dir, output_file, is_cached=True):
        """ 将视频转为文字视频 """
        print('Start Video 2 TxtVideo...')
        try:
            print('Create Cache Dir...')
            cache_dir = os.path.join(input_dir, 'Cache')
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
            # Video转图片&txt图片
            print('Video 2 Images...')
            img_names = self.video2images(input_dir, input_file, cache_dir, is_with_txt=True)
            # txt图片合成视频
            print('Images 2 Video...')
            self.images2video(cache_dir, img_names, cache_dir, 'cached.avi', self.FPS)
            # Video提取音频
            print('Video 2 MP3...')
            self.video2mp3(input_dir, input_file, cache_dir, 'cached.mp3')
            # 视频+音频 合成
            print('Combine Video & MP3...')
            self.video_add_mp3(cache_dir, 'cached.avi', 'cached.mp3', output_dir, output_file)
            print('Finish Video 2 TxtVideo...')
            shutil.rmtree(cache_dir)
        finally:
            # 如果不缓存，强制删除Cache文件夹
            if not is_cached:
                shutil.rmtree(cache_dir)

    def video2cartoonvideo(self, input_dir, input_file, output_dir, output_file, is_cached=True):
        """ base原视频，生成新的风格化视频 """
        print(f'Start Stylize the Video: {input_file}')
        self._init_image_util()
        try:
            print('Create Cache Dir...')
            cache_dir = os.path.join(input_dir, 'Cache')
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)

            """ Step1：视频转图片 """
            print('1. Video 2 Images...')
            img_names = self.video2images(input_dir, input_file, cache_dir)

            """ Step2: 图片卡通化 """
            print('2. Stylish Images...')
            new_img_names = []
            for img_name in img_names:
                new_img_name = self.image_util.image2cartooniseimage(cache_dir, img_name)
                print(new_img_name)
                new_img_names.append(new_img_name)

            """ Step3: 卡通化图片生成视频 """
            print('3. Images 2 Video...')
            self.images2video(input_dir=cache_dir, input_files=new_img_names,
                              output_dir=cache_dir, output_file='cached.avi',
                              fps=self.FPS)

            """ Step4：视频提取音频 """
            print('4. Video 2 MP3...')
            self.video2mp3(input_dir, input_file, cache_dir, 'cached.mp3')

            """ Step5: 卡通化视频与音频合并 """
            print('5. Combine Video & MP3...')
            self.video_add_mp3(cache_dir, 'cached.avi', 'cached.mp3', output_dir, output_file)

            print('Finish Video Stylization!')
            shutil.rmtree(cache_dir)
        finally:
            # 如果不缓存，强制删除Cache文件夹
            if not is_cached:
                shutil.rmtree(cache_dir)

    def video2images(self, input_dir, input_file, output_dir, is_with_txt=False):
        """ 将视频拆分成为图片 """
        input_path = os.path.join(input_dir, input_file)
        vc = cv2.VideoCapture(input_path)
        self.FPS = vc.get(cv2.CAP_PROP_FPS)  # 获取帧率
        print('Video FPS:', cv2.CAP_PROP_FPS)
        # 处理
        c = 1
        pic_names = []
        if vc.isOpened():
            r, frame = vc.read()
        else:
            r = False
        while r:
            pic_name = '{}_{}.jpg'.format(os.path.basename(input_file).split('.')[0], c)
            output_path = os.path.join(output_dir, pic_name)
            # 缓存机制
            if not os.path.exists(output_path):
                # cv2.imwrite(output_path, frame) # 路径有中文会乱码
                cv2.imencode('.jpg', frame)[1].tofile(output_path)
            # 如果is_with_txt=True，再生成一张txt格式的image
            if is_with_txt:
                self._init_image_util()
                pic_name = self.image_util.image2txtimage(output_dir, pic_name)  # 同时转换为ascii图
            print('Pic {} Finished!'.format(pic_name))
            c += 1
            pic_names.append(pic_name)
            r, frame = vc.read()
        vc.release()
        return pic_names

    def images2video(self, input_dir, input_files, output_dir, output_file, fps,
                           input_durations=[],
                           need_size=None):
        """ 将图片合成视频 """
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        image_paths = [os.path.join(input_dir, file) for file in input_files]
        if need_size:
            vw = cv2.VideoWriter(os.path.join(output_dir, output_file), fourcc, fps, need_size)
        else:
            size = Image.open(image_paths[0]).size
            vw = cv2.VideoWriter( os.path.join(output_dir, output_file), fourcc, fps, size)
        for i, image_path in enumerate(image_paths):
            # 如果有input_durations，则每张图片根据fps重复对应次数以达到对应duration
            if input_durations:
                freq = int(input_durations[i]*fps) + 1
            else:
                freq = 1
            # 读取图片
            frame = cv2.imread(image_path)
            # resize if necessary
            if need_size:
                frame = cv2.resize(frame, need_size)
            # write vw
            for i in range(freq):
                vw.write(frame)
        vw.release()
        return True

    def video2mp3(self, input_dir, input_file, output_dir, output_file):
        """ 调用ffmpeg获取mp3音频文件 """
        self._init_ffmpeg_path()
        inputfile_name = os.path.join(input_dir, input_file)
        outfile_name = os.path.join(output_dir, output_file)
        shell_script = '{} -i {} -f mp3 {}'.format(self.ffmpeg_path, inputfile_name, outfile_name)
        print(shell_script)
        subprocess.call(shell_script, shell=True)

    def video_add_mp3(self, input_dir, video_name, mp3_file, output_dir, output_file):
        """ 合成音频和视频文件 """
        self._init_ffmpeg_path()
        video_path = os.path.join(input_dir, video_name)
        mp3_path = os.path.join(input_dir, mp3_file)
        outfile_name = os.path.join(output_dir, output_file)
        shell_script = '{} -i {} -i {} -strict -2 -f mp4 {}'.format(self.ffmpeg_path, video_path, mp3_path, outfile_name)
        print(shell_script)
        subprocess.call(shell_script, shell=True)

    def video_add_subtitles(self, input_dir, video_name, output_dir, output_file,
                                  sentences, start_times, durations):
        """ 给视频添加字幕 """
        # 读取Video
        src_video = os.path.join(input_dir, video_name)
        video = VideoFileClip(src_video)
        w, h = video.w, video.h
        # 生成字幕
        txts = []
        for s, start, d in zip(sentences, start_times, durations):
            txt = TextClip(s, fontsize=40, font='SimHei', size=(w-20, 40), align='center', color='DarkOrange')\
                .set_position((10, h-150))\
                .set_duration(d)\
                .set_start(start)
            txts.append(txt)
        # 合并生成新视频
        video = CompositeVideoClip([video, *txts])
        #fn, ext = os.path.splitext(src_video)
        output_path = os.path.join(output_dir, output_file)
        video.write_videofile(output_path)
        return True

    def video_add_video(self, input_dir, video1_name, video2_name, pct,
                              output_dir, output_name):
        """ 在 video1 中加入 video2，
                video2 按 video1.size * pct 的大小缩放
            用于实现画中画等功能
        """
        video1_path = os.path.join(input_dir, video1_name)
        video2_path = os.path.join(input_dir, video2_name)
        output_path = os.path.join(output_dir, output_name)
        """ 读取两个视频 """
        clip1 = VideoFileClip(video1_path)
        clip2 = VideoFileClip(video2_path)
        """ 设定clip2的大小和位置 """
        clip2_resize = (int(pct * clip1.size[0]), int(pct * clip1.size[1]))
        clip2 = clip2.resize(clip2_resize)
        clip2 = clip2.set_position( (clip1.size[0] - clip2_resize[0], 0) )
        """ 出片~ """
        CompositeVideoClip([clip1, clip2]).write_videofile(output_path)

if __name__ == '__main__':
    video_utils = VideoUtils()

    # 1. video2txtvideo
    input_dir = os.path.join('C:' + os.sep, 'Users', 'xuezhihuan', 'MyCodes', 'static')
    input_file = 'test.mp4'
    output_dir = os.path.join('C:' + os.sep, 'Users', 'xuezhihuan', 'MyCodes', 'static')
    output_file = 'test-txt.mp4'
    video_utils.video2txtvideo(input_dir, input_file, output_dir, output_file, is_cached=True)

    """ 2. video2cartoonvideo """
    input_dir = os.path.join('C:', 'Users', 'xuezhihuan', 'Downloads')
    input_videoname = 'huoyuanjia.mp4'
    output_videoname = 'new_{}'.format(input_videoname)
    video_utils.video2cartoonvideo(input_dir=input_dir, input_file=input_videoname,
                                   output_dir=input_dir, output_file=output_videoname,
                                   is_cached=True)
