# -*- coding: UTF-8 -*-
import NetAcceptThread
_metaclass_ = type
class NetAccept:
    def __init__(self,view):
        self._netaccept = NetAcceptThread.NetAcceptThread()
        self._netaccept.setDaemon(True)
    def startNetConnect(self):
        self._netaccept.start()

    def stopNetConnect(self):
        self._netaccept.stop()
        #self._netaccept.join()
if __name__=='__main__':
    n = NetAccept(1234)
    n.startNetConnect() 