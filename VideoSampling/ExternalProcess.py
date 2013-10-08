# -*- coding:UTF-8 -*-   
  
import os, subprocess  
  
class ExternalProcess(object):  
    '''  Python管理应用程序  '''  
    def __init__(self,appPath):  
        '''  appPath:要启动的应用程序的路径  pid:启动的进程id  '''  
        self.appPath = appPath  
        self.pid = None  
          
    def run(self,args):  
        ''' 启动应用程序  '''  
        #判断应用程序路径是否存在  
        if(os.path.exists(self.appPath)):
            _cmd = self.appPath + " " + args  
            self.__p = subprocess.Popen(args = _cmd,shell=True)  
            self.pid = self.__p.pid  
            if self.pid is None:  
                return False  
            return True  
        else:  
            return False
    
    def waitForProcess(self):
        self.__p.wait()
              
              
if __name__ == '__main__':  
    exeMgr = ExternalProcess(r"C:\Program Files\Tencent\QQ\Bin\QQ.exe")  
    exeMgr.run()  
