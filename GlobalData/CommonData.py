# -*- coding: UTF-8 -*-
class MsgHandlec:
    MSGHEADTYPE = 'ii'
    SAMPLINGTYPE = "fffff"
    PADDING = "###"
    SHOWPADDING = "::"
    SPARATE = "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~\n"
    FILEBLOCKSIZE = 10240
    
class ThreadType:
    CONNECTAP = 10001
    ACCEPTAP = 10002    
    ACCETPNO = 10003
    
class ViewPublisherc:
    LOGIN_TRYAGAIN = "logintryagain"
    LOGIN_SWITCH = "loginswitch"
    
    REGISTER_TRYAGAIN = "registertryagain"
    REGISTER_SWITCH = "registerswitch"
    
    MAINFRAME_REWRITETEXT = "mainframerewritetext"
    MAINFRAME_APPENDTEXT = "mainframeappendtext"
    MAINFRAME_REFRESHSTATIC = "mainframerefstatic"
    MAINFRAME_REFRESHFILETABLE = "mainframereffiletable"
    FULLFRAME_APPENDTEXT = "fullframeappendtext"

class MainFramec:
    usermenu = {"用户审核".decode("utf8"):"UserAudit","用户删除".decode("utf-8"):"DeleteUser"}
    toolmenu = {"清理屏幕".decode("utf8"):"ClearDisplay"}
    menuMap = {"用户管理".decode("utf8"):usermenu,"工具".decode("utf8"):toolmenu,}
    disablemenu = ["用户审核","用户删除"]
    
class Rsac:
    "密钥及明文长度:对应关系为:1024:128,2048:256"
    KEYLEN = 1024
    PLAINTLEN = 128    
    
class HashBySha1c:
    "哈希后的长度"
    BINARYHASH = 20
    HEXHASH = 40

class SamplingFrameArrayc:
    GROUPPARAMELEN = 7