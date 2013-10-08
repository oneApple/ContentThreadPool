import wx, sys
from View import LoginDialog

reload(sys)                         
sys.setdefaultencoding('utf-8')   

app = wx.PySimpleApp()
dlg = LoginDialog.LoginDialog(None)
dlg.Run()
app.MainLoop()