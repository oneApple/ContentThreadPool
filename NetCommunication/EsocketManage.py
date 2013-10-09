# -*- coding: UTF-8 -*-
_metaclass_ = type
import RWLock
import socket,select
from GlobalData import MagicNum, ConfigData

class GlobalDataValue(object):
    def __init__(self,sockfd,threadtype):
        self.__rwlock = RWLock.RWLock()
        self.sockfd = sockfd
        self.threadtype = threadtype
        self.currentbytes = 0
        self.peername = ""
        self.filename = ""
        self.outdata = ""
 
    def GetData(self,attr):
        self.__rwlock.acquire_read()
        try:
            return getattr(self,attr)
        finally:
            self.__rwlock.release_read()
    
    def SetData(self,attr,value):
        self.__rwlock.acquire_write()
        try:
            setattr(self,attr,value)
        finally:
            self.__rwlock.release_write()
    
    def __getattr__(self,attr):
        "没有该属性"
        return None

class GlobalDataManage(object):
    gRwlock = RWLock.RWLock()
    def __init__(self):
        self.__socketMap = {}
    
    def AddData(self,sockfd,threadtype):
        GlobalDataManage.gRwlock.acquire_write()
        try:
            if sockfd.fileno() not in self.__socketMap:
                self.__socketMap[sockfd.fileno()] = GlobalDataValue(sockfd,threadtype)
                return True
            return False
        finally:
            GlobalDataManage.gRwlock.release_write()
    
    def DelData(self,sockfdno):
        GlobalDataManage.gRwlock.acquire_write()
        try:
            if sockfdno in self.__socketMap:
                self.__socketMap[sockfdno].GetData("sockfd").close()
                del self.__socketMap[sockfdno]
                return True
            return False
        finally:
            GlobalDataManage.gRwlock.release_write()
    
#    def ModData(self,sockfd,attr,value):
#        GlobalDataManage.gRwlock.acquire_read()
#        try:
#            self.__socketMap[sockfd].SetData(attr,value)
#        finally:
#            GlobalDataManage.gRwlock.acquire_read()

    def ReleaseAllData(self):
        GlobalDataManage.gRwlock.acquire_read()
        try:
            for key in self.__socketMap:
                yield self.__socketMap[key].GetData("sockfd")
            self.__socketMap.clear()
        finally:
            GlobalDataManage.gRwlock.release_read()
    
    def GetData(self,sockfd):
        GlobalDataManage.gRwlock.acquire_read()
        try:
            if sockfd not in self.__socketMap:
                return None
            value = self.__socketMap[sockfd]
            return value
        finally:
            GlobalDataManage.gRwlock.release_read()
        
class EsocketManage(object):
    def __init__(self):
        self._gm = GlobalDataManage()
        self.epfd = select.epoll()
        self.registerListen()
    
    def registerListen(self):
        self.listenfd = socket.socket()
        self.listenfd.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        config = ConfigData.ConfigData()
        _listenAddress = config.GetLocalServerAddress()
        try:
            self.listenfd.bind((_listenAddress[0],int(_listenAddress[1])))
        except Exception,e:
            self.listenfd.close();
            print e
            return MagicNum.NetAcceptc.BINDERROR
        self.listenfd.listen(MagicNum.NetAcceptc.MAXLISTENNUM)
        self.listenfd.setblocking(0)
        self.epfd.register(self.listenfd.fileno(),select.EPOLLIN | select.EPOLLET)
    
    def AddNewSockfd(self,sockfd,threadtype):
        if self._gm.AddData(sockfd,threadtype):
            self.epfd.register(sockfd.fileno(),select.EPOLLIN | select.EPOLLET)
            
        
        
    def DelSockfd(self,sockfdno):
        if self._gm.DelData(sockfdno):
            self.epfd.unregister(sockfdno)

    def ReleaseAllData(self):
        for sockfd in self._gm.ReleaseAllData():
            self.epfd.modify(sockfd, select.EPOLLOUT)
            #self.epfd.unregister(sockfd.fileno())
        self.epfd.close()
#    def SetSockData(self,sockfd,attr,value):
#        self._gm.ModData(sockfd.fileno(), attr, value)
    
    def GetSockData(self,sockfdno):
        return self._gm.GetData(sockfdno)
    

if __name__ == "__main__":
    g = GlobalDataValue()
    g.SetData("attr", "value")
    print g.GetData("attr")
        
    
