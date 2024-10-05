#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import pandas as pd

class SqliteUtils(object):
    def __init__(self, db_path=None):
        """ SQLITE都存在db_dir下的sqlite文件夹 """
        self.db_path = db_path

    def __connect(self):
        """
            db_path确定，则进行连接；
            db_path为空，则报告异常
        """
        if self.db_path:
            return sqlite3.connect(self.db_path)
        else:
            print('初始化时未提供db_path～请使用update_db_path更新')
            return False

    def fetch_data_df(self, sql):
        """ 根据sql，获取结果数据，以DataFrame返回 """
        conn = self.__connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            columns = [c[0] for c in cursor.description]
            conn.close()
            data_df = pd.DataFrame(data, columns=columns)
            return data_df
        else:
            return None

    def get_tabs(self):
        """ 获取DB内所有Table的名称列表 """
        conn = self.__connect()
        if conn:
            sql = "SELECT name _id FROM sqlite_master WHERE type ='table';"
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            tab_names = [d[0] for d in data]
            return tab_names

    def get_tab_col_df(self, tab_name):
        """ 根据table_name，获取表的column信息，以DataFrame返回 """
        sql = 'pragma table_info({});'.format(tab_name)
        print(sql)
        conn = self.__connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            columns = [c[0] for c in cursor.description]
            data_df = pd.DataFrame(data, columns=columns)
            conn.close()
            return data_df

    def get_tab_col_lst(self, tab_name):
        sql = 'pragma table_info({});'.format(tab_name)
        print(sql)
        conn = self.__connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            columns = [l[1] for l in data]
            return columns

    def get_tab_data_df(self, table_name, data_cols=None, limit=None):
        """ 获取table_name中数据，以DataFrame返回， 可以限制limit和data_cols """
        if data_cols:   sql = 'select {} from {}'.format(','.join(data_cols), table_name)
        else:           sql = 'select * from {}'.format(table_name)
        print(sql)
        conn = self.__connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if limit:
                data = cursor.fetchall(limit)
            else:
                data = cursor.fetchall()
            columns = [c[0] for c in cursor.description]
            conn.close()
            data_df = pd.DataFrame(data, columns=columns)
            return data_df

    def update_db_path(self, db_path):
        self.db_path=db_path

    def create_tab_from_tab_info_dict(self, tab_info_dict):
        """
            根据传入的table_info_dict生成数据库
            table_info_dict : {
                column_names: string[]
                column_types: string[]
                data_df?:     Pandas.DataFrame
            }
        """
        conn = self.__connect()
        if conn:
            try:
                for tab_name, tab_info in tab_info_dict.items():
                    print("Table Name：", tab_name)
                    col_names, col_types = tab_info['column_names'], tab_info['column_types']
                    conn = self.create_table(conn, tab_name, col_names, col_types)
                    if 'data_df' in tab_info:
                        data_df = tab_info['data_df']
                        conn = self.insert_data_df(conn, tab_name, data_df)
                return True
            finally:
                conn.close()
        else:
            return False

    def create_tab(self, tab_name, col_names, col_types):
        """
            根据输入的Table信息，创建对应conn的数据表，默认删表重建
        """
        conn = self.__connect()
        if not conn:
            return False
        else:
            cursor = conn.cursor()
            cursor.execute("Drop table if exists {}".format(tab_name))
            col_info = ','.join(['{} {}'.format(col_name, col_type) for (col_name, col_type) in zip(col_names, col_types)])
            sql = 'CREATE TABLE {}({})'.format(tab_name, col_info)
            cursor.execute(sql)
            conn.commit()
            return True

    def insert_value_rows(self, tab_name, tab_cols, value_rows):
        """
            将value_rows插入到SQLITE表中，column_lst为对应列名
        """
        conn = self.__connect()
        if not conn:
            return False
        if len(value_rows)>0:
            cursor = conn.cursor()
            str_tab_cols = ",".join(tab_cols)
            str_value_rows = ",".join(["('{}')".format("','".join(value_row)) for value_row in value_rows])
            sql = "INSERT INTO {}({}) values {}".format(tab_name, str_tab_cols, str_value_rows)
            #print(sql)
            cursor.execute(sql)
            conn.commit()
        else:
            print('传入的value_rows为空，跳过插入')
        return True

    def insert_data_df(self, tab_name, data_df, ignore_col=True):
        """
            将data_df导入到conn的tab_name
        """
        conn = self.__connect()
        if not conn:
            return False
        else:
            data_df = data_df.fillna('')
            if ignore_col:
                cursor = conn.cursor()
                for i, row in data_df.iterrows():
                    sql = "INSERT INTO {} VALUES{}".format(tab_name, tuple(row))
                    # print(sql)
                    cursor.execute(sql)
                conn.commit()
            return True

    @staticmethod
    def init_db_from_excel(sqlite_path, excel_path, ignore_sheets=[]):
        """
            description: 根据提供的Excel生成Sqlite
        """
        print('Start Sqlite Initializing： {}~'.format(sqlite_path))
        # 1. 指定路径Excel不存在 -> 中断执行
        if not os.path.exists(excel_path):
            print('Excel not Exists, Quit Sqlite Initializing!')
        # 2. 指定路径Excel存在，但指定路径sqlite也存在 -> 中断执行
        elif os.path.exists(sqlite_path):
            print('Sqlite File already existed, Quit Sqlite Initializing!')
        # 3. 指定路径Excel存在，指定路径Sqlite不存在 -> 开始导入
        else:
            exl = pd.read_excel(excel_path, None)
            exl_sheets = exl.keys()
            if ignore_sheets: # 去除需要ignore的sheets
                exl_sheets = [e for e in exl_sheets if e not in ignore_sheets]
            # Excel的Sheet Name就是DB_Name
            for tab_name in exl_sheets:
                print("Table Name：", tab_name)
                ori_df = pd.read_excel(excel_path, sheet_name=tab_name, header=None)
                col_names, col_types = (ori_df.iloc[0], ori_df.iloc[1]) # 前两行是字段命名及类型
                data_df = ori_df[2:] # 后续是要导入的数据（可以没有）
                # 创建sqlite 并 导入数据
                db_util = SqliteUtils(db_path=sqlite_path)
                db_util.create_tab(tab_name, col_names, col_types)
                db_util.insert_data_df(tab_name, data_df)
            print('Finish Sqlite Initializing!')


if __name__ == '__main__':
    """ 1.Initialize DB from Excel """
    sqlite_path = '/Users/bytedance/projects/mywebapp/React+Flask/backend/service/data/quantitative_reports.db'
    excel_path = '/Users/bytedance/projects/mywebapp/React+Flask/backend/service/data/quantitative_reports.xlsx'
    SqliteUtils.init_db_from_excel(sqlite_path, excel_path, ignore_sheets=['new_fortune_score'])

    """ 2.查询表列表 """
    # db_util = SqliteUtils(sqlite_path)
    # tabs = db_util.get_tabs()
    # print(tabs)

    """ 3.查询表数据 """
    # data_df = db_util.get_tab_data_df(tabs[0])
    # print(data_df)

    """ 4.自定义sql查询 """
    # data_df = db_util.fetch_data_df("select * from report_list where s_code='1' and series_code='1.1'")
    # print(data_df)