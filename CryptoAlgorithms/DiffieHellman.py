# -*- coding: UTF-8 -*-

from random import getrandbits
from Crypto import Random
from Crypto.PublicKey.pubkey import bignum, getPrime

_g = 2

def GetBigPrime(bits = 300):
    "获取大素数"
    return bignum(getPrime(bits-1, Random.new().read))

class DiffieHellman:
    "p大素数,g底数,公钥可以公开，私钥_randnum要保密"
    def __init__(self, prime, bits = 300):
        self.__prime = prime
        while True:
            r = getrandbits(bits)
            if r < self.__prime:
                self.__randnum = r
                break
        self.pubkey = pow(_g, self.__randnum, self.__prime)
        
    def getPubkey(self):
        "获取公钥"
        return self.pubkey
    
    def getKey(self,otherpubkey):
        "获取最终的协商密钥"
        return pow(otherpubkey,self.__randnum, self.__prime)
    
if __name__ == '__main__':
    p = GetBigPrime()
    d1 = DiffieHellman(p)
    d2 = DiffieHellman(p)

