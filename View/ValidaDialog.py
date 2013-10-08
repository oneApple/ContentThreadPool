# -*- coding: UTF-8 -*-

import wx

import NotEmptyValidator
from GlobalData import MagicNum
   
class ValidaDialog(wx.Dialog):
    "非空验证窗口，必须填写所有才可以"
    def __init__(self,title,type):
        "初始化并创建所有组件"
        self.__textList = []
        self.__type = type
        
        super(ValidaDialog,self).__init__(None, -1, title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.createHeader(self.__type)
        self.createAllText()
        self.addNewControl()
        self.createButton(wx.ALIGN_CENTER)
        
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)  
    
    def getTextLabel(self):
        "文本标签列表"
        pass
    
    def getHeaderText(self):
        "头部静态文本显示信息"
        pass
    
    def firstButtonFun(self):
        "取消按钮动作"
        self.Destroy()
    
    def secondButtonFun(self):
        "提交按钮动作"
        pass
    
    def registerButtonFun(self,event):
        "图片按钮动作"
        pass
    
    def getInputText(self):
        "获取输入数据"
        _texts = []
        for _text in self.__textList:
            _texts.append(_text.GetValue())
        return _texts;
    
    def setInputText(self,textlist):
        "设置输入框显示数据"
        for control,text, in zip(self.__textList,textlist):
            control.SetValue(text)
    
    def setHeaderText(self,text):
        "设置头部标签文本"
        self.__text.SetLabel(text)
        self.__text.SetForegroundColour("red")
    
    def addNewControl(self):
        "怎加新的控件"
        pass
    
    def createHeaderStatic(self):
        "创建头部静态文本"
        self.__text = wx.StaticText(self, -1, self.getHeaderText())
        self.__text.SetForegroundColour("green")
        self.__text.SetBackgroundColour("white")
        
        self.sizer.Add(self.__text, 0, wx.ALIGN_CENTER, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createHeaderButton(self):
        "创建头部按钮"
        from GlobalData import ConfigData
        _config = ConfigData.ConfigData()
        jpg = wx.Image(_config.GetIcoPath(),wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        fileButton=wx.BitmapButton(self,-1,jpg)
        self.Bind(wx.EVT_BUTTON,self.registerButtonFun,fileButton)
        self.sizer.Add(fileButton, 0, wx.EXPAND, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createHeader(self,type):
        "创建头部"
        if type == MagicNum.ValidaDialogc.STATICTEXT:
            self.createHeaderStatic()
        elif type == MagicNum.ValidaDialogc.IMAGEBUTTON:
            self.createHeaderButton()
            self.createHeaderStatic()

    def createSingleText(self,sizer,label):
        "创建单个文本框"
        _static = wx.StaticText(self, -1, label)
        if label == "密码":
            _text = wx.TextCtrl(self, validator=NotEmptyValidator.NotEmptyValidator(),style = wx.PASSWORD)
        else:
            _text = wx.TextCtrl(self, validator=NotEmptyValidator.NotEmptyValidator())
        sizer.Add(_static,0,wx.ALIGN_RIGHT)
        sizer.Add(_text,0,wx.EXPAND)
        self.__textList.append(_text)
    
    def createAllText(self):
        "创建所有文本框"
        _textlist = self.getTextLabel();
        _textnum = len(_textlist)
        _fgs = wx.FlexGridSizer(_textnum, 2, 5, 10)
        for _label in _textlist:
            self.createSingleText(_fgs,_label)
        self.__textList[0].SetFocus()
        _fgs.AddGrowableCol(1)
        self.sizer.Add(_fgs, 0, wx.EXPAND|wx.ALL, 5)
    
    def createButton(self,type):
        "创建按钮"
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        okay = wx.Button(self, wx.ID_OK, "提交")
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL,"取消")
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(cancel)
        btns.AddButton(okay)
        btns.Realize()
        self.sizer.Add(btns, 0, type|wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def tryAgain(self,msg):
        _input = [""] * len(self.__textList)
        self.setInputText(_input)
        self.setHeaderText(msg.data)
        self.Hide()
        self.Run()
   
    def Run(self):
        "显示"
        _res = self.ShowModal()
        if _res == wx.ID_OK:
            self.secondButtonFun()
        elif _res == wx.ID_CANCEL:
            self.firstButtonFun()
        #self.Destroy()
   