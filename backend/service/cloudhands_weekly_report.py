#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd
import numpy as np
import json
import time

import requests
from bs4 import BeautifulSoup

from docxtpl import DocxTemplate, InlineImage
from opencc import OpenCC  # Traditional Chinese Transform
converter_s2t = OpenCC('s2t')  # 简体转繁体
converter_t2s = OpenCC('t2s')  # 繁体转简体
# for height and width you have to use millimeters (Mm), inches or points(Pt) class :
from docx.shared import Pt
from PIL import Image

# 设置中文字体，添加多平台支持
import matplotlib.pyplot as plt
import platform
sys = platform.system()
if sys.lower() == 'windows':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
elif sys.lower() == 'darwin':  # macOS
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti TC']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei']

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from ..utils.osfile_utils import OSFileUtils
from ..utils.docx_utils import DocxUtils

# 用于Selenium爬取的导入
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class CloudhandsWeeklyReport(object):
    def __init__(self, week_start):
        """
            1.初始化爬取文件地址
            2.初始化周报产出地址
            3.初始化相关url
            4.初始化相关爬取文件名称
        """
        self.week_start = week_start
        self.output_file_dir = os.path.join('.', 'backend', 'static', 'output', 'cloudhands_weely_report', week_start)
        self.crawl_file_dir = os.path.join('.', 'backend', 'static', 'crawl', 'cloudhands_weely_report', week_start)
        self.meta_data_dir = os.path.join('.', 'sqlite')
        self.__mkdirs()
        # 1.爬取FundamentalEventSummary【周报标题&基本面摘要】的Url
        self.fx678_url = 'https://news.fx678.com/column/forex'
        self.fx678_headers = {
            'referer': 'https://www.fx678.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        self.fund_event_summary_file = 'fund_event_summary.csv'
        # 2.爬取ForexTrendSummary【外汇期货合约走势】的Url
        self.forex_trend_summary_file = 'forex_trend_summary.csv'
        self.forex_trend_summary_pic = 'forex_trend_summary.png'
        self.traditional_forex_trend_summary_pic = 'fanti_forex_trend_summary.png'
        # 3.爬取ForexPositionSummary【期货市场头寸分析】的Url
        self.display_curr_order = ['欧元', '澳元', '英镑', '日元', '加元', '纽元']
        self.cftc_net_position_file = 'cftc_net_position.csv'
        self.cftc_net_position_pic = 'cftc_net_position.png'
        self.traditional_cftc_net_position_pic = 'fanti_cftc_net_position.png'
        # 4.爬取MajorCurrencyForecast【重点货币对展望】的Url
        self.major_currency_forecast_file = 'major_curr_forecast.json'
        # 5.爬取FutureDataEvent【后市观察指标】的Url
        self.jin10_data_filter_file = 'jin10_financial_data_list.xlsx'
        self.forex_future_data_event_file = 'future_data_event.xlsx'
        self.future_data_event_data_types = {'DATA': 'DATA.png', 'EVENT': 'EVENT.png'}
        self.traditional_future_data_event_data_types = {'DATA': 'fanti_DATA.png', 'EVENT': 'fanti_EVENT.png'}
        # Output File的模板
        self.weekly_report_demo = 'Cloudhands Report Demo.docx'
        self.weekly_report_output = {
            'docx-jt': "（简体）CME版本 云核变量策略周报 {}.docx".format(self._week_report_period),
            'docx-ft': "（繁体）CME版本 云核变量策略周报 {}.docx".format(self._week_report_period),
            'pdf-jt': "（简体）CME版本 云核变量策略周报 {}.pdf".format(self._week_report_period),
            'pdf-ft': "（繁体）CME版本 云核变量策略周报 {}.pdf".format(self._week_report_period),
        }
        # genpy Path
        self.genpy_path = r'C:\Users\ASUS\AppData\Local\Temp\gen_py\3.7'
        # Proxy Port(代理端口)
        self.proxies = {
            'https': 'https://127.0.0.1:10809',  # 查找到你的vpn在本机使用的https代理端口
            'http': 'http://127.0.0.1:10809',  # 查找到vpn在本机使用的http代理端口
        }

    def __mkdirs(self):
        """ 创建静态文件文件夹 """
        OSFileUtils.mkdir(self.output_file_dir)
        OSFileUtils.mkdir(self.crawl_file_dir)

    @property
    def _week_report_period(self):
        week_start_dt = datetime.datetime.strptime(self.week_start, '%Y-%m-%d')
        week_end_dt = week_start_dt + datetime.timedelta(days=6)
        return '{} - {}'.format(week_start_dt.strftime('%Y.%m.%d'), week_end_dt.strftime('%Y.%m.%d'))

    @property
    def _forex_trend_dates(self):
        wstart_dt = datetime.datetime.strptime(self.week_start, '%Y-%m-%d')
        l_wend_dt = wstart_dt + datetime.timedelta(days=-1)
        l_wstart_dt = wstart_dt + datetime.timedelta(days=-7)
        l_mstart_dt = wstart_dt + datetime.timedelta(days=-1-31)
        return {
            'l_wstart_dt': l_wstart_dt.strftime('%Y-%m-%d'),
            'l_mstart_dt': l_mstart_dt.strftime('%Y-%m-%d'),
            'l_wend_dt': l_wend_dt.strftime('%Y-%m-%d'),
        }

    @staticmethod
    def df_to_traditional(df):
        traditional_df = df.applymap(lambda x: converter_s2t.convert(x) if isinstance(x, str) else x)
        traditional_df.columns = [converter_s2t.convert(col) for col in df.columns]
        return traditional_df

    @staticmethod
    def get_week_dates(week='next'):
        """ 获取下周或本周（周一到周日）的日期列表 """
        week_dates = []
        if week == 'this': # 本周
            now_dt = datetime.datetime.now() - datetime.timedelta(days=7)
        else: # 下周
            now_dt = datetime.datetime.now()
        now_wkd = now_dt.weekday()
        begin_d = now_dt + datetime.timedelta(days=7-now_wkd)
        last_d = now_dt + datetime.timedelta(days=13-now_wkd)
        while begin_d <= last_d:
            week_dates.append(str(begin_d)[:10].replace('-', ''))
            begin_d += datetime.timedelta(days=1)
        return week_dates

    def crawl_fundamental_event_summary(self):
        """ 爬取并保存基本面摘要数据 """
        # Step1: 在 FX678 获取外汇周报内容，若未能成功获取返回空字典
        weekly_report_dict = self.get_fx678_weekly_report()
        weekly_report_df = pd.DataFrame()
        weekly_report_df['Item'] = weekly_report_dict.keys()
        weekly_report_df['Content'] = weekly_report_dict.values()
        # Step2: 保存本地csv
        f_path = os.path.join(self.crawl_file_dir, self.fund_event_summary_file)
        weekly_report_df.to_csv(f_path, index=False, encoding='utf-8-sig')
        return True

    def crawl_forex_trend_summary(self):
        """ 爬取并保存外汇行情数据 """
        print('Start Crawl Forex Trend Summary Data...')
        forex_trend_date = self._forex_trend_dates
        m_start_date = forex_trend_date['l_mstart_dt']
        w_start_date = forex_trend_date['l_wstart_dt']
        end_date = forex_trend_date['l_wend_dt']
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if end_date>today_date:
            print('End date>today date, set it to today date.')
            end_date=today_date 
        try:
            # 1.Crawl from Trading View
            need_columns = ["name", "close", "change|1W", "change|1M"]
            filters1 = [{"left": "forex_priority", "operation": "nempty"},
                        {"left": "sector", "operation": "equal", "right": "Major"}
                        ]
            filters2 = [{"left": "forex_priority", "operation": "nempty"},
                        {"left": "country,country2", "operation": "equal", "right": "Asia"}
                        ]
            data_df1 = self.get_trading_view_trend_data_df(need_columns, filters1)
            data_df2 = self.get_trading_view_trend_data_df(need_columns, filters2)
            data_df = pd.concat([data_df1, data_df2[data_df2['name'] == 'USDCNY']])
            data_df.columns = ['TICKER',  'LAST', '1W CHG %', '1M CHG %']
        except:
            # 2.Crawl from api.exchangerate.host
            data_df = pd.concat([
                self.get_apilayer_fx_data_df('EUR', 'USD', m_start_date, end_date),
                self.get_apilayer_fx_data_df('USD', 'JPY', m_start_date, end_date),
                self.get_apilayer_fx_data_df('GBP', 'USD', m_start_date, end_date),
                self.get_apilayer_fx_data_df('AUD', 'USD', m_start_date, end_date),
                self.get_apilayer_fx_data_df('USD', 'CAD', m_start_date, end_date),
                self.get_apilayer_fx_data_df('USD', 'CHF', m_start_date, end_date),
                self.get_apilayer_fx_data_df('NZD', 'USD', m_start_date, end_date),
                self.get_apilayer_fx_data_df('USD', 'CNY', m_start_date, end_date),
            ], axis=0)
            data_df['TICKER'] = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD','USDCAD', 'USDCHF', 'NZDUSD', 'USDCNY']
            data_df['LAST'] = data_df[end_date]
            data_df['1W CHG %'] = 100 * (data_df[end_date] / data_df[w_start_date] - 1)
            data_df['1M CHG %'] = 100 * (data_df[end_date] / data_df[m_start_date] - 1)

        print('Start Saving Data to CSV...')
        data_path = os.path.join(self.crawl_file_dir, self.forex_trend_summary_file)
        data_df[['TICKER', 'LAST', '1W CHG %', '1M CHG %']].to_csv(data_path, index=False, encoding='utf-8')
        return True

    def crawl_forex_position_data(self):
        """ 爬取并保存外汇头寸持仓数据 """
        print('Start Crawl Forex Position Data...')
        cftc_net_position_df = self.get_cftc_net_position_df()
        print('Start Saving Data To CSV...')
        cftc_net_position_df.to_csv(os.path.join(self.crawl_file_dir, self.cftc_net_position_file), index=False,
                                    encoding='utf-8-sig')
        return True

    def crawl_major_currency_forecast(self):
        """ 爬取并保存 主要货币对走势预测 数据 """
        news_url = self.get_fx168_trading_analysis_url()
        analysis_dict = self.get_fx168_trading_analysis_dict(news_url)
        with open(os.path.join(self.crawl_file_dir, self.major_currency_forecast_file), 'w') as f:
            json.dump(analysis_dict, f)
        return True

    def crawl_option_strategy(self):
        """ 爬取 人民币套期保值 相关数据 """
        return True

    # def crawl_forex_future_data_event(self):
    #     """ 爬取并保存 财经数据&事件 数据 """
    #     print('Start crawl_forex_future_data_event...')
    #     # 获取爬取日期范围
    #     y, m, d = self.week_start.split('-')
    #     comp_week_start = '{}-{}-{}'.format(y, m.zfill(2), d.zfill(2))
    #     week = 'this' if comp_week_start <= str(datetime.datetime.now())[:10] else 'next'
    #     week_dates = self.get_week_dates(week)
    #     # 爬取数据的DataFrame
    #     print('Start Crawl From Website...{}-{}'.format(week_dates[0], week_dates[-1]))
    #     data_df = self.get_future_data_event_df(week_dates, 'data', 3)
    #     event_df = self.get_future_data_event_df(week_dates, 'event', 3)
    #     # 筛取一部分财经数据，避免数量过多
    #     print('Start Filter Necessary Financial Data...')
    #     data_df = self.filter_jin10_financial_data_df(data_df)
    #     # 保存Excel
    #     print('Start Save Data To Excel...')
    #     with pd.ExcelWriter(os.path.join(self.crawl_file_dir, self.forex_future_data_event_file)) as writer:
    #         data_df.to_excel(writer, 'DATA', index=False)
    #         event_df.to_excel(writer, 'EVENT', index=False)
    #     return True

    def crawl_forex_future_data_event(self):
        """ 爬取并保存 财经数据&事件 数据 """
        print('Start crawl_forex_future_data_event...')
        # 获取爬取日期范围
        y, m, d = self.week_start.split('-')
        comp_week_start = '{}-{}-{}'.format(y, m.zfill(2), d.zfill(2))
        week = 'this' if comp_week_start <= str(datetime.datetime.now())[:10] else 'next'
        week_dates = self.get_week_dates(week)
        # 爬取数据的DataFrame
        print('Start Crawl From Website...{}-{}'.format(week_dates[0], week_dates[-1]))
        data_df, event_df = self.get_future_data_event_df_selenium(week_dates)
        # 筛取一部分财经数据，避免数量过多
        print('Start Filter Necessary Financial Data...')
        data_df = self.filter_jin10_financial_data_df(data_df)
        # 保存Excel
        print('Start Save Data To Excel...')
        excel_path = os.path.join(self.crawl_file_dir, self.forex_future_data_event_file)
        with pd.ExcelWriter(excel_path) as writer:
            data_df.to_excel(writer, 'DATA', index=False)
            event_df.to_excel(writer, 'EVENT', index=False)
        return True

    def generate_fundamental_event_data(self):
        data_df = pd.read_csv(os.path.join(self.crawl_file_dir, self.fund_event_summary_file))
        res = {'data_lst': data_df.to_dict(orient='records')}
        return res

    def generate_forex_trend_summary(self):
        """
        生成外汇期货合约趋势数据（含图表图片）
        
        读取爬取的外汇趋势数据，处理后生成趋势表格图片，同时生成简体和繁体版本。
        
        Returns:
            dict: 包含生成的图片文件名
        """
        # 读取爬取的趋势数据文件
        forex_trend_summary_data = pd.read_csv(os.path.join(self.crawl_file_dir, self.forex_trend_summary_file))
        
        # 处理数据格式
        trend_data = self.reformat_forex_trend_summary_data(forex_trend_summary_data, self.week_start)
        
        # 渲染简体表格图片
        fig, ax = self.render_forex_trend_table(trend_data, cellLoc='left',
                                               col_width=1.2, row_height=0.4, row_colors=['lightblue', 'w'],
                                               dynamic_num_color_cols=[4, 5])
        image_path = os.path.join(self.output_file_dir, self.forex_trend_summary_pic)
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)
        
        # 生成繁体版本
        data_df_traditional = self.df_to_traditional(trend_data)
        fig, ax = self.render_forex_trend_table(data_df_traditional, cellLoc='left',
                                                col_width=1.2, row_height=0.4, row_colors=['lightblue', 'w'],
                                                dynamic_num_color_cols=[4, 5])
        image_path = os.path.join(self.output_file_dir, self.traditional_forex_trend_summary_pic)
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)
        
        # 返回结果
        res = {
            'image_name': self.forex_trend_summary_pic,
        }
        return res

    def generate_forex_position_data(self):
        """ 生成外汇头寸持仓数据 """
        if os.path.exists(os.path.join(self.crawl_file_dir, self.cftc_net_position_file)):
            data_df = pd.read_csv(os.path.join(self.crawl_file_dir, self.cftc_net_position_file))
            data_df = pd.merge(pd.DataFrame(self.display_curr_order, columns=['货币']), data_df, how='left', on='货币')
            # Figure
            fig, ax = self.get_picture_from_forex_position(data_df)
            img_path = os.path.join(self.output_file_dir, self.cftc_net_position_pic)
            fig.savefig(img_path)
            self.add_image_border(img_path, img_path, bc=(0, 100, 255), dst_w=960)
            # 修改为繁体
            data_df_traditional = self.df_to_traditional(data_df)
            print(data_df_traditional)
            fig, ax = self.get_picture_from_forex_position(data_df_traditional)
            img_path = os.path.join(self.output_file_dir, self.traditional_cftc_net_position_pic)
            fig.savefig(img_path)
            self.add_image_border(img_path, img_path, bc=(0, 100, 255), dst_w=960)
            # Summary Text
            text = self.get_text_from_forex_position(data_df)
            data = {
                'data_lst':     data_df.to_dict(orient='records'),
                'data_path':    os.path.join(self.crawl_file_dir, self.cftc_net_position_file),
                'picture_name': self.cftc_net_position_pic,
                'text':         text,
            }
        else:
            data = {
                'data_lst': [],
                'data_path': '未找到持仓数据文件',
                'picture_name': '',
                'text': '未找到持仓数据文件',
            }
        return data

    def generate_major_currency_forecast(self):
        """ 生成 重点货币对展望 数据 """
        if os.path.exists(os.path.join(self.crawl_file_dir, self.major_currency_forecast_file)):
            with open(os.path.join(self.crawl_file_dir, self.major_currency_forecast_file), 'r') as f:
                data = json.load(f)
            res = {'analysis_dict': data}
            return res
        return

    def generate_forex_future_data_event(self, data_type):
        """ 获取渲染HTML需要的数据，data_typ """
        file_path = os.path.join(self.crawl_file_dir, self.forex_future_data_event_file)
        data_df = pd.read_excel(file_path, data_type).fillna('')
        data_json_lst = data_df.to_dict(orient='records')

        if data_type == 'DATA':
            render_data_df = data_df[['date', 'time', 'country', 'time_period', 'name']]
            render_data_df.columns = ['日期', '时间', '国家', '数据区间', '数据类型']
            new_text_lst, row_size_lst = self.reformat_long_text(render_data_df['数据类型'], None, None)
            render_data_df['数据类型'] = new_text_lst
        elif data_type == 'EVENT':
            render_data_df = data_df[['date', 'time', 'country', 'people', 'event_content']]
            render_data_df.columns = ['日期', '时间', '国家', '人物', '事件内容']
            new_text_lst, row_size_lst = self.reformat_long_text(render_data_df['事件内容'], None, None)
            render_data_df['事件内容'] = new_text_lst
        #print(data_type, row_size_lst+[1])
        fig, ax = self.render_future_data_event_table(render_data_df,
                                                      colWidths=np.array([1.2, 0.8, 1, 1.5, 8.]),
                                                      rowHeights=np.array(row_size_lst+[1]),
                                                      row_height=0.4,
                                                      cellLoc='right')
        image_path = os.path.join(self.output_file_dir, self.future_data_event_data_types[data_type])
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)
        # 修改为繁体
        data_df_traditional = self.df_to_traditional(render_data_df)
        # print(data_df_traditional)
        fig, ax = self.render_future_data_event_table(data_df_traditional,
                                                      colWidths=np.array([1.2, 0.8, 1, 1.5, 8.]),
                                                      rowHeights=np.array(row_size_lst + [1]),
                                                      row_height=0.4,
                                                      cellLoc='right')
        image_path = os.path.join(self.output_file_dir, self.traditional_future_data_event_data_types[data_type])
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)

        res = {
            'data_json_lst': data_json_lst,
            'image_name': '{}.png'.format(data_type),
        }
        return res


    def generate_output_files(self, report_title, 
                                    report_summary,
                                    fundamental_events,
                                    trend_image_src,
                                    position_summary_data,
                                    curr_forecasts,
                                    strategy_info,
                                    data_image_src, 
                                    event_image_src):
        """ 生成周报结果文件 """
        # 加载周报模板
        word_tpl_path = os.path.join(self.meta_data_dir, "Cloudhands Report Demo.docx")
        tpl = DocxTemplate(word_tpl_path)
        # 拼接 png_path & output_path
        forex_trend_summary_png_path = os.path.join(self.output_file_dir, self.forex_trend_summary_pic)
        cftc_net_position_png_path = os.path.join(self.output_file_dir, self.cftc_net_position_pic)
        future_data_png_path = os.path.join(self.output_file_dir, self.future_data_event_data_types['DATA'])
        future_event_png_path = os.path.join(self.output_file_dir, self.future_data_event_data_types['EVENT'])
        output_word_path = os.path.join(self.output_file_dir, self.weekly_report_output['docx-jt'])
        output_pdf_path = os.path.join(self.output_file_dir, self.weekly_report_output['pdf-jt'])
        # 进行文本内容替换
        context = {
            'Report_Period':  self._week_report_period,

            'Report_Title':   report_title,
            'Report_Summary': report_summary,

            'Title_Fundamental_1':   fundamental_events[0]['title'],
            'Content_Fundamental_1': fundamental_events[0]['content'],
            'Title_Fundamental_2':   fundamental_events[1]['title'],
            'Content_Fundamental_2': fundamental_events[1]['content'],
            'Title_Fundamental_3':   fundamental_events[2]['title'],
            'Content_Fundamental_3': fundamental_events[2]['content'],

            'Picture_Trend':    InlineImage(tpl, forex_trend_summary_png_path, width=Pt(350)),
            # 外汇期货上周持仓头寸统计
            'Picture_Position': InlineImage(tpl, cftc_net_position_png_path, width=Pt(320)),
            'Content_Position': position_summary_data['text'],
            # 主要货币对走势展望
            'Content_Forecast_1': curr_forecasts[0]['forecast'],
            'Content_Forecast_2': curr_forecasts[1]['forecast'],
            'Content_Forecast_3': curr_forecasts[2]['forecast'],
            'Content_Forecast_4': curr_forecasts[3]['forecast'],
            # 外汇期权策略
            'Title_Strategy':   strategy_info['strategy_title'],
            'Content_Strategy': strategy_info['strategy_content'],
            'Picture_Strategy': strategy_info['strategy_img_src'],
            # 财经数据 & 财经事件
            'Blank_FutureData': '\n' * self.get_pic_height_blank_row_amt(future_data_png_path),
            'Picture_FutureData': InlineImage(tpl, future_data_png_path, width=Pt(400)),
            'Blank_FutureEvent': '\n' * self.get_pic_height_blank_row_amt(future_event_png_path),
            'Picture_FutureEvent': InlineImage(tpl, future_event_png_path, width=Pt(400)),
        }
        tpl.render(context)
        # 生成简体cWord + 转换PDF
        tpl.save(output_word_path)
        DocxUtils().docx_to_pdf(output_word_path,output_pdf_path)

        # 拼接 png_path & output_path
        traditional_forex_trend_summary_png_path = os.path.join(self.output_file_dir, self.traditional_forex_trend_summary_pic)
        traditional_cftc_net_position_png_path = os.path.join(self.output_file_dir, self.traditional_cftc_net_position_pic)
        traditional_future_data_png_path = os.path.join(self.output_file_dir, self.traditional_future_data_event_data_types['DATA'])
        traditional_future_event_png_path = os.path.join(self.output_file_dir, self.traditional_future_data_event_data_types['EVENT'])
        traditional_output_word_path = os.path.join(self.output_file_dir, self.weekly_report_output['docx-ft'])
        traditional_output_pdf_path = os.path.join(self.output_file_dir, self.weekly_report_output['pdf-ft'])
        # 进行文本内容替换
        tpl = DocxTemplate(word_tpl_path)
        context['Picture_Trend'] = InlineImage(tpl, traditional_forex_trend_summary_png_path, width=Pt(350))
        context['Picture_Position'] = InlineImage(tpl, traditional_cftc_net_position_png_path, width=Pt(320))
        context['Picture_FutureData'] = InlineImage(tpl, traditional_future_data_png_path, width=Pt(400))
        context['Picture_FutureEvent'] = InlineImage(tpl, traditional_future_event_png_path, width=Pt(400))
        tpl.render(context)
        # 生成繁体Word + 文本简转繁 + 生成PDF
        tpl.save(traditional_output_word_path)
        DocxUtils().translate_to_traditional(traditional_output_word_path, traditional_output_word_path)
        DocxUtils().docx_to_pdf(traditional_output_word_path, traditional_output_pdf_path)
        return True



    @staticmethod
    def get_pic_height_blank_row_amt(pic_path, resize_width=400, blank_row_height=16):
        """ 获取图片按照宽度resize后的高度，需要多少空行 """
        im = Image.open(pic_path)
        resize_height = resize_width * im.size[1] / im.size[0]
        n = (resize_height//blank_row_height+1)-2
        return int(n)

    @staticmethod
    def render_forex_trend_table(data, dynamic_num_color_cols=[], col_width=3.0, row_height=0.625, font_size=14,
                                 header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w', bbox=[0, 0, 1, 1],
                                 header_columns=0, fig=None, ax=None, **kwargs):
        """ 渲染 外汇期货历史行情表  """
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            if 'colWidths' in kwargs:
                size[0] = kwargs['colWidths'].sum()
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in mpl_table._cells.items():
            (row_id, col_id) = k
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])
                if col_id in dynamic_num_color_cols:
                    value = data.values[(row_id - 1, col_id)]
                    color = 'red' if float(value.replace('%', '')) >= 0 else 'green'
                    cell.set_text_props(color=color)
        fig.tight_layout()
        return fig, ax

    @staticmethod
    def reformat_long_text(text_lst, fontsize, need_line_width):
        new_text_lst = []
        row_size_lst = []
        for line_text in text_lst:
            insert_idxes = [i for i in range(len(line_text)) if i%38 == 37]
            list_line_text = list(line_text)
            for i in insert_idxes[::-1]:
                list_line_text.insert(i, '\n')

            new_text_lst.append(''.join(list_line_text))
            row_size_lst.append(len(insert_idxes)+1)
        return new_text_lst, row_size_lst

    @staticmethod
    def render_future_data_event_table(data, col_width=3.0, row_height=0.625, font_size=14, rowHeights=None,
                                       header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                                       bbox=[0, 0, 1, 1], header_columns=0, fig=None, ax=None, **kwargs):
        """ 渲染财经数据和财经事件表 """
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            if 'colWidths' in kwargs:
                size[0] = kwargs['colWidths'].sum()
            if rowHeights is not None:
                size[1] = rowHeights.sum() * row_height
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in mpl_table._cells.items():
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors)])
            if rowHeights is not None:
                cell.set_height(rowHeights[k[0]-1] * row_height)
        fig.tight_layout()
        return fig, ax

    @staticmethod
    def get_contract_symbol(TICKER, str_data_date):
        curr_contact_symbol_dict = {
            'EURUSD': '6E',
            'USDJPY': '6J',
            'GBPUSD': '6B',
            'AUDUSD': '6A',
            'USDCAD': '6C',
            'USDCHF': '6S',
            'NZDUSD': '6N',
            'USDCNY': 'CNH',
        }
        symbol1 = curr_contact_symbol_dict[TICKER]

        dt_data_date = datetime.datetime.strptime(str_data_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        month_day_one = dt_data_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        week_num = int(dt_data_date.strftime('%W')) - int(month_day_one.strftime('%W')) + 1
        contract_year = int(str_data_date[:4])
        if dt_data_date.month in [12]:
            if week_num < 3:
                symbol2 = 'Z'
            else:
                symbol2 = 'H'
                contract_year += 1
        elif dt_data_date.month in (1, 2):
            symbol2 = 'H'
        elif dt_data_date.month in (3, ):
            if week_num < 3:
                symbol2 = 'H'
            else:
                symbol2 = 'M'
        elif dt_data_date.month in (4, 5):
            symbol2 = 'M'
        elif dt_data_date.month in (6, ):
            if week_num < 3:
                symbol2 = 'M'
            else:
                symbol2 = 'U'
        elif dt_data_date.month in (7, 8):
            symbol2 = 'U'
        elif dt_data_date.month in (9, ):
            if week_num < 3:
                symbol2 = 'U'
            else:
                symbol2 = 'Z'
        elif dt_data_date.month in (10, 11):
            symbol2 = 'Z'

        symbol = '{}{}{}'.format(symbol1, symbol2, contract_year)
        contract_month_dict = {
            'H': 'Mar',
            'M': 'Jun',
            'U': 'Sep',
            'Z': 'Dec',
        }
        contract_month = '{}-{}'.format(contract_month_dict[symbol2], contract_year % 100)
        return symbol, contract_month

    def convert_simplified_to_traditional_word(self):
        """
        将简体Word文件转换为繁体Word文件（包括文本和图片）
        
        使用类属性中已维护的路径：
        - 输入: self.output_file_dir + self.weekly_report_output['docx-jt']
        - 输出: self.output_file_dir + self.weekly_report_output['docx-ft']
        
        步骤：
        1. 先进行文本简繁转换
        2. 再替换图片为繁体版本
        
        Returns:
            bool: 转换成功返回True，失败返回False
        """
        try:
            # 获取输入输出路径（已维护在类属性中）
            output_word_path = os.path.join(self.output_file_dir, self.weekly_report_output['docx-jt'])
            output_pdf_path = os.path.join(self.output_file_dir, self.weekly_report_output['pdf-jt'])
            traditional_output_word_path = os.path.join(self.output_file_dir, self.weekly_report_output['docx-ft'])
            traditional_output_pdf_path = os.path.join(self.output_file_dir, self.weekly_report_output['pdf-ft'])
        
            # 检查输入文件是否存在
            if not os.path.exists(output_word_path):
                print(f'错误：输入文件不存在: {output_word_path}')
                return False
            
            # 步骤1：使用 DocxUtils 进行文本简繁转换
            DocxUtils().translate_to_traditional(output_word_path, traditional_output_word_path)
            
            # 步骤2：替换图片为繁体版本
            self._replace_images_in_word(traditional_output_word_path)
            
            # 步骤3：生成PDF
            DocxUtils().docx_to_pdf(output_word_path, output_pdf_path)
            DocxUtils().docx_to_pdf(traditional_output_word_path, traditional_output_pdf_path)
            
            return True
        except Exception as e:
            print(f'简繁转换失败: {e}')
            return False

    def _replace_images_in_word(self, word_path):
        """
        替换Word文档中的图片为繁体版本
        
        Word内部图片顺序（共5张）：
        - image1.jpg: 封面/Logo（不替换）
        - image2.png: trend图表 → 替换为繁体trend
        - image3.png: position图表 → 替换为繁体position  
        - image4.png: data图表 → 替换为繁体data
        - image5.png: event图表 → 替换为繁体event
        """
        import zipfile
        import shutil
        import tempfile
        
        # 繁体图片路径（按顺序对应 image2-image5）
        traditional_images = [
            os.path.join(self.output_file_dir, self.traditional_forex_trend_summary_pic),
            os.path.join(self.output_file_dir, self.traditional_cftc_net_position_pic),
            os.path.join(self.output_file_dir, self.traditional_future_data_event_data_types['DATA']),
            os.path.join(self.output_file_dir, self.traditional_future_data_event_data_types['EVENT']),
        ]
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. 解压 Word 文档
            with zipfile.ZipFile(word_path, 'r') as zf:
                zf.extractall(temp_dir)
            
            # 2. 替换图片（从第2张开始，跳过第1张封面）
            media_dir = os.path.join(temp_dir, 'word', 'media')
            image_names = ['image2.png', 'image3.png', 'image4.png', 'image5.png']
            
            for i, image_name in enumerate(image_names):
                src_img = traditional_images[i]
                dst_img = os.path.join(media_dir, image_name)
                
                if os.path.exists(src_img):
                    shutil.copy2(src_img, dst_img)
                    print(f'替换图片: {image_name} <- {os.path.basename(src_img)}')
                else:
                    print(f'警告：繁体图片不存在: {src_img}')
            
            # 3. 重新压缩为 Word 文档
            os.remove(word_path)
            with zipfile.ZipFile(word_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zf.write(file_path, arcname)

    def generate_forex_position_data_html(self):
        """
        生成CFTC持仓数据HTML表格（替代PNG图片）
        
        Returns:
            dict: 包含生成的HTML文件名
        """
        if os.path.exists(os.path.join(self.crawl_file_dir, self.cftc_net_position_file)):
            data_df = pd.read_csv(os.path.join(self.crawl_file_dir, self.cftc_net_position_file))
            data_df = pd.merge(pd.DataFrame(self.display_curr_order, columns=['货币']), data_df, how='left', on='货币')
            
            # 生成简体HTML
            html_content = self._generate_cftc_position_html(data_df, is_traditional=False)
            html_path = os.path.join(self.output_file_dir, 'cftc_net_position.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 生成繁体HTML（手动设置繁体列名）
            data_df_traditional = self.df_to_traditional(data_df)
            # 手动设置繁体列名（因为df_to_traditional不会转换列名）
            data_df_traditional.columns = ['貨幣', '上周淨持倉', '本周淨持倉', 'delta淨持倉', 'report_date']
            html_content_traditional = self._generate_cftc_position_html(data_df_traditional, is_traditional=True)
            html_path_traditional = os.path.join(self.output_file_dir, 'fanti_cftc_net_position.html')
            with open(html_path_traditional, 'w', encoding='utf-8') as f:
                f.write(html_content_traditional)
            
            data = {
                'data_lst': data_df.to_dict(orient='records'),
                'data_path': os.path.join(self.crawl_file_dir, self.cftc_net_position_file),
                'picture_name': 'cftc_net_position.html',
                'text': self.get_text_from_forex_position(data_df),
            }
        else:
            data = {
                'data_lst': [],
                'data_path': '未找到持仓数据文件',
                'picture_name': '',
                'text': '未找到持仓数据文件',
            }
        return data

    def generate_forex_trend_summary_html(self):
        """
        生成外汇趋势数据HTML表格（替代PNG图片）
        
        Returns:
            dict: 包含生成的HTML文件名
        """
        forex_trend_summary_data = pd.read_csv(os.path.join(self.crawl_file_dir, self.forex_trend_summary_file))
        trend_data = self.reformat_forex_trend_summary_data(forex_trend_summary_data, self.week_start)
        
        # 生成简体HTML
        html_content = self._generate_forex_trend_html(trend_data, is_traditional=False)
        html_path = os.path.join(self.output_file_dir, 'forex_trend_summary.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 生成繁体HTML
        data_df_traditional = self.df_to_traditional(trend_data)
        html_content_traditional = self._generate_forex_trend_html(data_df_traditional, is_traditional=True)
        html_path_traditional = os.path.join(self.output_file_dir, 'fanti_forex_trend_summary.html')
        with open(html_path_traditional, 'w', encoding='utf-8') as f:
            f.write(html_content_traditional)
        
        res = {
            'image_name': 'forex_trend_summary.html',
        }
        return res

    def generate_forex_future_data_event_html(self, data_type):
        """
        生成财经数据/事件HTML表格（替代PNG图片）
        
        Args:
            data_type: 'DATA' 或 'EVENT'
        
        Returns:
            dict: 包含生成的HTML文件名
        """
        file_path = os.path.join(self.crawl_file_dir, self.forex_future_data_event_file)
        data_df = pd.read_excel(file_path, data_type).fillna('')
        data_json_lst = data_df.to_dict(orient='records')

        if data_type == 'DATA':
            render_data_df = data_df[['date', 'time', 'country', 'time_period', 'name']]
            render_data_df.columns = ['日期', '时间', '国家', '数据区间', '数据类型']
            new_text_lst, row_size_lst = self.reformat_long_text(render_data_df['数据类型'], None, None)
            render_data_df['数据类型'] = new_text_lst
        elif data_type == 'EVENT':
            render_data_df = data_df[['date', 'time', 'country', 'people', 'event_content']]
            render_data_df.columns = ['日期', '时间', '国家', '人物', '事件内容']
            new_text_lst, row_size_lst = self.reformat_long_text(render_data_df['事件内容'], None, None)
            render_data_df['事件内容'] = new_text_lst
        
        y, m, d = self.week_start.split('-')
        comp_week_start = '{}-{}-{}'.format(y, m.zfill(2), d.zfill(2))
        week = 'this' if comp_week_start <= str(datetime.datetime.now())[:10] else 'next'
        week_dates = self.get_week_dates(week)
        week_dates_mon_to_fri = week_dates[:5]
        
        html_content = self._generate_future_data_event_html(render_data_df, data_type, week_dates_mon_to_fri, is_traditional=False)
        html_path = os.path.join(self.output_file_dir, f'{data_type}.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        data_df_traditional = self.df_to_traditional(render_data_df)
        html_content_traditional = self._generate_future_data_event_html(data_df_traditional, data_type, week_dates_mon_to_fri, is_traditional=True)
        html_path_traditional = os.path.join(self.output_file_dir, f'fanti_{data_type}.html')
        with open(html_path_traditional, 'w', encoding='utf-8') as f:
            f.write(html_content_traditional)
        
        res = {
            'data_json_lst': data_json_lst,
            'image_name': f'{data_type}.html',
        }
        return res

    def _generate_cftc_position_html(self, data_df, is_traditional=False):
        """生成CFTC持仓数据HTML（ECharts图表版）"""
        title = '外汇期货持仓变化' if not is_traditional else '外匯期貨持倉變化'
        
        # 动态检测列名
        columns = data_df.columns.tolist()
        if '貨幣' in columns:
            col_currency = '貨幣'
            col_last_week = '上周淨持倉' if '上周淨持倉' in columns else '上周净持仓'
            col_this_week = '本周淨持倉' if '本周淨持倉' in columns else '本周净持仓'
        else:
            col_currency = '货币'
            col_last_week = '上周净持仓'
            col_this_week = '本周净持仓'
        
        # 获取数据
        currencies = data_df[col_currency].tolist()
        last_week_data = data_df[col_last_week].fillna(0).astype(int).tolist()
        this_week_data = data_df[col_this_week].fillna(0).astype(int).tolist()
        
        # 转换货币名称为繁体
        if is_traditional:
            currency_map = {'欧元':'歐元', '澳元':'澳元', '英镑':'英鎊', '日元':'日圓', '加元':'加幣', '纽元':'紐元'}
            currencies = [currency_map.get(c, c) for c in currencies]
        
        # 计算Y轴范围
        all_data = last_week_data + this_week_data
        y_min = min(all_data) * 1.2
        y_max = max(all_data) * 1.2
        
        # 繁体/简体文本
        title_text = f'截至上周二 ({data_df["report_date"].iloc[0]})CFTC各货币期货净持仓变化' if not is_traditional else f'截至上週二 ({data_df["report_date"].iloc[0]})CFTC各貨幣期貨淨持倉變化'
        legend_last = '上周净持仓' if not is_traditional else '上週淨持倉'
        legend_this = '本周净持仓' if not is_traditional else '本週淨持倉'
        y_axis_name = '净持仓量（万手）' if not is_traditional else '淨持倉量（萬手）'
        remarks_title = '📌 数据说明' if not is_traditional else '📌 數據說明'
        remarks_text1 = '• 根据原始 Excel 完整生成，所有数据精确展示。' if not is_traditional else '• 根據原始 Excel 完整生成，所有數據精確展示。'
        remarks_text2 = '• 负值 = 净空头，正值 = 净多头。' if not is_traditional else '• 負值 = 淨空頭，正值 = 淨多頭。'
        remarks_text3 = '• 数值标签根据正负值自动调整位置（正值在柱顶上方，负值在柱底下方）。' if not is_traditional else '• 數值標籤根據正負值自動調整位置（正值在柱頂上方，負值在柱底下方）。'
        footer_text = '✨ 字体全面增大 · 微软雅黑 · 数值标签智能定位 · 完整外汇期货持仓 ✨' if not is_traditional else '✨ 字體全面增大 · 微軟雅黑 · 數值標籤智能定位 · 完整外匯期貨持倉 ✨'

        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'sqlite', 'cftc_position_template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        html = html.format(
            title=title,
            remarks_title=remarks_title,
            remarks_text1=remarks_text1,
            remarks_text2=remarks_text2,
            remarks_text3=remarks_text3,
            legend_last=legend_last,
            legend_this=legend_this,
            footer_text=footer_text,
            currencies=currencies,
            last_week_data=last_week_data,
            this_week_data=this_week_data,
            y_min=y_min,
            y_max=y_max,
            title_text=title_text,
            y_axis_name=y_axis_name
        )
        return html

    def _generate_forex_trend_html(self, trend_data, is_traditional=False):
        """生成外汇趋势数据HTML表格（参考forex_trend_summary.html样式）"""
        # 动态检测列名
        columns = trend_data.columns.tolist()
        if '期货' in columns:
            col_ticker = '期货'
            col_code = '代码'
            col_expiry = '合约到期月'
            col_last = '最新价'
            col_week = '周变动'
            col_month = '月变动'
        else:
            col_ticker = columns[0] if len(columns) > 0 else 'TICKER'
            col_code = columns[1] if len(columns) > 1 else '代码'
            col_expiry = columns[2] if len(columns) > 2 else '合约到期月'
            col_last = columns[3] if len(columns) > 3 else '最新价'
            col_week = columns[4] if len(columns) > 4 else '周变动'
            col_month = columns[5] if len(columns) > 5 else '月变动'
        
        # 货币行样式映射
        row_styles = ['row-eur', 'row-jpy', 'row-gbp', 'row-aud', 'row-cad', 'row-chf', 'row-nzd', 'row-cny']
        
        # 货币表情符号映射
        currency_flags = {
            '欧元': '🇪🇺', '歐元': '🇪🇺',
            '日元': '🇯🇵', '日圓': '🇯🇵',
            '英镑': '🇬🇧', '英鎊': '🇬🇧',
            '澳元': '🇦🇺',
            '加元': '🇨🇦',
            '瑞郎': '🇨🇭',
            '纽元': '🇳🇿', '紐元': '🇳🇿',
            '人民币': '🇨🇳', '人民幣': '🇨🇳'
        }
        
        # 简体/繁体文本
        if not is_traditional:
            title = '📊 外汇期货数据汇总 · 全篇统一38px'
            subtitle = '横版 · 货币为行 | 微软雅黑 · 全篇统一38px超大字号 | 合约到期月：'
            header_note = '✅ 标题、表头、正文、数据、备注全部统一38px，清晰醒目'
            col_currency = '货币'
            col_future_code = '期货代码'
            col_expiry_month = '合约到期月'
            col_latest = '最新价'
            col_weekly = '周变动'
            col_monthly = '月变动'
            remarks_title = '📌 数据说明'
            remarks_data_source = '• <strong>数据来源</strong>：根据原始 Excel 文件完整生成，未省略任何数据项。'
            remarks_expiry = '• <strong>合约到期月</strong>：所有合约均为'
            remarks_color = '• <strong>颜色标识</strong>：<span style="color:#2a7a4b; font-weight:800;">绿色/正号</span>表示上涨，<span style="color:#c23d3d; font-weight:800;">红色/负号</span>表示下跌。'
            remarks_latest = '• <strong>最新价</strong>：截至最近交易日的结算价或最新报价。'
            remarks_note1 = '• 🎯 本版本全篇统一38px超大字号：标题、表头、货币名、数据、备注均为38px，每个字都清晰醒目。'
            remarks_note2 = '• 💡 所有单元格文字统一大小，适合远距离观看、投屏、老年阅读或截图分享。其中"人民币"所在单元格强制单行显示，不换行。'
            footer_text = '✨ 全篇统一38px · 微软雅黑 · 横版货币行 · 完整外汇期货数据 · 人民币一行展示 ✨'
        else:
            title = '📊 外匯期貨數據彙總 · 全篇統一38px'
            subtitle = '橫版 · 貨幣為行 | 微軟雅黑 · 全篇統一38px超大字號 | 合約到期月：'
            header_note = '✅ 標題、表頭、正文、數據、備註全部統一38px，清晰醒目'
            col_currency = '貨幣'
            col_future_code = '期貨代碼'
            col_expiry_month = '合約到期月'
            col_latest = '最新價'
            col_weekly = '周變動'
            col_monthly = '月變動'
            remarks_title = '📌 數據說明'
            remarks_data_source = '• <strong>數據來源</strong>：根據原始 Excel 檔案完整生成，未省略任何數據項。'
            remarks_expiry = '• <strong>合約到期月</strong>：所有合約均為'
            remarks_color = '• <strong>顏色標識</strong>：<span style="color:#2a7a4b; font-weight:800;">綠色/正號</span>表示上漲，<span style="color:#c23d3d; font-weight:800;">紅色/負號</span>表示下跌。'
            remarks_latest = '• <strong>最新價</strong>：截至最近交易日的結算價或最新報價。'
            remarks_note1 = '• 🎯 本版本全篇統一38px超大字號：標題、表頭、貨幣名、數據、備註均為38px，每個字都清晰醒目。'
            remarks_note2 = '• 💡 所有單元格文字統一大小，適合遠距離觀看、投屏、老年閱讀或截圖分享。其中"人民幣"所在單元格強制單行顯示，不換行。'
            footer_text = '✨ 全篇統一38px · 微軟雅黑 · 橫版貨幣行 · 完整外匯期貨數據 · 人民幣一行展示 ✨'
        
        # 获取到期月用于标题
        expiry_month = trend_data[col_expiry].iloc[0] if len(trend_data) > 0 else ''
        
        # 生成表格行
        table_rows = ''
        for idx, (_, row) in enumerate(trend_data.iterrows()):
            ticker = row[col_ticker]
            flag = currency_flags.get(ticker, '')
            row_style = row_styles[idx % len(row_styles)]
            
            # 处理数值格式
            last_val = row[col_last]
            week_val = row[col_week]
            month_val = row[col_month]
            
            # 判断正负类
            week_chg_class = 'positive' if (isinstance(week_val, str) and week_val.startswith('+')) or (isinstance(week_val, (int, float)) and week_val > 0) else 'negative' if (isinstance(week_val, str) and '-' in week_val) or (isinstance(week_val, (int, float)) and week_val < 0) else 'neutral'
            month_chg_class = 'positive' if (isinstance(month_val, str) and month_val.startswith('+')) or (isinstance(month_val, (int, float)) and month_val > 0) else 'negative' if (isinstance(month_val, str) and '-' in month_val) or (isinstance(month_val, (int, float)) and month_val < 0) else 'neutral'
            
            table_rows += f'''
                    <tr class="{row_style}">
                        <td>{flag} {ticker}</td>
                        <td>{row[col_code]}</td>
                        <td>{row[col_expiry]}</td>
                        <td><span class="neutral">{last_val if isinstance(last_val, str) else f'{last_val:.4f}'}</span></td>
                        <td><span class="{week_chg_class}">{week_val}</span></td>
                        <td><span class="{month_chg_class}">{month_val}</span></td>
                    </tr>'''
        
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'sqlite', 'forex_trend_template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        html = html.format(
            title=title,
            subtitle=subtitle,
            expiry_month=expiry_month,
            header_note=header_note,
            col_currency=col_currency,
            col_future_code=col_future_code,
            col_expiry_month=col_expiry_month,
            col_latest=col_latest,
            col_weekly=col_weekly,
            col_monthly=col_monthly,
            remarks_title=remarks_title,
            remarks_data_source=remarks_data_source,
            remarks_expiry=remarks_expiry,
            remarks_color=remarks_color,
            remarks_latest=remarks_latest,
            remarks_note1=remarks_note1,
            remarks_note2=remarks_note2,
            footer_text=footer_text,
            table_rows=table_rows
        )
        return html


    def _generate_future_data_event_html(self, data_df, data_type, week_dates_mon_to_fri, is_traditional=False):
        """生成财经数据/事件HTML表格（参考DATA.html和EVENT.html样式）"""
        row_styles = {
            '中国': 'row-china', '中國': 'row-china',
            '欧元区': 'row-eurozone', '歐元區': 'row-eurozone',
            '美国': 'row-usa', '美國': 'row-usa',
            '法国': 'row-france', '法國': 'row-france',
            '英国': 'row-uk', '英國': 'row-uk',
            '日本': 'row-japan', '日本': 'row-japan',
            '加拿大': 'row-canada', '加拿大': 'row-canada',
            '澳大利亚': 'row-canada',
            '德国': 'row-germany', '德國': 'row-germany',
            '国际': 'row-intl', '國際': 'row-intl'
        }
        
        week_dates_set = set(week_dates_mon_to_fri)
        
        # 简体/繁体文本
        if not is_traditional:
            title = '📊 全球财经日程' if data_type == 'EVENT' else '📊 全球经济数据日程'
            subtitle = '横版 · 国家为行 | 微软雅黑 · 全篇统一38px超大字号'
            header_note = '✅ 标题、表头、正文、数据全部统一38px，清晰醒目'
            split_hint = '📸 多图分段指南：如需截取多张图片，可从此处分割，上下两部分各取所需，大字体完整保留。'
            remarks_title = '📌 数据说明'
            remarks_data_source = '• 数据来源：原始Excel数据完整生成'
            remarks_time = '• 时间格式：统一采用24小时制显示'
            remarks_note1 = '• 空白单元格表示当日无相关数据/事件'
            remarks_note2 = '• 数据/事件按时间顺序横向排列'
            remarks_note3 = '• 重要数据/事件已突出显示'
            footer_text = '✨ 全38px统一超大字号 · 微软雅黑 · 横版国家行 · 完整经济数据日程 ✨' if data_type == 'DATA' else '✨ 全球财经日程 · 全篇统一38px微软雅黑 · 每行独立配色 · 事件横向排 · 清晰极简 ✨'
            empty_cell = '—'
            week_days = ['周一', '周二', '周三', '周四', '周五']
            col_country = '🌍 国家 / 地区'
            countries = ['中国', '欧元区', '美国', '法国', '英国']
            col_date = '日期'
            col_country_name = '国家'
            col_time = '时间'
            col_data_name = '数据类型'
            col_event_content = '事件内容'
            col_people = '人物'
        else:
            title = '📊 全球財經日程' if data_type == 'EVENT' else '📊 全球經濟數據日程'
            subtitle = '橫版 · 國家為行 | 微軟雅黑 · 全篇統一38px超大字號'
            header_note = '✅ 標題、表頭、正文、數據全部統一38px，清晰醒目'
            split_hint = '📸 多圖分段指南：如需截取多張圖片，可從此處分割，上下兩部分各取所需，大字體完整保留。'
            remarks_title = '📌 數據說明'
            remarks_data_source = '• 數據來源：原始Excel數據完整生成'
            remarks_time = '• 時間格式：統一採用24小時制顯示'
            remarks_note1 = '• 空白單元格表示當日無相關數據/事件'
            remarks_note2 = '• 數據/事件按時間順序橫向排列'
            remarks_note3 = '• 重要數據/事件已突出顯示'
            footer_text = '✨ 全38px統一超大字號 · 微軟雅黑 · 橫版國家行 · 完整經濟數據日程 ✨' if data_type == 'DATA' else '✨ 全球財經日程 · 全篇統一38px微軟雅黑 · 每行獨立配色 · 事件橫向排 · 清晰極簡 ✨'
            empty_cell = '—'
            week_days = ['週一', '週二', '週三', '週四', '週五']
            col_country = '🌍 國家 / 地區'
            countries = ['中國', '歐元區', '美國', '法國', '英國']
            col_date = '日期'
            col_country_name = '國家'
            col_time = '時間'
            col_data_name = '數據類型'
            col_event_content = '事件內容'
            col_people = '人物'
        
        date_range = f'{week_dates_mon_to_fri[0]}—{week_dates_mon_to_fri[-1]}' if len(week_dates_mon_to_fri) > 1 else week_dates_mon_to_fri[0]
        
        header_dates = []
        for i, dt in enumerate(week_dates_mon_to_fri[:5]):
            dt_str = str(dt)
            month = int(dt_str[4:6])
            day = int(dt_str[6:8])
            header_dates.append(f'{month}月{day}日<br>{week_days[i]}')
        # 直接生成表头HTML
        header_html = ''.join([f'<th>{hd}</th>' for hd in header_dates])
        
        def extract_country(name_str):
            country_list = ['中国', '美国', '欧元区', '法国', '英国', '日本', '加拿大', '澳大利亚', '德国',
                           '中國', '美國', '歐元區', '法國', '英國', '日本', '加拿大', '澳大利亞', '德國']
            if not isinstance(name_str, str):
                return None
            for country in country_list:
                if country in name_str:
                    return country
            return None
        
        grouped_data = {}
        for _, row in data_df.iterrows():
            date = row[col_date] if col_date in data_df.columns else row.get('date', '')
            date_str = str(date) if not pd.isna(date) else ''
            if date_str not in week_dates_set:
                continue
            
            country = row[col_country_name] if col_country_name in data_df.columns and not pd.isna(row[col_country_name]) else row.get('country', '')
            if pd.isna(country) or country == '':
                if data_type == 'DATA':
                    name_col = col_data_name if col_data_name in data_df.columns else 'name'
                else:
                    name_col = col_event_content if col_event_content in data_df.columns else 'event_content'
                country = extract_country(row.get(name_col, ''))
            
            if country is None or country == '':
                continue
            
            time_val = row[col_time] if col_time in data_df.columns else row.get('time', '')
            
            if data_type == 'DATA':
                data_name = row[col_data_name] if col_data_name in data_df.columns else row.get('name', '')
                key = (country, date_str)
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append({'time': time_val, 'name': data_name})
            else:
                people = row[col_people] if col_people in data_df.columns else ''
                event_content = row[col_event_content] if col_event_content in data_df.columns else row.get('event_content', '')
                key = (country, date_str)
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append({'time': time_val, 'people': people, 'content': event_content})
        
        table_rows = ''
        for country in countries:
            row_class = row_styles.get(country, 'row-china')
            row_html = f'<tr class="{row_class}">'
            row_html += f'<td>{country}</td>'
            
            for dt in week_dates_mon_to_fri[:5]:
                cell_contents = []
                key = (country, dt)
                if key in grouped_data:
                    for item in grouped_data[key]:
                        if data_type == 'DATA':
                            time = item.get('time', '')
                            name = item.get('name', '')
                            cell_contents.append(f'<div class="data-item"><span class="data-time">{time}</span><span class="data-content">{name}</span></div>')
                        else:
                            time = item.get('time', '')
                            people = item.get('people', '')
                            content = item.get('content', '')
                            display_text = f'{people} · {content}' if people else content
                            cell_contents.append(f'<div class="event-item"><span class="event-time">{time}</span><span class="event-desc">{display_text}</span></div>')
                
                if cell_contents:
                    row_html += f'<td>{"<br>".join(cell_contents)}</td>'
                else:
                    row_html += f'<td><span class="empty-cell">{empty_cell}</span></td>'
            
            row_html += '</tr>'
            table_rows += row_html
        
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'sqlite', 'future_data_event_template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        html = html.format(
            title=title,
            subtitle=subtitle,
            date_range=date_range,
            header_note=header_note,
            col_country=col_country,
            header_html=header_html,
            table_rows=table_rows,
            split_hint=split_hint,
            remarks_title=remarks_title,
            remarks_data_source=remarks_data_source,
            remarks_time=remarks_time,
            remarks_note1=remarks_note1,
            remarks_note2=remarks_note2,
            remarks_note3=remarks_note3,
            footer_text=footer_text,
            data_type=data_type
        )
        return html


    @staticmethod
    def reformat_forex_trend_summary_data(data, str_data_date):
        """ 重构外汇行情趋势数据 """
        trend_data = pd.DataFrame([], columns=['期货', '代码', '合约到期月', '最新价', '周变动', '月变动'])

        trend_data['期货'] = data['TICKER'].apply(lambda x: x.replace('USD', ''))
        trend_data['代码'] = data['TICKER'].apply(lambda x: CloudhandsWeeklyReport.get_contract_symbol(x, str_data_date)[0])
        trend_data['合约到期月'] = data['TICKER'].apply(lambda x: CloudhandsWeeklyReport.get_contract_symbol(x, str_data_date)[1])
        trend_data['最新价'] = [x if t[:3] != 'USD' else round(1. / x, 5) for x, t in zip(data['LAST'], data['TICKER'])]
        trend_data['周变动'] = ['{:.2f}%'.format(x if t[:3] != 'USD' else -x) for x, t in zip(data['1W CHG %'],
                                                                                             data['TICKER'])]
        trend_data['月变动'] = ['{:.2f}%'.format(x if t[:3] != 'USD' else -x) for x, t in zip(data['1M CHG %'],
                                                                                                     data['TICKER'])]
        return trend_data

    @staticmethod
    def add_image_border(src, dst=None, loc='a', bw=3, bc=(0, 0, 0), dst_w=None):
        '''
        src: (str) 需要加边框的图片路径
        dst: (str) 加边框的图片保存路径
        loc: (str) 边框添加的位置, 默认是'a'(
            四周: 'a' or 'all'
            上: 't' or 'top'
            右: 'r' or 'rigth'
            下: 'b' or 'bottom'
            左: 'l' or 'left'
        )
        bw: border-width (int) 边框宽度 (默认是3)
        bc: border-color (int or 3-tuple) 边框颜色 (默认是0, 表示黑色; 也可以设置为三元组表示RGB颜色)
        dst_w: int 最终图片的宽度
        '''
        # 1.读取图片
        img_ori = Image.open(src)
        w, h = img_ori.size[0], img_ori.size[1]
        # 2.添加边框
        if loc in ['a', 'all']:
            w += 2 * bw
            h += 2 * bw
            img_new = Image.new('RGB', (w, h), bc)
            img_new.paste(img_ori, (bw, bw))
        elif loc in ['t', 'top']:
            h += bw
            img_new = Image.new('RGB', (w, h), bc)
            img_new.paste(img_ori, (0, bw, w, h))
        elif loc in ['r', 'right']:
            w += bw
            img_new = Image.new('RGB', (w, h), bc)
            img_new.paste(img_ori, (0, 0, w - bw, h))
        elif loc in ['b', 'bottom']:
            h += bw
            img_new = Image.new('RGB', (w, h), bc)
            img_new.paste(img_ori, (0, 0, w, h - bw))
        elif loc in ['l', 'left']:
            w += bw
            img_new = Image.new('RGB', (w, h), bc)
            img_new.paste(img_ori, (bw, 0, w, h))
        else:
            img_new = img_ori
        # 3.resize
        if dst_w is not None:
            img_new = img_new.resize((dst_w, int(h * dst_w/w)))
        # 4.保存图片
        if dst:
            img_new.save(dst)
        return img_new



    def get_fx678_weekly_report(self):
        """ 获取Dict格式的 fx678_weekly_report """
        href = self.get_fx678_weekly_report_href()
        if href:
            url = 'https://news.fx678.com{}'.format(href)
            headers = self.fx678_headers
            resp = requests.get(url, headers=headers)
            bs_resp = BeautifulSoup(resp.text)
            article_cont = bs_resp.select('div.article-cont')[0]
            article_dict = {}
            # 获取Title
            title = article_cont.select('h1')[0].text
            article_dict['title'] = title
            # 获取Summary & 具体Topic Content
            content = article_cont.select('div.content')[0]
            curr_topic = 'summary'
            # 拆解Article Content中的标签，按每个h2标签为Key分成多条新闻
            for child in content.children:
                child_name = child.name
                if child_name == 'br':
                    continue
                elif child_name in ('h2', 'font'):
                    curr_topic = child.text
                else:
                    child_text = child.text if child_name is not None else child
                    if curr_topic not in article_dict:
                        article_dict[curr_topic] = []
                    article_dict[curr_topic].append(child_text)
            for k in article_dict.keys():
                if k != 'title':
                    article_dict[k] = ''.join(article_dict[k]).strip()

            return article_dict
        return {}

    def get_fx678_weekly_report_href(self):
        """ 获取汇通网的外汇周评文章dict """
        resp = requests.get(self.fx678_url, headers=self.fx678_headers)
        bs_resp = BeautifulSoup(resp.text)
        # 解析获取外汇周评的href
        news_items = bs_resp.select('div > ul > li.item > a')
        for item in news_items:
            if ('外汇周评' in item.text) or ('汇市周评' in item.text):
                href = item.attrs['href']
                return href
        return None

    def get_trading_view_trend_data_df(self, need_columns, filters):
        """ 获取Trading View的趋势数据 """
        # 2. 利用代理proxy获取数据
        url = 'https://scanner.tradingview.com/forex/scan'
        payload = {"filter": filters,
                   "options": {"lang": "en"},
                   "markets": ["forex"],
                   "symbols": {"query": {"types": ["forex"]}, "tickers": []},
                   "columns": need_columns,
                   "sort": {"sortBy": "forex_priority", "sortOrder": "asc"},
                   "range": [0, 150]}
        resp = requests.post(url, json=payload, proxies=self.proxies)
        resp_json = resp.json()
        df = pd.DataFrame([r['d'] for r in resp_json['data']], columns=need_columns)
        return df

    # def get_exchangerate_host_fx_data_df(self, base, out_curr, start_date, end_date):
    #     # api url for request
    #     url = 'https://api.exchangerate.host/timeseries?base={0}&start_date={1}&end_date={2}&symbols={3}'.format(base,start_date,end_date,out_curr)
    #     response = requests.get(url)
    #     # retrive response in json format
    #     data = response.json()
    #     data_df = pd.DataFrame(data['rates'])
    #     return data_df

    def get_apilayer_fx_data_df(self, base, out_curr, start_date, end_date):
        # api url for request
        url = f'https://api.apilayer.com/currency_data/timeframe?start_date={start_date}&end_date={end_date}&source={base}&currencies={out_curr}'
        headers = {"apikey":'VwKulne8n3atHyIcfTNaer25a5QOKk7L'}
        resp = requests.get(url, headers=headers)
        data = resp.json()
        data_df = pd.DataFrame(data['quotes'])
        return data_df

    def get_cftc_net_position_df(self):
        """ 爬取CFTC持仓报告 """
        url = 'https://www.cftc.gov/dea/options/financial_lof.htm'
        resp = requests.get(url)
        resp_text = resp.text
        """ 将CFRC持仓报告的原文TEXT结构化为DataFrame """
        data = resp_text.split(
            '\n-----------------------------------------------------------------------------------------------------------------------------------------------------------\r\n              ')
        # 生成 两层Column结构(category->position)的 DataFrame表头
        cats = [
            ['Dealer Intermidiate'] * 3 + ['Institutional'] * 3 + ['Leveraged Funds'] * 3 + ['Other Reportable'] * 3 + [
                'Nonreportable'] * 2,
            ['Long', 'Short', 'Spreading'] * 4 + ['Long', 'Short']]
        multi_cols = pd.MultiIndex.from_arrays(cats, names=('category', 'position'))

        # 解析各个货币对的【持仓变动数据】，并放在一个dict里
        panel_data = {}
        for d in data[1:]:
            temp = d.split('\n')
            #print(temp[7])
            #print(temp[10])
            final = [# 本周持仓情况（Positions行）
                        [float(x.replace(',', '').replace('.', '0')) for x in temp[7].strip().split()],
                     # 上周持仓情况（Changes from行）
                        [float(x.replace(',', '').replace('.', '0')) for x in temp[10].strip().split()]]
            final = pd.DataFrame(final, index=['this week', 'change from last week'])
            final.columns = multi_cols
            # key值（货币对名称）
            cat_name = temp[4].split(' -')[0]
            panel_data[cat_name] = final

        # dict中数据生成to_df
        need_curr_dict = {'EURO FX':                '欧元',
                          'JAPANESE YEN':           '日元',
                          # 'BRITISH POUND STERLING': '英镑',
                          'BRITISH POUND': '英镑',
                          'AUSTRALIAN DOLLAR':  '澳元',
                          'CANADIAN DOLLAR':    '加元',
                          'SWISS FRANC':        '瑞士法郎',
                          #'NEW ZEALAND DOLLAR': '纽元',
                          'NZ DOLLAR':          '纽元',
                          'MEXICAN PESO':       '墨西哥比索',
                          'BRAZILIAN REAL':     '巴西雷亚尔'}
        to_df = pd.DataFrame(index=sorted(need_curr_dict.keys()), columns=['货币', '上周净持仓', '本周净持仓', 'delta净持仓'])
        for key_curr in panel_data.keys():
            if key_curr in need_curr_dict:
                to_df['货币'][key_curr] = need_curr_dict[key_curr]
                # 根据Panel_data中的原始数据，计算并填入to_df
                tmp_data = panel_data[key_curr]
                total_long = 0
                total_short = 0
                total_change = 0
                for tc in ['Dealer Intermidiate', 'Institutional', 'Leveraged Funds', 'Other Reportable']:
                    total_long += tmp_data[tc]['Long']['this week'] + tmp_data[tc]['Spreading']['this week']
                    total_short += tmp_data[tc]['Short']['this week'] + tmp_data[tc]['Spreading']['this week']
                    total_change += tmp_data[tc]['Long']['change from last week'] - tmp_data[tc]['Short']['change from last week']
                net_position = total_long - total_short
                to_df['上周净持仓'][key_curr] = net_position - total_change
                to_df['本周净持仓'][key_curr] = net_position
                to_df['delta净持仓'][key_curr] = total_change

        # 获取报告日期, 并转化为【YYYY-mm-dd】的形式放在to_df中
        report_date = data[0].split('Combined Positions as of ')[-1].strip()
        month_map_dict = {'January': 'Jan',
                          'February': 'Feb',
                          'March': 'Mar',
                          'April': 'Apr',
                          'May': 'May',
                          'June': 'Jun',
                          'July': 'Jul',
                          'August': 'Aug',
                          'September': 'Sep',
                          'October': 'Oct',
                          'November': 'Nov',
                          'December': 'Dec',
                          }
        for month in month_map_dict:
            report_date = report_date.replace(month, month_map_dict[month])
        to_df['report_date'] = str(datetime.datetime.strptime(report_date, '%b %d, %Y').date())
        return to_df

    def get_fx168_trading_analysis_url(self):
        """ 获取FX168的【欧元、英镑、日元、澳元和黄金最新交易分析】 """
        url = 'https://app4.fx168api.com/news/searchNews.json?keyWord=%E6%AC%A7%E5%85%83%E3%80%81%E8%8B%B1%E9%95%91%E3%80%81%E6%97%A5%E5%85%83%E3%80%81%E6%BE%B3%E5%85%83%E5%92%8C%E9%BB%84%E9%87%91%E6%9C%80%E6%96%B0%E4%BA%A4%E6%98%93%E5%88%86%E6%9E%90&pageNo=1&pageSize=20'
        resp = requests.get(url)
        resp_dict = resp.json()
        # 解析获取【最新交易分析】href
        for item in resp_dict['data']['items']:
            news_url = item['newsUrl']
            return news_url

    def get_fx168_trading_analysis_dict(self, news_url):
        """ 获取Trading Analysis的内容dictionary"""
        # 代理访问news_url
        resp = requests.get(news_url, proxies=self.proxies)
        bs_resp = BeautifulSoup(resp.content.decode('utf-8'))

        # 解析bs_resp生成analysis_dict
        analysis_dict = {'欧元/美元': '',
                         '英镑/美元': '',
                         '美元/日元': '',
                         '澳元/美元': '',
                         '黄金': ''}
        #items = bs_resp.select('div.TRS_Editor > p[align="justify"]')
        items = bs_resp.select('div.centerarticle > p')
        text_lines = [i.text for i in items]
        # analysis_idxes = [所有currency名称的idx] + [总行数]
        analysis_idxes = [i for (i, text) in enumerate(text_lines) if text in analysis_dict] + [len(text_lines)]
        for idx1, idx2 in zip(analysis_idxes[:-1], analysis_idxes[1:]):
            tmp_lines = text_lines[idx1: idx2]
            curr_name = tmp_lines[0]
            curr_text = '\n'.join(tmp_lines[1:])
            analysis_dict[curr_name] = curr_text

        return analysis_dict

    def get_future_data_event_df(self, week_dates, data_type, level=3):
        """  """
        dfs = []
        for week_d in week_dates:
            df = self.get_jin10_financial_data_event_df(week_d, data_type)
            dfs.append(df)
        final_df = pd.concat(dfs).drop_duplicates()

        if data_type == 'data':
            final_df['date'] = final_df['pub_time'].apply(lambda x: (x[:10]).replace('-', ''))
            final_df['time'] = final_df['pub_time'].apply(lambda x: x[-13:-8])
            final_df = final_df[['date', 'time', 'country', 'star', 'time_period', 'name']]
        elif data_type == 'event':
            final_df['date'] = final_df['event_time'].apply(lambda x: str(x)[:10].replace('-', ''))
            final_df['time'] = final_df['event_time'].apply(lambda x: x[-13:-8])
            final_df['event_content'] = final_df['event_content'].apply(lambda x: x.replace('。',''))
            final_df = final_df[['date', 'time', 'country', 'star', 'region', 'people', 'event_content']]
        if level:
            final_df = final_df[final_df['star'] >= level]
        return final_df

    def get_future_data_event_df_selenium(self, week_dates):
        all_data_sources, all_event_sources = self.get_jin10_financial_data_event_sources_selenium(week_dates)
        # 5. 解析页面数据
        result_data = []  # 存储财经数据
        for date_str, page_source in zip(week_dates, all_data_sources):
            soup = BeautifulSoup(page_source, 'html.parser')
            # 爬取财经数据（jinTable1）
            for row in soup.select("#jinTable1 > div.jin-table-body__wrapper > div > div > div > div.jin-table-row"):
                content = row.get_text(strip=True, separator='|')
                result_data.append(f"{date_str}|{content}")
        print(result_data)
        # 6. 处理财经数据
        new_result_data = []
        ts = ''  # 用于处理时间连续的情况
        for r in result_data:
            items = r.split('|')
            if len(items) == 9:
                if items[-5] != '视频解读': # 如果没有视频解读，就加上"视频解读"
                    items = items[:len(items) - 4] + ['视频解读'] + items[-4:]
            # 确定最新一条数据的时间
            if len(items) == 10:
                ts = items[1]
            elif len(items) < 10:
                items = items[:1] + [ts] + items[1:]
            new_result_data.append('|'.join(items))
        data_df = pd.DataFrame([r.split('|')[:3] for r in new_result_data], columns=['date', 'time', 'name'])
        # 为data_df添加缺失列
        data_df_columns = ['date', 'time', 'country', 'star', 'time_period', 'name']
        for col in data_df_columns:
            if col not in data_df.columns:
                data_df[col] = ''
        data_df = data_df[data_df_columns]  # 调整列顺序

        result_event = []  # 存储财经事件
        for date_str, page_source in zip(week_dates, all_event_sources):
            soup = BeautifulSoup(page_source, 'html.parser')
            # 爬取财经事件（jinTable2）
            for row in soup.select("#jinTable2 > div.jin-table-body__wrapper > div > div.jin-table-row__group"):
                content = row.get_text(strip=True, separator='|')
                result_event.append(f"{date_str}|{content}")
        # 7. 处理财经事件
        event_records = []
        for r in result_event:
            items = r.split('|')
            if len(items) >= 10:  # 异常数据
                continue
            elif len(items) >= 3:
                date = items[0]
                ts = items[1]
                # 提取国家、星级、区域、人物、事件内容等信息
                country = items[2] if len(items) > 2 else ''
                star = len([c for c in items[2] if c == '★']) if len(items) > 2 else 0
                event_content = items[3] if len(items) > 3 else ''
                people = items[5] if len(items) > 4 else ''
                region = ''
                event_records.append({
                    'date': date,
                    'time': ts,
                    'country': country,
                    'star': star,
                    'region': region,
                    'people': people,
                    'event_content': event_content.replace('。', '')
                })
        event_df = pd.DataFrame(event_records)
        # 为event_df添加缺失列
        event_df_columns = ['date', 'time', 'country', 'star', 'region', 'people', 'event_content']
        for col in event_df_columns:
            if col not in event_df.columns:
                event_df[col] = ''
        event_df = event_df[event_df_columns]  # 调整列顺序
        return data_df, event_df

    @staticmethod
    def get_jin10_financial_data_event_df(date, data_type):
        """ 爬取金十数据的【财经数据与事件】 """
        if data_type == 'event':
            url = 'https://cdn-rili.jin10.com/data/{}/{}/event.json?'.format(date[:4], date[4:])
        elif data_type == 'data':
            url = 'https://cdn-rili.jin10.com/data/{}/{}/economics.json?'.format(date[:4], date[4:])
        resp = requests.get(url)
        resp_df = pd.DataFrame(resp.json())
        return resp_df

    @staticmethod
    def get_jin10_financial_data_event_sources_selenium(week_dates):
        """ 使用Selenium爬取金十数据日历，获取财经数据和事件
        参数:
            week_dates: 日期列表，格式如 ['20260209', '20260210', ...]
        返回:
            data_df: 财经数据DataFrame
            event_df: 财经事件DataFrame
        """
        # 1. 配置Chrome浏览器选项, 可以根据需要添加无头模式等选项
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--disable-gpu")

        # 2. 初始化浏览器驱动
        driver_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options
        )

        first_date = week_dates[0]
        url = f"https://rili.jin10.com/day/{first_date[:4]}-{first_date[4:6]}-{first_date[6:]}"
        driver.get(url)
        input('按Enter键继续爬取')

        # 3. 爬取每个日期的财经数据
        all_data_sources = []
        countdown_text = ''  # 多久公布下一跳数据，用于侧面监测切换到新的日期页面了
        weekday_btns = driver.find_elements(By.CSS_SELECTOR, "div.date-slider > ul > li")
        for i, btn in enumerate(weekday_btns[:5]):
            print(i + 1)
            btn.click()
            while True:
                time.sleep(3)
                countdown_items = driver.find_elements(By.CSS_SELECTOR,"div.countdown-line")
                if len(countdown_items)>0:
                    new_countdown_text = countdown_items[0].text
                else:
                    new_countdown_text = 'no data'
                if countdown_text != new_countdown_text:
                    all_data_sources.append(driver.page_source)
                    countdown_text = new_countdown_text
                    break
        print(f"共爬取到{len(all_data_sources)}天的数据")
        # 切换到【大事】Tab
        elements = driver.find_elements(By.CSS_SELECTOR,
                                        "div.index-page-header > div.index-page-header__left > div > div")
        # target_element = elements[1]
        target_element = next((el for el in elements if "大事" in el.text), None)
        target_element.click()
        time.sleep(3)
        # 4.爬取每个日期的财经事件
        all_event_sources = []
        countdown_text = ''  # 多久公布下一跳数据，用于侧面监测切换到新的日期页面了
        weekday_btns = driver.find_elements(By.CSS_SELECTOR, "div.date-slider > ul > li")
        for i, btn in enumerate(weekday_btns[:5]):
            print(i + 1)
            btn.click()
            while True:
                time.sleep(3)
                countdown_items = driver.find_elements(By.CSS_SELECTOR, "div.countdown-line")
                if len(countdown_items)>0:
                    new_countdown_text = countdown_items[0].text
                else:
                    new_countdown_text = 'no data'
                if countdown_text != new_countdown_text or new_countdown_text == 'no data':
                    all_event_sources.append(driver.page_source)
                    countdown_text = new_countdown_text
                    break
        print(f"共爬取到{len(all_event_sources)}天的数据")

        driver.quit()
        return all_data_sources, all_event_sources

    def filter_jin10_financial_data_df(self, data_df):
        """ 按照列表筛取金十财经数据，避免数量过多 """
        filter_file_path = os.path.join(self.meta_data_dir, self.jin10_data_filter_file)
        if os.path.exists(filter_file_path):
            filter_df = pd.read_excel(filter_file_path)
            q_data_names = set(filter_df[filter_df['is_store'] == 'Y']['数据类型'])
            # data_df = data_df[data_df['name'].isin(q_data_names)]
            data_df = data_df[data_df['name'].apply(lambda x: any(q in x for q in q_data_names))]
        return data_df

    def get_text_from_forex_position(self, data_df):
        """ 解析ForexPosition DataFrame，获取总结文本 """
        # begin
        report_date = data_df['report_date'].tolist()[0]
        text1 = '据美国商品期货委员会公布的{}期货市场头寸持仓报告显示，上周各货币的报告总持仓情况如下：'.format(report_date)
        # 持仓变动情况
        text2 = ''
        for curr, curr_chg in zip(data_df['货币'], data_df['delta净持仓']):
            direction = '净空头' if curr_chg < 0 else '净多头'
            chg_amt = '{}手'.format(abs(int(curr_chg)))
            text2 += '{}{}变化{}，'.format(curr, direction, chg_amt)
        # 多空转换
        trans_df = data_df[data_df['本周净持仓']*data_df['上周净持仓'] <= 0]
        if len(trans_df) == 0:
            text3 = '上周没有总持仓多空转换的货币。'
        else:
            text3 = '上周总持仓多空转换的货币有：{}。'.format('，'.join(trans_df['货币']))
        # 变动超20%
        chg_over20_df = data_df[data_df['delta净持仓']/data_df['上周净持仓'] >= 0.2]
        if len(chg_over20_df) == 0:
            text4 = '没有单向总持仓变动超过20%的货币。'
        else:
            text4 = '除此之外，单向总持仓变动超过20%的货币有：{}。'.format('，'.join(chg_over20_df['货币']))

        text = text1 + text2 + text3 + text4
        return text

    def get_picture_from_forex_position(self, data_df):
        """ 解析ForexPosition DataFrame，保存成图片 """
        (curr, last_v, curr_v) = data_df.columns[:3]
        labels = data_df[curr].tolist()
        position_last_wk = data_df[last_v].astype(int)
        position_this_wk = data_df[curr_v].astype(int)
        title = '截至上周二（{}）CFTC各货币期货净持仓变化'.format(data_df['report_date'][0])
        ylabel = '持仓数（万手）'
        if curr != converter_t2s.convert(curr):  # 不是简体中文
            title = converter_s2t.convert(title)
            ylabel = converter_s2t.convert(ylabel)

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        # Construct Subplot
        fig, ax = plt.subplots(figsize=(12, 6))
        # Plot Bar
        rects1 = ax.bar(x - width / 2, position_last_wk, width, label=position_last_wk.name)
        rects2 = ax.bar(x + width / 2, position_this_wk, width, label=position_this_wk.name)
        # Add title
        ax.set_title(title, fontsize=20)
        # Add Axis Labels
        ax.set_ylabel(ylabel, fontsize=20)
        # Add custom Axis-Tick Labels, etc.
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(15)
        # Add Legend
        ax.legend(fontsize=15)
        # Add Annotate Labels
        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                offset = 3 if height >= 0 else -15
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, offset),  # 3 or -3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=14)
        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        return fig, ax

    def get_file_path(self, file_name):
        """ 获取output file的完整路径 """
        # 如果是output_File，要映射成完整文件名再判断
        if file_name in self.weekly_report_output:
            file_name = self.weekly_report_output[file_name]
        # 判断文件是否存在
        if os.path.exists(os.path.join(self.output_file_dir, file_name)):
            res = {
                'file_dir':  self.output_file_dir,
                'file_name': file_name
            }
            return res
        else:
            return None

    def delete_doc(self, doc_dir):
        """ 删除 docxtpl 的 genpy文件夹 """
        return True

if __name__ == '__main__':
    str_date = '2026-5-18'  # 使用现有数据目录的日期
    print(str_date)
    report_generator = CloudhandsWeeklyReport(str_date)

    # report_generator.crawl_forex_trend_summary()
    # report_generator.generate_forex_trend_summary()

    # report_generator.crawl_forex_position_data()
    # report_generator.generate_forex_position_data()
    
    # 测试新函数
    print("开始测试新的图表生成函数...")
    result = report_generator.generate_forex_position_data_new()
    print("新图表生成完成！")
    print(f"生成的图片名称: {result['picture_name']}")

    # report_generator.generate_major_currency_forecast()

    # #report_generator.crawl_forex_future_data_event()
    # report_generator.generate_forex_future_data_event('DATA')
    # report_generator.generate_forex_future_data_event('EVENT')

    # report_generator.generate_output_files()