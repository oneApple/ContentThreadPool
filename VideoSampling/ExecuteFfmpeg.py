# -*- coding: UTF-8 -*-
import ExternalProcess
class ExecuteFfmpeg:
    "执行外部程序"
    def __init__(self,filename):
        "获取可执行程序路径"
        from GlobalData import ConfigData
        _cfg = ConfigData.ConfigData()
        self.__pathAndArgs = _cfg.GetFfmpegPathAndArgs()
        self.__filename = filename
        
    def Run(self):
        "获取参数"
        with open(self.__pathAndArgs[1],"r") as f:
            _args = f.read()
        cmd = "-i " + self.__filename + " " +  _args
        self.__e = ExternalProcess.ExternalProcess(self.__pathAndArgs[0])
        if self.__e.run(cmd) == False:
            return False
        else:
            return True
    def WaitForProcess(self):
        self.__e.waitForProcess()

if __name__ == "__main__":
    e = ExecuteFfmpeg("/home/keym/project/auditnew/AuditNew/media/auditserver/8.mpeg")
    
    if e.Run() == True:
        e.WaitForProcess()
