# -*- coding: UTF-8 -*-
from Crypto.Hash import SHA
#the length of string is less than 2^21
from GlobalData import MagicNum

class HashBySha1:
    def __init__(self):
        self.__hash = SHA.new()
        
    def GetShortHash(self,message,binOrhex):
        "生成40位（16进制）的hash值(二进制是20位)，并且信息的长度必须小于2**21,最后一个参数用来指定返回二进制或是十六进制"
        assert(pow(2,21) > len(message))
        self.__hash.update(message)
        if binOrhex == MagicNum.HashBySha1c.BINARY:
            return self.__hash.digest()
        elif binOrhex == MagicNum.HashBySha1c.HEXADECIMAL:
            return self.__hash.hexdigest()
    
    def GetLongHash(self,message,binOrhex):
        _gaplen = pow(2,20)
        _hash = ""
        for index in range(len(message) / _gaplen):
            _hash += self.GetShortHash(message[index * _gaplen : (index + 1) * _gaplen],binOrhex)
        return self.GetHash(_hash, binOrhex)
    
    def GetHash(self,message,binOrhex):
        if len(message) < pow(2,21):
            return self.GetShortHash(message, binOrhex)
        else:
            return self.GetLongHash(message, binOrhex)
    
if __name__ == '__main__':
    h = HashBySha1()
