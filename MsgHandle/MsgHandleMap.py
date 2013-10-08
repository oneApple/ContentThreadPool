# -*- coding: UTF-8 -*-
_metaclass_ = type
from GlobalData.MagicNum import MsgTypec
from MsgHandle import RecvLoginFailed, SendDhPAndPubkey, RecvRegisterFailed, RecvRegisterSuccess, \
                      IdentifyVerifyFailed, RecvDhPubkeyAndSendDhGenerateSuccess, RecvLoginSuccess, SendFileBuffer, \
                      SendAgroupSignAndParam, RecvSendMediaSuccess, MsgHandleInterface,\
                      RecvFilename, RecvFileBuffer, RecvAllFile, RecvCgroupSignAndParam, \
                      SendLoginResult, RecvAndSendDh, SendRegisterResult, RecvObtainFile
                      


class MsgHandleMap:
    def __init__(self):
        "消息类型与处理类之间的关系"
        self.__MsgHandleMap = {MsgTypec.LOGINFAIL:RecvLoginFailed.RecvLoginFailed(),
                               MsgTypec.LOGINSUCCESS:RecvLoginSuccess.RecvLoginSuccess(),
                               MsgTypec.REQCLOSEMSG:IdentifyVerifyFailed.IdentifyVerifyFailed(),
                               MsgTypec.REGISTERFAIL:RecvRegisterFailed.RecvRegisterFailed(),
                               MsgTypec.REGISTERSUCCESSMSG:RecvRegisterSuccess.RecvRegisterSuccess(),
                               
                               MsgTypec.REQDHPANDPUBKEY:SendDhPAndPubkey.SendDhPAndPubkey(),
                               MsgTypec.SENDDHPUBKEY:RecvDhPubkeyAndSendDhGenerateSuccess.RecvDhPubkeyAndSendDhGenerateSuccess(),
                               
                               MsgTypec.REQFILEBUFFER:SendFileBuffer.SendFileBuffer(),
                               MsgTypec.IDENTITYVERIFYFAILED:IdentifyVerifyFailed.IdentifyVerifyFailed(),
                               MsgTypec.REQAGROUP:SendAgroupSignAndParam.SendAgroupSignAndParam(),
                               MsgTypec.RECVMEDIASUCCESS:RecvSendMediaSuccess.RecvSendMediaSuccess(),
                               
                               MsgTypec.REQAUDITRETURN:RecvFilename.RecvFilename(),
                               MsgTypec.SENDFILEBUFFER:RecvFileBuffer.RecvFileBuffer(),
                               MsgTypec.SENDFILEOVER:RecvAllFile.RecvAllFile(),
                               MsgTypec.SENDCGROUP:RecvCgroupSignAndParam.RecvCgroupSignAndParam(),
                               
                               MsgTypec.REQLOGINMSG:SendLoginResult.SendLoginResult(),
                               MsgTypec.SENDDHPANDPUBKEY:RecvAndSendDh.RecvAndSendDh(),
                               MsgTypec.REQREGISTERMSG:SendRegisterResult.SendRegisterResult(),
                               
                               MsgTypec.REQOBTAINFILE:RecvObtainFile.RecvObtainFile(),
                               
                               }
                
    def getMsgHandle(self,msgtype):
        "通过消息类型返回具体的处理类"
        if not self.__MsgHandleMap.has_key(msgtype):
            return MsgHandleInterface.MsgHandleInterface()
        return self.__MsgHandleMap[msgtype]