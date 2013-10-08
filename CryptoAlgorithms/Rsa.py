# -*- coding: UTF-8 -*-

from Crypto.PublicKey import RSA
import pickle ,random ,string

class Rsa:
    def __init__(self,directory = "./keys"):
        self.__keydir = directory
        self.__prikeydir = self.__keydir + "/own/prikey.pem"
        self.__pubkeydir = self.__keydir + "/own/pubkey.pkl"
    
    def GenerateKeypair(self,bits = 1024):
        key = RSA.generate(bits)
        with open(self.__prikeydir,"w") as f:
            f.write(key.exportKey())
        with open(self.__pubkeydir,"w") as f:
            self.__pubkeystring = pickle.dump(key.publickey(), f)
    
    def EncryptByPubkey(self, plaintext, pubkeydir = ""):
        dir = self.__keydir + "/" + pubkeydir + "/" + "pubkey.pkl"
        with open(dir, 'r') as f:
            pubkey = pickle.load(f)
        return "".join(pubkey.encrypt(plaintext,random.randint(0,len(plaintext))))
    
    def DecryptByPrikey(self,ciphertext):
        with open(self.__prikeydir,'r') as f:
            key = RSA.importKey(f.read())
            return key.decrypt(ciphertext)
                
    def SignByPrikey(self,message):
        with open(self.__prikeydir,'r') as f:
            key = RSA.importKey(f.read())
            return str(key.sign(message, random.randint(0,len(message)))[0])
        
    def VerifyByPubkey(self,message,sign,pubkeydir = ""):
        dir = self.__keydir + "/" + pubkeydir + "/pubkey.pkl"
        with open(dir, 'r') as f:
            pubkey = pickle.load(f)
            signtuple = (string.atol(sign),)
            return pubkey.verify(message,signtuple)
   
if __name__ == '__main__':
    r = Rsa(".")
    r.GenerateKeypair()
            