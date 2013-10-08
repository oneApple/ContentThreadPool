# -*- coding: UTF-8 -*-
import Rsa
from GlobalData import ConfigData, CommonData

class RsaKeyExchange:
    "生成和交换密钥"
    def __init__(self):
        _cfd = ConfigData.ConfigData()
        self.__keyPath = _cfd.GetKeyPath()
    
    def GenerateRsaKey(self):
        import os
        _ownPath = self.__keyPath + "/own"
        if not os.path.exists(_ownPath):
            if not os.path.exists(self.__keyPath):
                os.mkdir(self.__keyPath)
            os.mkdir(_ownPath)
            _rsa = Rsa.Rsa(self.__keyPath)
            _rsa.GenerateKeypair(CommonData.Rsac.KEYLEN)
    
    def GetPubkeyStr(self,name):
        _path = self.__keyPath + "/" + name + "/pubkey.pkl"
        with open(_path, 'r') as f:
            pkeystr = f.read()
        return pkeystr     
    
    def WritePubkeyStr(self,name,pkeystr):
        import os
        _dir = self.__keyPath + "/" + name
        _path = _dir + "/pubkey.pkl"
        if not os.path.exists(_dir):
                os.mkdir(_dir)
        with open(_path, 'w') as f:
            f.write(pkeystr)
               

if __name__ == "__main__":
    r = RsaKeyExchange()
    r.GenerateRsaKey()
    _s = r.GetPubkeyStr("own")
    r.WritePubkeyStr("name", _s)
    _cfd = ConfigData.ConfigData()
    _rsa = Rsa.Rsa(_cfd.GetKeyPath())
    