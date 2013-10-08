# -*- coding: UTF-8 -*-

_metaclass_ = type
#when u is 4,the array is chaos and random
#even two num is similar ,the array is different
#the finally result is not determined
#the initVaule is include (0,1)
class Chaos:
    "生成混沌序列"
    def __init__(self,arraylen,x0,u):
        self.__lenOfArray = arraylen
        self.__x0 = x0
        self.__u = u
        
    def calculate(self,u,x):
        return u * x * (1 - x)
    
    def getChaosArray(self):
        "获取指定长度的混沌序列"
        self._chaosArray = []
        x = self.__x0
        for i in range(self.__lenOfArray):
            self._chaosArray.append(x)
            x = self.calculate(4.0, x)
        return self._chaosArray
    
    def getBinaryArray(self):
        "转换成二值序列"
        self.getChaosArray()
        for i in range(self.__lenOfArray):
            if self._chaosArray[i] > 0.5:
                self._chaosArray[i] = 1
            else:
                self._chaosArray[i] = 0
        return self._chaosArray
            
if __name__ == '__main__':
    c = Chaos(5,0.12,4)
    c.getChaosArray()
