#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd
import numpy as np
import json

import requests
from bs4 import BeautifulSoup

from docxtpl import DocxTemplate, InlineImage
# for height and width you have to use millimeters (Mm), inches or points(Pt) class :
from docx.shared import Pt
from PIL import Image

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from ..utils.osfile_utils import OSFileUtils
from ..utils.docx_utils import DocxUtils

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
        # 3.爬取ForexPositionSummary【期货市场头寸分析】的Url
        self.display_curr_order = ['欧元', '澳元', '英镑', '日元', '加元', '纽元']
        self.cftc_net_position_file = 'cftc_net_position.csv'
        self.cftc_net_position_pic = 'cftc_net_position.png'
        # 4.爬取MajorCurrencyForecast【重点货币对展望】的Url
        self.major_currency_forecast_file = 'major_curr_forecast.json'
        # 5.爬取FutureDataEvent【后市观察指标】的Url
        self.jin10_data_filter_file = 'jin10_financial_data_list.xlsx'
        self.forex_future_data_event_file = 'future_data_event.xlsx'
        self.future_data_event_data_types = {'DATA': 'DATA.png', 'EVENT': 'EVENT.png'}
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
            forex_trend_date = self._forex_trend_dates
            m_start_date = forex_trend_date['l_mstart_dt']
            w_start_date = forex_trend_date['l_wstart_dt']
            end_date = forex_trend_date['l_wend_dt']

            data_df = pd.concat([
                self.get_exchangerate_host_fx_data_df('EUR', 'USD', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('USD', 'JPY', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('GBP', 'USD', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('AUD', 'USD', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('USD', 'CAD', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('USD', 'CHF', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('NZD', 'USD', m_start_date, end_date),
                self.get_exchangerate_host_fx_data_df('USD', 'CNY', m_start_date, end_date),
            ], axis=0)
            data_df['TICKER'] = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD',
                                 'USDCAD', 'USDCHF', 'NZDUSD', 'USDCNY']
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
        data_df = self.get_future_data_event_df(week_dates, 'data', 3)
        event_df = self.get_future_data_event_df(week_dates, 'event', 3)
        # 筛取一部分财经数据，避免数量过多
        print('Start Filter Necessary Financial Data...')
        data_df = self.filter_jin10_financial_data_df(data_df)
        # 保存Excel
        print('Start Save Data To Excel...')
        writer = pd.ExcelWriter(os.path.join(self.crawl_file_dir, self.forex_future_data_event_file))
        data_df.to_excel(writer, 'DATA', index=False)
        event_df.to_excel(writer, 'EVENT', index=False)
        writer.save()
        return True


    def generate_fundamental_event_data(self):
        data_df = pd.read_csv(os.path.join(self.crawl_file_dir, self.fund_event_summary_file))
        res = {'data_lst': data_df.to_dict(orient='records')}
        return res

    def generate_forex_trend_summary(self):
        """ 生成 外汇期货合约 数据 """
        # 读取文件
        forex_trend_summary_data = pd.read_csv(os.path.join(self.crawl_file_dir, self.forex_trend_summary_file))
        # 处理文件
        trend_data = self.reformat_forex_trend_summary_data(forex_trend_summary_data, self.week_start)
        # 渲染图片并保存
        fig, ax = self.render_forex_trend_table(trend_data, cellLoc='left',
                                               col_width=1.2, row_height=0.4, row_colors=['lightblue', 'w'],
                                               dynamic_num_color_cols=[4, 5])
        image_path = os.path.join(self.output_file_dir, self.forex_trend_summary_pic)
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)
        # 返回结果
        res = {
            #'data_json_lst': forex_trend_summary_data.to_dict(orient='records'),
            'image_name':    self.forex_trend_summary_pic,
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
        image_path = os.path.join(self.output_file_dir, '{}.png'.format(data_type))
        fig.savefig(image_path)
        self.add_image_border(image_path, image_path, bc=(0, 100, 255), dst_w=960)

        res = {
            'data_json_lst': data_json_lst,
            'image_name': '{}.png'.format(data_type),
        }
        return res


    def generate_output_files(self,  report_title, report_summary,
                                     fundamental_events,
                                     trend_image_src,
                                     position_summary_data,
                                     curr_forecasts,
                                     strategy_info,
                                     data_image_src, event_image_src):
        """ 生成周报结果文件 """
        # 加载周报模板
        word_tpl_path = os.path.join(self.meta_data_dir, "Cloudhands Report Demo.docx")
        tpl = DocxTemplate(word_tpl_path)
        # 拼接图片path
        forex_trend_summary_png_path = os.path.join(self.output_file_dir, self.forex_trend_summary_pic)
        cftc_net_position_png_path = os.path.join(self.output_file_dir, self.cftc_net_position_pic)
        future_data_png_path = os.path.join(self.output_file_dir, self.future_data_event_data_types['DATA'])
        future_event_png_path = os.path.join(self.output_file_dir, self.future_data_event_data_types['EVENT'])
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
        # 生成结果Word
        tpl.save(os.path.join(self.output_file_dir, self.weekly_report_output['docx-jt']))
        # 简体转繁体
        DocxUtils().translate_to_traditional(os.path.join(self.output_file_dir, self.weekly_report_output['docx-jt']),
                                             os.path.join(self.output_file_dir, self.weekly_report_output['docx-ft'])
                                             )
        # 结果Wrod转PDF
        DocxUtils().docx_to_pdf(os.path.join(self.output_file_dir, self.weekly_report_output['docx-jt']),
                                os.path.join(self.output_file_dir, self.weekly_report_output['pdf-jt'])
                                )
        DocxUtils().docx_to_pdf(os.path.join(self.output_file_dir, self.weekly_report_output['docx-ft']),
                                os.path.join(self.output_file_dir, self.weekly_report_output['pdf-ft'])
                                )
        return True

    @staticmethod
    def get_pic_height_blank_row_amt(pic_path, resize_width=400, blank_row_height=16):
        """ 获取图片按照宽度resize后的高度，需要多少空行 """
        im = Image.open(pic_path)
        resize_height = resize_width * im.size[1] / im.size[0]
        # -2因为模板里本来就有两个空行
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
                #print(k)
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

        # 12-3:'H' 3-6:'M' 6-9:'U' 9-12:'Z'
        dt_data_date = datetime.datetime.strptime(str_data_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        month_day_one = dt_data_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # 当月第一天
        week_num = int(dt_data_date.strftime('%W')) - int(month_day_one.strftime('%W')) + 1  # 当前日期处于本月第几周
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
        # 1. 从Vultr服务器获取数据
        """
        # Config加载url
        cf = configparser.ConfigParser()
        cf.read(os.path.join('.', 'backend', 'config', 'oversea_vps.ini'))
        url = "http://{}:{}/data/trading_view".format(cf.get("vultr_jp_vps", "host"), cf.get("vultr_jp_vps", "port"))
        # 根据fiters和need_columns拉取数据
        data = {
            'filters': str(filters),
            'columns': str(need_columns)
        }
        resp = requests.post(url, data=data)
        resp_json = resp.json()
        df = pd.DataFrame([r['d'] for r in resp_json['data']], columns=need_columns)
        
        """
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

    def get_exchangerate_host_fx_data_df(self, base, out_curr, start_date, end_date):
        # api url for request
        url = 'https://api.exchangerate.host/timeseries?base={0}&start_date={1}&end_date={2}&symbols={3}'.format(base,start_date,end_date,out_curr)
        response = requests.get(url)
        # retrive response in json format
        data = response.json()
        data_df = pd.DataFrame(data['rates'])
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

    def get_jin10_financial_data_event_df(self, date, data_type):
        """ 爬取金十数据的【财经数据与事件】 """
        if data_type == 'event':
            url = 'https://cdn-rili.jin10.com/data/{}/{}/event.json?'.format(date[:4], date[4:])
        elif data_type == 'data':
            url = 'https://cdn-rili.jin10.com/data/{}/{}/economics.json?'.format(date[:4], date[4:])
        resp = requests.get(url)
        resp_df = pd.DataFrame(resp.json())
        return resp_df


    def filter_jin10_financial_data_df(self, data_df):
        """ 按照列表筛取金十财经数据，避免数量过多 """
        if os.path.exists(os.path.join(self.meta_data_dir, self.jin10_data_filter_file)):
            filter_df = pd.read_excel(os.path.join(self.meta_data_dir, self.jin10_data_filter_file))
            q_data_names = set(filter_df[filter_df['is_store'] == 'Y']['数据类型'])
            data_df = data_df[data_df['name'].isin(q_data_names)]
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
        labels = data_df['货币'].tolist()
        position_last_wk = data_df['上周净持仓'].astype(int)
        position_this_wk = data_df['本周净持仓'].astype(int)
        title = '截至上周二（{}）CFTC各货币期货净持仓变化'.format(data_df['report_date'][0])

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
        ax.set_ylabel('持仓数（万手）', fontsize=20)
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
    str_date = str(datetime.datetime.now())[:10]
    print(str_date)
    report_generator = CloudhandsWeeklyReport(str_date)

    # report_generator.generate_forex_trend_summary()

    report_generator.crawl_forex_trend_summary()

    # report_generator.crawl_forex_position_data()
    # report_generator.generate_forex_position_data()

    # report_generator.generate_major_currency_forecast()

    # #report_generator.crawl_forex_future_data_event()
    # report_generator.generate_forex_future_data_event('DATA')
    # report_generator.generate_forex_future_data_event('EVENT')

    # report_generator.generate_output_files()
