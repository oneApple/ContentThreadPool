# -*- coding: UTF-8 -*-
from ConfigParser import ConfigParser
_metaclass_ = type

class ConfigData:
    "获取配置数据"
    def __init__(self):
        "配置文件为CONFIGFILE"
        CONFIGFILE = "./Config.cfg"
        self.__cfg = ConfigParser()
        self.__cfg.read(CONFIGFILE)
        
    def GetDbPath(self):
        "获取数据库路径"
        return self.__cfg.get("database", "path")
    
    def GetIcoPath(self):
        "获取图标路径"
        return self.__cfg.get("ico", "path")
    
    def GetKeyPath(self):
        "获取密钥存放路径"
        return self.__cfg.get("keys", "path")
    
    def GetAuditServerAddress(self):
        "获取审核服务器地址"
        _ip = self.__cfg.get("auditserver", "ip")
        _port = self.__cfg.get("auditserver", "port")
        return _ip, _port
    
    def GetLocalServerAddress(self):
        "获取审核服务器地址"
        _ip = self.__cfg.get("localserver", "ip")
        _port = self.__cfg.get("localserver", "port")
        return _ip, _port
    
    def GetFfmpegPathAndArgs(self):
        _path = self.__cfg.get("ffmpeg", "path")
        _args = self.__cfg.get("ffmpeg", "args")
        return _path, _args
    
    def GetYVectorFilePath(self):
        _path = self.__cfg.get("yvector", "path")
        return _path
    
    def GetMediaPath(self):
        "获取媒体存放位置"
        return self.__cfg.get("media", "path")
    
if __name__=='__main__':
    c = ConfigData()
