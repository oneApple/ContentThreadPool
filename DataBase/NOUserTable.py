# -*- coding: UTF-8 -*-
import sqlite3

from DataBase import DataBaseInterface
from GlobalData import MagicNum

class NOUserTable(DataBaseInterface.DataBaseInterface,object):
    def __init__(self):
        "初始化父类"
        super(NOUserTable,self).__init__()
    
    def CreateTable(self):
        "创建ap用户表并插入超级管理员"
        self.ExcuteCmd("CREATE TABLE NOUserTable (name TEXT PRIMARY KEY,password TEXT,permission INT)")
        self.AddNewUser(['local','local',MagicNum.CPUserTablec.NORMAL])
    
    def VerifyNamePsw(self,name,psw):
        "验证一个用户的用户名和密码是否正确"
        _sql = "SELECT * FROM NOUserTable where name=? AND password=?"
        _res = self.Search(_sql, [name.decode("utf8"),psw])
        if _res == []:
            return False
        else:
            return _res[0][2]
    
    def AddNewUser(self,value):
        "增加新的用户"
        try:
            self.InsertValue("NOUserTable",value)
        except sqlite3.IntegrityError:
            return False
        return True
    
    def AlterUser(self,attri,value,name):
        "更改用户信息"
        _sql = "UPDATE NOUserTable SET "+ attri +"=? where name=?"
        self.ExcuteCmd(_sql,[value,name.decode("utf8")])
    
    def searchUser(self,name):
        _sql = "SELECT * FROM NOUserTable where name=?"
        return self.Search(_sql, [name.decode("utf8")])
    
    def deleteUser(self,name):
        _sql = "DELETE FROM NOUserTable WHERE name=?"
        self.ExcuteCmd(_sql, [name.decode("utf8"),])  
    
if __name__=='__main__':
    a = NOUserTable()
    a.Connect()
    #a.CreateTable()
    a.deleteUser("no")
    #a.AddNewUser(["a","a","localhost",8000,4001])
    a.CloseCon()