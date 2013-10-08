# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import CommunicationThread 

class ComThreadManage(object):
    def __init__(self):
        self.__threadlist = []
        
    def run(self,threadnum):
        for i in range(threadnum):
            th = CommunicationThread.CommunicationThread()
            self.__threadlist.append(th)
            th.start()
    
    def stop(self):
        "关闭所有线程"
        while self.__threadlist:
            th = self.__threadlist[0]
            th.stop()
            #th.join()
            self.__threadlist.remove(th)
        CommunicationThread.CommunicationThread().epManage.ReleaseAllData()

if __name__ == "__main__":
    c = ComThreadManage()
    c.run(4)