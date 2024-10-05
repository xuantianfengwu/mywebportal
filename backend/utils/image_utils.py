#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

class ImageUtils(object):
    def __init__(self):
        self.ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. ")

    def image2txtimage(self, image_dir, image_name):
        """ 将图片转换为字符图片 """
        # 缓存机制
        image_path = os.path.join(image_dir, image_name)
        txt_image_name = '_txt.'.join(image_name.split('.'))
        txt_image_path = os.path.join(image_dir, txt_image_name)
        if not os.path.exists(txt_image_path):
            # 读取原图片
            im = Image.open(image_path).convert('RGB')
            # gif拆分后的图像，需要转换，否则报错，由于gif分割后保存的是索引颜色
            raw_width = im.width
            raw_height = im.height
            width = int(raw_width / 6)
            height = int(raw_height / 15)
            im = im.resize((width, height), Image.NEAREST)
            # 解析原图片每个像素的颜色和文字
            txt = ""
            colors = []
            for i in range(height):
                for j in range(width):
                    pixel = im.getpixel((j, i))
                    colors.append((pixel[0], pixel[1], pixel[2]))
                    if len(pixel) == 4:
                        txt += self.get_char(pixel[0], pixel[1], pixel[2], pixel[3])
                    else:
                        txt += self.get_char(pixel[0], pixel[1], pixel[2])
                txt += '\n'
                colors.append((255, 255, 255))

            im_txt = Image.new("RGB", (raw_width, raw_height), (255, 255, 255))
            dr = ImageDraw.Draw(im_txt)
            # font = ImageFont.truetype(os.path.join("fonts","汉仪楷体简.ttf"),18)
            font = ImageFont.load_default()
            x = y = 0
            # 获取字体的宽高
            font_w, font_h = font.getsize(txt[1])
            font_h *= 1.37  # 调整后更佳
            # ImageDraw为每个ascii码进行上色
            for i in range(len(txt)):
                if txt[i] == '\n':
                    x += font_h
                    y = -font_w
                dr.text((y, x), txt[i], font=font, fill=colors[i])
                y += font_w
            # 保存新图片
            im_txt.save(txt_image_path)
        return txt_image_name

    def image2cartooniseimage(self, image_dir, image_name, mode='rgb'):
        assert mode in ['rgb', 'hsv']
        image_path = os.path.join(image_dir, image_name)
        cartoon_image_name = '_cartoon.'.join(image_name.split('.'))
        cartoon_image_path = os.path.join(image_dir, cartoon_image_name)
        """ 缓存机制 """
        if not os.path.exists(cartoon_image_path):
            image = cv2.imread(image_path)
            if mode == 'rgb':
                # Step1: 利用双边滤波器对原图像进行保边去噪处理
                # --下采样
                image_bilateral = image
                for _ in range(2):
                    image_bilateral = cv2.pyrDown(image_bilateral)
                # --进行多次的双边滤波
                for _ in range(7):
                    image_bilateral = cv2.bilateralFilter(image_bilateral, d=9, sigmaColor=9, sigmaSpace=7)
                # --上采样
                for _ in range(2):
                    image_bilateral = cv2.pyrUp(image_bilateral)
                # Step2: 将步骤一中获得的图像灰度化后，使用中值滤波器去噪
                image_gray = cv2.cvtColor(image_bilateral, cv2.COLOR_RGB2GRAY)
                image_median = cv2.medianBlur(image_gray, 7)
                # Step3: 对步骤二中获得的图像使用自适应阈值从而获得原图像的轮廓
                image_edge = cv2.adaptiveThreshold(image_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                                   blockSize=9, C=2)
                image_edge = cv2.cvtColor(image_edge, cv2.COLOR_GRAY2RGB)
                # Step4: 将步骤一中获得的图像与步骤三中获得的图像轮廓合并即可实现将照片变为卡通图片的效果了
                image_cartoon = cv2.bitwise_and(image_bilateral, image_edge)
            elif mode == 'hsv':
                # Step1: 图像BGR空间转HSV空间, 在HSV空间进行直方图均衡化, 中值滤波和形态学变换
                image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(image_hsv)
                # --直方图均衡化
                v = cv2.equalizeHist(v)
                image_hsv = cv2.merge((h, s, v))
                # --中值滤波
                image_hsv = cv2.medianBlur(image_hsv, 7)
                # --形态学变换-开/闭运算
                kernel = np.ones((5, 5), np.uint8)
                image_hsv = cv2.morphologyEx(image_hsv, cv2.MORPH_CLOSE, kernel, iterations=2)
                # --中值滤波
                image_hsv = cv2.medianBlur(image_hsv, 7)
                # Step2: 对步骤一中获得的图像使用自适应阈值从而获得原图像的轮廓
                image_mask = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
                image_mask = cv2.cvtColor(image_mask, cv2.COLOR_RGB2GRAY)
                image_mask = cv2.medianBlur(image_mask, 7)
                image_edge = cv2.adaptiveThreshold(image_mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                                   blockSize=9, C=2)
                image_edge = cv2.cvtColor(image_edge, cv2.COLOR_GRAY2RGB)
                # Step3: 将步骤二中获得的图像轮廓与原图像合并即可实现将照片变为卡通图片的效果了
                image_cartoon = cv2.bitwise_and(image, image_edge)
            cv2.imwrite(cartoon_image_path, image_cartoon)
        return cartoon_image_name

    def get_char(self, r, g, b, alpha=256):
        """ 根据alpha和rgb匹配一个文字出来 """
        if alpha == 0:
            return ''
        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray / unit)]
