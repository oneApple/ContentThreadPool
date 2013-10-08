# -*- coding: UTF-8 -*-
import sqlite3

from GlobalData import ConfigData

class DataBaseInterface:
    "对sqlite简单封装"
    def __init__(self):
        "获取数据库路径"
        _config = ConfigData.ConfigData()
        self.dbPath = _config.GetDbPath()
    
    def Connect(self):
        "链接数据库,如果不存在则创建"
        self.__con = sqlite3.connect(self.dbPath)
         
    def ExcuteCmd(self,sql,value = []):
        "执行数据库命令"
        cur = self.__con.cursor()
        cur.execute(sql,value)
        self.__con.commit()
        
    def InsertValue(self,dbname,value = []):
        "向数据库中插入值"
        valueNum = len(value)
        cur = self.__con.cursor()
        query = 'INSERT INTO ' + dbname + ' VALUES(' + '?,' * (valueNum - 1) + '?)'
        cur.execute(query,value)
        self.__con.commit()
    
    def Search(self,sql,value = []):
        "执行查询命令"
        cur = self.__con.cursor()
        cur.execute(sql,value)
        self.__con.commit()
        return cur.fetchall()
     
    def CloseCon(self):
        "关闭数据库"
        self.__con.close()

if __name__=='__main__':
    a = DataBaseInterface()
    a.Connect()
    a.ExcuteCmd("CREATE TABLE APUserTable (name TEXT PRIMARY KEY,password TEXT)" )
    sql = "UPDATE APUserTable SET password=?,permission=? where name=?"
    a.ExcuteCmd(sql, ["new",2,"ke"])
    a.InsertValue("APUserTable",['ke',"d","POS",1])
    a.CloseCon()