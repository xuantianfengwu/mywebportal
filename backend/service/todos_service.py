
from ..utils import sqlite_utils
import os

class TodosService(object):
    def __init__(self):
        self.sqlite_name = 'todos'
        self.sqlite_db = sqlite_utils.SqliteConnection(self.sqlite_name)
        self.task_lst = self._generate_task_lst()

    def _generate_task_lst(self):
        try:
            todos_task_df = self.sqlite_db.get_table_data_df('task')
            todos_lst = [{'id':                 row[0],
                          'task_name':          row[1],
                          'task_desc':          row[2],
                          'task_owner':         row[3],
                          'create_date':        row[4],
                          'last_modify_date':   row[5],
                          'is_complete':        row[6]
                          } for i,row in todos_task_df.iterrows()
                        ]
        except:
            todos_lst = [{'id':                 '0',
                          'task_name':          'test',
                          'task_desc':          'test',
                          'task_owner':         'user1',
                          'create_date':        '00000000',
                          'last_modify_date':   '00000000',
                          'is_complete':        False
                          }]
        return todos_lst

    def get_all_tasks(self):
        return self.task_lst