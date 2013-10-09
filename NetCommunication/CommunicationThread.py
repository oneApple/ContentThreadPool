# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import EsocketManage
from GlobalData import CommonData
from MsgHandle import MsgHandleMap
from NetCommunication import NetSocketFun
import threading,select,socket,errno,struct

class CommunicationThread(threading.Thread):  
    epManage = EsocketManage.EsocketManage()
    
    def __init__(self):
        super(CommunicationThread,self).__init__()
        self.runflag = True
    
    def ModifyInToOut(self,fd):
        self.__class__.epManage.epfd.modify(fd, select.EPOLLOUT | select.EPOLLET)
    
    def SendData(self,fd,outdata):
        NetSocketFun.NetSocketSend(fd, outdata)
        self.__class__.epManage.epfd.modify(fd, select.EPOLLIN | select.EPOLLET)
    
    def run(self):
        while self.runflag:
            epoll_list = self.__class__.epManage.epfd.poll()
            for fd, events in epoll_list:
                if fd == self.__class__.epManage.listenfd.fileno():
                    conn, addr = self.__class__.epManage.listenfd.accept()
                    print addr,fd
                    conn.setblocking(0)
                    CommunicationThread.epManage.AddNewSockfd(conn,CommonData.ThreadType.ACCEPTAP)
                    
                elif select.EPOLLIN & events:
                    try:
                        _MsgHandleMap = MsgHandleMap.MsgHandleMap()
                        fddata = self.__class__.epManage.GetSockData(fd)
                        if not fddata:
                            break
                        recvbuffer = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),struct.calcsize(CommonData.MsgHandlec.MSGHEADTYPE))
                        if len(recvbuffer) == 0 or (len(recvbuffer) != struct.calcsize(CommonData.MsgHandlec.MSGHEADTYPE)):
                            self.__class__.epManage.DelSockfd(fd)
                            break
                        recvmsghead = struct.unpack(CommonData.MsgHandlec.MSGHEADTYPE,recvbuffer)
                        print fd,recvmsghead
                        _MsgHandleMap.getMsgHandle(recvmsghead[0]).HandleMsg(recvmsghead[1],fddata,self)
                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            break
                        else:
                            self.__class__.epManage.DelSockfd(fd)
                            break   
                elif select.EPOLLOUT & events:
                    try:
                        fddata = self.__class__.epManage.GetSockData(fd)
                        if not fddata:
                            break
                        self.SendData(fddata.GetData("sockfd"), fddata.GetData("outdata"))
                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            break
                        else:
                            self.__class__.epManage.DelSockfd(fd)
                            break   
                           
                elif select.EPOLLHUP & events:
                    self.__class__.epManage.DelSockfd(fd)
                       
        print "thread end"
            
    def stop(self):
        self.runflag = False
    