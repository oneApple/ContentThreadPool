# -*- coding: UTF-8 -*-
import wx
from wx.lib.pubsub  import Publisher

import ValidaDialog
import RegisterDialog
import MainFrame
from GlobalData import MagicNum, CommonData
from NetCommunication import NetConnect

class LoginDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,netconnect):
        super(LoginDialog,self).__init__("登录",MagicNum.ValidaDialogc.IMAGEBUTTON)
        if not netconnect:
            self.__netconnect = NetConnect.NetConnect(self)
            if self.__netconnect.StartNetConnect() == MagicNum.NetConnectc.NOTCONNECT:
                self.setHeaderText("无法连接到服务器，请重新启动") 
        else :
            self.__netconnect = netconnect
        self.registerPublisher()
        
    def registerPublisher(self):
        Publisher().subscribe(self.tryAgain, CommonData.ViewPublisherc.LOGIN_TRYAGAIN)    
        Publisher().subscribe(self.SwitchView, CommonData.ViewPublisherc.LOGIN_SWITCH)     
        
    def getTextLabel(self):
        _labelList = ["用户名", "密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
                   内 容 提 供 部 门\
                """
        return _text
    
    def SwitchView(self,msg):
        _inputlist = self.getInputText()
        _mainFrame = MainFrame.MyFrame(msg.data + (_inputlist[0],),self.__netconnect)
        _mainFrame.Run()
        self.Hide()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        self.__netconnect.ReqConnect(_inputlist[0], _inputlist[1])
            
    def registerButtonFun(self,event):
        self.Destroy()
        _dlg = RegisterDialog.RegisterDialog(self.__netconnect)
        _dlg.Run()
        
        
if __name__=='__main__':
    app = wx.PySimpleApp()
    dlg = LoginDialog(None)
    dlg.Run()
    app.MainLoop()