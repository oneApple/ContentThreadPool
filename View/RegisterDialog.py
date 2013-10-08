# -*- coding: UTF-8 -*-
import wx
from wx.lib.pubsub  import Publisher

import ValidaDialog
import LoginDialog
from GlobalData import MagicNum, CommonData

class RegisterDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,netconnect):
        super(RegisterDialog,self).__init__("注册",MagicNum.ValidaDialogc.STATICTEXT)
        self.__netconnect = netconnect
        self.registerPublisher()
        
    def registerPublisher(self):
        Publisher().subscribe(self.tryAgain, CommonData.ViewPublisherc.REGISTER_TRYAGAIN)    
        Publisher().subscribe(self.SwitchView, CommonData.ViewPublisherc.REGISTER_SWITCH)  
    
    def getTextLabel(self):
        _labelList = ["用户名", "密码","重复密码","监听地址","监听端口"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
                \n 欢 迎 注 册 系 统
                """
        return _text
        
    def innerTryAgain(self,msg):
        self.setInputText(["","","","",""])
        self.setHeaderText("\n" + msg + "\n")
        self.Hide()
        self.Run()

    def SwitchView(self,msg):
        self.Destroy()
        _loginFrame = LoginDialog.LoginDialog(self.__netconnect)
        _loginFrame.Run()

    def addNewUser(self,inputlist):
        del inputlist[1]
        self.__netconnect.ReqRegister(*inputlist)
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        if _inputlist[1] != _inputlist[2]:
            self.innerTryAgain("密码输入不一致")
        else:
            self.addNewUser(_inputlist)    
        
if __name__=='__main__':
    app = wx.PySimpleApp()
    dlg = RegisterDialog()
    dlg.Run()
    app.MainLoop()