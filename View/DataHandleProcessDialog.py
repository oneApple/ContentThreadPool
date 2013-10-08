#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

'''
    Function:绘图
    Input：NONE
    Output: NONE
    author: socrates
    blog:http://www.cnblogs.com/dyx1024/
    date:2012-07-22
'''  
import time
import thread 
 
def DataHandle(mainframe,frame):  
    from Command import DataHandleCmd
    _cmd = DataHandleCmd.DataHandleCmd(mainframe, *mainframe.getSamplingParams())
    _cmd.Excute() 
    frame.Destroy()
    thread.exit_thread()  
     
class DataHandleProcessDialog(wx.Dialog):
    def __init__(self,frame):
        wx.Dialog.__init__(self, None, -1, '数据处理中...',size = (400,150))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("white")
        self.count = 0
        self.gauge = wx.Gauge(panel, -1, 20, (100, 60), (250, 25), style = wx.GA_PROGRESSBAR)
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        
        self.frame = frame
        
             
    def OnIdle(self, event):
        self.count = self.count + 1
        if self.count >= 20:
            self.count = 0
        self.gauge.SetValue(self.count)
        time.sleep(0.1)
    
    def Run(self):
        self.Center()
        self.Show()
        
        thread.start_new_thread(DataHandle, (self.frame,self))
     