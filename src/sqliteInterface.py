# -*- coding:utf-8 -*-
import sqlite3


class  SQLiteInterface(object):
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()
        
    def table_field(self, table_name):
        self._cursor.execute(r'select * from %s'%(table_name))
        return list(map(lambda x: x[0], self._cursor.description))

    def select(self, table_name, column=None, where=None, other_str="", output_dict=True):
        column_str, where_str= "*",""
        if column:
            column_str = ",".join(column)
            field_name = column
        else:
            field_name = self.table_field(table_name)
        if where:
            where_str = " where %s"%(where)
        select_str = "select {column} from {table} {where} {other}" \
                     .format(table = table_name
                             ,column = column_str
                             ,where = where_str
                             ,other = other_str)
        #print select_str
        self._cursor.execute(select_str)    
        raw_result = self._cursor.fetchall()

        if output_dict:
            return map(lambda x : dict(zip(field_name,x)),raw_result) 
        else:
            return raw_result 
