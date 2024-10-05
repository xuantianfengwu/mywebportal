#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 获取必要的爬虫信息 """

import requests
from bs4 import BeautifulSoup
import os

class Crawler(object):
    def __init__(self):
        pass

    def crawl_choaqingmv_resource(self, url=None, video_id=None, output_dir=None, output_name=None):
        """ 爬取 超清MV 网站的资源
            http://www.chaoqingmv.com/
        """
        if not url and not video_id:
            print('请输入url或video_id')
            return

        if not output_name:
            output_name = '{}.mp4'.format(video_id)
        if not output_dir:
            output_dir = '.'
        output_path = os.path.join(output_dir, output_name)

        """ 获取 下载ts文件 的url_base """
        url_a = "http://www.chaoqingmv.com/video/{}.html".format(video_id)
        resp_a = requests.get(url_a)
        bs = BeautifulSoup(resp_a.content)
        img_src = bs.select_one('div.mv_img > img').get('src')
        ts_down_url_base = img_src.replace('.jpg', '/')
        print('已获取到ts文件下载地址: {}'.format(ts_down_url_base))

        """ 获取video涉及的全部ts文件名称 """
        url_b = 'http://www.chaoqingmv.com/skin/zuiaidj/player/play.php?id={}&type=video'.format(video_id)
        resp = requests.get(url_b)
        resp_json = resp.json()
        # 解析得到php文件中的 m3u8_url """
        m3u8_url = resp_json['url']
        # 访问 m3u8_url 获取 m3u8 文件内容 """
        m3u8_cont = requests.get(m3u8_url).text
        # m3u8中获取全部ts文件名称 """
        ts_files = [line for line in m3u8_cont.split('\n') if line[-3:]=='.ts' ]
        print('已获取到全部ts文件列表: 共{}个'.format(len(ts_files)))

        """ 顺序下载全部ts文件 """
        print('开始下载~')
        with open(output_path, 'wb') as f:
            for ts_f in ts_files:
                ts_down_url = ts_down_url_base + ts_f
                resp = requests.get(ts_down_url)
                f.write(resp.content)
        print('文件下载完成：{}'.format(output_path))
        return True

if __name__ == '__main__':
    crawler = Crawler()

    """ 下载超清MV上的视频： http://www.chaoqingmv.com/video """
    crawler.crawl_choaqingmv_resource(video_id=3018)
