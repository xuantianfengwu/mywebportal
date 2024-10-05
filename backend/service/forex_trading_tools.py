#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..utils.sqlite_utils import SqliteUtils
from ..utils.osfile_utils import OSFileUtils
import os
import numpy as np
import pandas as pd
import time

class ForexTradingTools(object):
    """ 外汇交易相关服务类 """
    def __init__(self):
        self.sqlite_name = 'forextrading'
        self.sqlite_db = SqliteUtils(self.sqlite_name)
        self.symbol_list = ['EURUSD', 'GBPUSD', 'AUDUSD', 'USDJPY', 'USDCAD', 'USDCHF']

    def initialize_sqlite_db(self, replace=False):
        """ 根据sqlite文件夹里的Excel批量生成每个Symbol的表 """
        if not replace and os.path.exists(self.sqlite_db.db_path):
            return False
        else:
            # excel_path = os.path.join('..', '..', 'sqlite', '{}.xlsx'.format(self.sqlite_name))
            # for tab in ['forex_tester_raw_data', 'history_price', 'history_indicator']:
            #     table_df = pd.read_excel(excel_path, tab, header=None)
            #     table_info = {
            #         'column_names': table_df.iloc[0].tolist(),
            #         'column_types': table_df.iloc[1].tolist()
            #     }
            #     table_info_dict = {
            #         '{}_{}'.format(symbol, tab): table_info.copy()
            #         for symbol in self.symbol_list
            #     }
            #     self.sqlite_db.initialize_sqlite_from_table_info_dict(table_info_dict)
            return True

    def import_forex_tester_data(self, file_path, to_table, row_freq=100000, overwrite=False):
        """
            读取从Forex Tester下载的数据，导入数据库: https://forextester.com/data/datasources
        """
        filename = os.path.basename(file_path)
        symbol = filename.split('.')[0]

        file_row_cnt = OSFileUtils(file_path).get_big_file_row_cnt()
        print('{}文件共有{}行'.format(filename, file_row_cnt))
        with open(file_path, 'r') as f:
            first_line = f.readline().rstrip()
            # 检查表头是否符合Forex Tester下载文件的格式
            if first_line == '<TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>':
                data_columns = ['TICKER', 'DTYYYYMMDD', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
                print('开始读取文件并插入数据库')
                start = time.time()
                value_rows = []
                for i, l in enumerate(f):
                    value_row = l.rstrip().split(',')
                    value_rows.append(value_row)
                    if ((i+1) % row_freq == 0) or (i == file_row_cnt-2):
                        db_table = '{}_{}'.format(symbol, to_table)
                        self.sqlite_db.insert_value_rows(db_table, data_columns, value_rows)
                        print('Insert Progress: {}/{} | {:.2f}s'.format(i+1, file_row_cnt-1, time.time()-start))
                        value_rows = []
                print('Finish Data Import of {}'.format(symbol))
                return True
            else:
                print('文件列头不符合预期，跳出~')
                return False

    def update_forex_data(self, data):
        res = {
            'is_success': True
        }
        return res

    def save_upload_file(self, f):
        """ 将上传的Data File保存下来，以便进行处理 """
        upload_file_path = os.path.join(".", "backend", "static", "upload", "trading", "forex", f.filename)
        osfile_util = OSFileUtils(upload_file_path)
        osfile_util.save_file(f)
        return upload_file_path

    def get_symbol_list(self):
        return self.symbol_list
