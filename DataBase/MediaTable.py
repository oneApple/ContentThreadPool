# -*- coding: UTF-8 -*-
import sqlite3

from DataBase import DataBaseInterface
from GlobalData import MagicNum

class MediaTable(DataBaseInterface.DataBaseInterface,object):
    def __init__(self):
        "初始化父类"
        super(MediaTable,self).__init__()
    
    def CreateTable(self):
        "创建媒体表"
        self.ExcuteCmd("CREATE TABLE MediaTable (name TEXT PRIMARY KEY,agroupParam TEXT,agroupHash TEXT,  \
                                                                       bgroupParam TEXT,bgroupHash TEXT,  \
                                                                       audituser TEXT,status INT)")
    
    def AddNewMedia(self,value):
        "增加新的媒体"
        _value =value + (MagicNum.MediaTablec.UNACCEPT,)
        try:
            self.InsertValue("MediaTable",_value)
        except sqlite3.IntegrityError:
            return False
        return True
    
    def AlterMedia(self,attri,value,name):
        "更改媒体表"
        _sql = "UPDATE MediaTable SET "+ attri +"=? where name=?"
        self.ExcuteCmd(_sql,[value,name.decode("utf8")])
    
    def searchMedia(self,name):
        _sql = "SELECT * FROM MediaTable where name=?"
        return self.Search(_sql, [name.decode("utf8")])
    
    def deleteMedia(self,name):
        _sql = "DELETE FROM MediaTable WHERE name=?"
        self.ExcuteCmd(_sql, [name.decode("utf8"),])  
    
if __name__=='__main__':
    a = MediaTable()
    a.Connect()
    #a.ExcuteCmd("drop table MediaTable")
    #a.CreateTable()
#    a.AddNewMedia(("14frame.mpeg","sign","signparam","bgroup","bgroupparam"))
    #a.deleteMedia("视频源1.mpg".decode("utf-8"))
    a.CloseCon()