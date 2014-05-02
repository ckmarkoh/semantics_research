# -*- coding:utf-8 -*-
import sqlite3



class  SQLiteInterface(object):
    def __init__(self,db_path):
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()
        
    def table_field(self,table_name):
        _cursor.execute(r'select * from %s'%(table_name))
        return list(map(lambda x: x[0], _cursor.description))

    def select(self,table_name,column=None,where=None,output_dict=True):
        select_str = "select {column} from {table_name}".format(table_name)
        if column:
            select_str = select_str.format(column=",".join(column))
            field_name = column
        else:
            select_str = select_str.format(column='*')
            field_name = self.table_field(table_name)
        if where:
            select_str += " where %s"%(where)

        _cursor.execute(select_str)    
        raw_result = _cursor.fetchall()

        if output_dict:
            return map(lambda x : zip(field_name,x),raw_result) 
        else:
            return raw_result 
