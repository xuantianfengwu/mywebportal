
import os
import pandas as pd

from ..utils.osfile_utils import OSFileUtils
from ..utils.sqlite_utils import SqliteUtils

class MiniProgramTools(object):
    def __init__(self):
        self.quant_db = self._init_data()

    def _init_data(self):
        db_path = os.path.join('.', 'backend', 'service', 'data', 'quantitative_reports.db')
        print(db_path)
        quant_db = SqliteUtils(db_path)
        return quant_db

    def get_quant_series_list(self):
        series_lst = self.quant_db.get_tab_data_df('series_list')
        return series_lst

    def get_quant_series_info(self, s_code, series_code):
        """ 根据输入的券商代码(s_code)和系列代码(series_code)，获取对应的series信息 """
        series_info = self.quant_db.fetch_data_df("select * from series_list where s_code={} and series_code={}".format(s_code, series_code))
        return series_info

    def get_quant_series_reports(self, s_code, series_code):
        """
            根据输入的券商代码(s_code)和系列代码(series_code)，获取对应的文章列表
        """
        report_lst = self.quant_db.fetch_data_df("select * from report_list where s_code={} and series_code={}".format(s_code, series_code))
        return report_lst

    def generate_q_series_list(self):
        data_df = self.get_quant_series_list()
        data = {
            'q_series_list': data_df.to_dict(orient='records')
        }
        return data

    def generate_q_series_reports(self, s_code, series_code):
        q_series_info = self.get_quant_series_info(s_code, series_code)
        q_series_reports = self.get_quant_series_reports(s_code, series_code)
        data = {
            'q_series_info': q_series_info.to_dict(orient='records')[0],
            'q_series_reports': q_series_reports.to_dict(orient='records')
        }
        return data

if __name__ == '__main__':
    m = MiniProgramTools()

    """ 1.获取quant_series_lst """
    q_series = m.get_quant_series_list()

    """ 2.获取quant_report_lst """
    q_reports = m.get_quant_series_reports('1','1.1')

    """ 3.获取quant_series_info """
    series_info = m.get_quant_series_info('1', '1.1')
