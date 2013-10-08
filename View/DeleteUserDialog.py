# -*- coding: UTF-8 -*-

import wx
from DataBase import NOUserTable
from GlobalData import MagicNum
   
class DeleteUserDialog(wx.SingleChoiceDialog):
    def __init__(self,title):
        self.__userlist = self.getUserList()
        super(DeleteUserDialog,self).__init__(None,"删除用户",title,self.__userlist)
   
    def getUserList(self):
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _sql = "select name from NOUserTable"
        _res = _db.Search(_sql)
        _db.CloseCon()
        _userlist = []
        for name in _res:
            _userlist.append(name[0])
        return _userlist
   
    def secondButtonFun(self):
        _choice = self.GetStringSelection()
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _db.deleteUser(_choice)
        _db.CloseCon()
        
    def firstButtonFun(self):
        pass
   
    def Run(self):
        _res = self.ShowModal()
        if _res == wx.ID_OK:
            self.secondButtonFun()
        elif _res == wx.ID_CANCEL:
            self.firstButtonFun()
        self.Destroy()
   
if __name__=='__main__':
    app = wx.App()
    f = DeleteUserDialog("修改权限")
    f.Run()
    app.MainLoop()