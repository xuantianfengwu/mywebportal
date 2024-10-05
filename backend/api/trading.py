#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, session, request
import flask
trading_bp = Blueprint('trading', __name__)

import json
import platform
from ..utils.web_response import WebResponse
from ..service.forex_trading_tools import ForexTradingTools
# 只有Windows可用周报编写部分（要操作生成Word）
sys = platform.system()
if sys.lower()=='windows':
    from ..service.cloudhands_weekly_report import CloudhandsWeeklyReport

@trading_bp.route('/forex/data/save', methods=['GET','POST'])
def save_forex_data():
    """ 将外汇行情通过Params传入，并保存在数据库 """
    # 解析参数
    data = json.loads(request.data)
    # 执行
    return WebResponse.success('上传成功！')

@trading_bp.route('/forex/file/upload', methods=['POST'])
def upload_forex_tester_file():
    """ 上传Forex Tester的文件，导入数据库 """
    # 解析参数
    file_type = request.form['file_type']
    f = request.files['file']
    # 执行
    print('开始上传文件...')
    file_path = ForexTradingTools().save_upload_file(f)
    print('文件已上传，开始导入数据库')
    if file_type == 'forex_tester':
        upload_res = ForexTradingTools().import_forex_tester_data(file_path, to_table='forex_tester_raw_data')
        if upload_res:
            return WebResponse.success('文件导入成功！')
        else:
            return WebResponse.fail('文件导入失败！')
    else:
        return WebResponse.fail('导入文件格式异常~')

@trading_bp.route('/forex/db/initialize')
def initialize_forex_db():
    """ 初始化外汇数据库表 """
    res = ForexTradingTools().initialize_sqlite_db()
    if res:
        return WebResponse.success('数据库初始化成功!')
    else:
        return WebResponse.fail('数据库已存在!')

@trading_bp.route('/cloudhands/crawl')
def crawl_cloudhands_data():
    """ 下载云核变量相关数据 """
    # 解析参数
    data_type = request.args['data_type']
    week_start = request.args['week_start']
    # 进行爬取
    if data_type == 'fundamental_event_summary':
        CloudhandsWeeklyReport(week_start).crawl_fundamental_event_summary()
    elif data_type == 'forex_trend_summary':
        CloudhandsWeeklyReport(week_start).crawl_forex_trend_summary()
    elif data_type == 'forex_position_data':
        CloudhandsWeeklyReport(week_start).crawl_forex_position_data()
    elif data_type == 'major_currency_forecast':
        CloudhandsWeeklyReport(week_start).crawl_major_currency_forecast()
    elif data_type == 'option_strategy':
        CloudhandsWeeklyReport(week_start).crawl_option_strategy()
    elif data_type == 'forex_future_data_event':
        CloudhandsWeeklyReport(week_start).crawl_forex_future_data_event()
    return WebResponse.success('数据爬取成功！')

@trading_bp.route('/cloudhands/forex/fund_event')
def get_cloudhands_fund_event_data():
    # 解析参数
    week_start = request.args['week_start']
    # 执行
    data = CloudhandsWeeklyReport(week_start).generate_fundamental_event_data()
    resp = WebResponse.success('获取数据成功！', data=data)
    return resp

@trading_bp.route('/cloudhands/forex/trend_summary')
def get_cloudhands_forex_trend_summary():
    """ 获取Forex Trend Summary数据 """
    # 解析参数
    week_start = request.args['week_start']
    # 执行
    data = CloudhandsWeeklyReport(week_start).generate_forex_trend_summary()
    resp = WebResponse.success('获取数据成功！', data=data)
    return resp

@trading_bp.route('/cloudhands/forex/position_data')
def get_cloudhands_forex_position_data():
    """ 获取ForexPositionData部分的数据 """
    # 解析参数
    week_start = request.args['week_start']
    # 获取数据
    data_lst = CloudhandsWeeklyReport(week_start).generate_forex_position_data()
    resp = WebResponse.success('获取数据成功！', data=data_lst)
    return resp

@trading_bp.route('/cloudhands/forex/major_currency_forecast')
def get_cloudhands_major_currency_forecast():
    """ 获取 Major_Currency_Forecast 部分的数据 """
    # 解析参数
    week_start = request.args['week_start']
    # 获取数据
    data_lst = CloudhandsWeeklyReport(week_start).generate_major_currency_forecast()
    resp = WebResponse.success('获取数据成功！', data=data_lst)
    return resp

@trading_bp.route('/cloudhands/forex/future_data_event')
def get_cloudhands_forex_future_data_event():
    """ 获取Forex_Future_Data_Event部分的数据 """
    # 解析参数
    data_type = request.args['data_type']
    week_start = request.args['week_start']
    # 获取数据
    res = CloudhandsWeeklyReport(week_start).generate_forex_future_data_event(data_type)
    resp = WebResponse.success('获取数据成功！', data=res)
    return resp

@trading_bp.route('/cloudhands/forex/output_report', methods=['POST'])
def generate_cloudhands_output_file():
    """ 生成周报文件以供下载 """
    # 解析参数
    report_title = request.form.get('report_title')
    report_summary = request.form.get('report_summary')
    fundamental_events = eval(request.form.get('fundamental_events'))
    trend_image_src = request.form.get('trend_image_src')
    position_summary_data = eval(request.form.get('position_summary_data'))
    curr_forecasts = eval(request.form.get('curr_forecasts'))
    strategy_info = eval(request.form.get('strategy_info'))
    data_image_src = request.form.get('data_image_src')
    event_image_src = request.form.get('event_image_src')
    week_start = request.form.get('week_start')
    # 执行逻辑
    res = CloudhandsWeeklyReport(week_start).generate_output_files(  report_title, report_summary,
                                                                     fundamental_events,
                                                                     trend_image_src,
                                                                     position_summary_data,
                                                                     curr_forecasts,
                                                                     strategy_info,
                                                                     data_image_src, event_image_src)
    resp = WebResponse.success('获取数据成功！', data=res)
    return resp

@trading_bp.route('/cloudhands/file')
def get_cloudhands_file():
    """ 图片预览接口 """
    # 解析参数
    file_name = request.args['file_name']
    week_start = request.args['week_start']
    # 执行
    res = CloudhandsWeeklyReport(week_start).get_file_path(file_name)
    # 返回
    if res:
        """ as_attachment=False的时候，Chrome会新窗口浏览PDF，反之会直接下载；word不管as_attachment True/False都会下载 """
        return flask.send_from_directory(res['file_dir'], res['file_name'], as_attachment=True)
        # return flask.send_from_directory(res['file_dir'], res['file_name'])
    else:
        return WebResponse.fail('文件不存在！')

