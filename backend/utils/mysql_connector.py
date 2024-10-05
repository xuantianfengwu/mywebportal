
import pandas as pd
from sqlalchemy import create_engine, text


class MySQLConnection():
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        """ 初始化数据库连接 """
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(user, passwd,
                                                                                       host, port, db,
                                                                                       charset))

    def read_df(self, sql_query):
        """ MySQL导出DataFrame """
        # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
        df_read = pd.read_sql_query(sql_query, self.engine)
        return df_read

    def insert_df(self, df_write, table, if_exists='fail'):
        """ 将df储存为MySQL中的表，不储存index列 """
        df_write.to_sql(table, self.engine, index=False, if_exists=if_exists)

    def execute(self, sql):
        result = self.engine.execute(text(sql))
        return result

    def get_table_column_lst(self, table):
        table_desc_df = self.read_df('desc {}'.format(table))
        return table_desc_df

    def create_table(self, table, columns, column_types):
        conn = self.engine.connect()
        conn.begin()
        try:
            conn.execute("Drop table if exists {}".format(table))
            column_info = ','.join(['{} {}'.format(col_name, col_type)
                                    for (col_name, col_type) in zip(columns, column_types)])
            sql = 'CREATE TABLE {}({})'.format(table, column_info)
            result = conn.execute(sql)
        finally:
            conn.close()
        return True

if __name__ == '__main__':
    mysql_connector = MySQLConnection(host='106.13.180.162', port='3307', user='xzh', passwd='!QAZ1qaz', db='trading')
    res = mysql_connector.create_table('test', ['a','b','c'], ['varchar(10)', 'varchar(20)', 'decimal(10,2)'])
    print(res)
