# -*- coding: UTF-8 -*-
from GlobalData import CommonData
class RegionMap:
    "区域与块对应关系"
    def regionMap(self,pos):
        "区域对应关系"
        pos = self.binaryToDecimal(pos)
        if pos == 0:
            return 0
        elif pos == 1:
            return 2
        elif pos == 2:
            return 8
        elif pos == 3:
            return 6
        elif pos == 4 or pos == 8 or pos == 12:
            return 1
        elif pos == 5 or pos == 9 or pos == 13:
            return 5
        elif pos == 6 or pos == 10 or pos == 14:
            return 7
        elif pos == 7 or pos == 11 or pos == 15:
            return 3
        else:
            return 4
    
    def unitMap(self,pos):
        "单元对应关系"
        pos = self.binaryToDecimal(pos)
        if pos == 0:
            return 0
        elif pos == 1:
            return 1
        elif pos == 2:
            return 3
        else:
            return 2
            
    
    def binaryToDecimal(self,binArray):
        "二进制转化为十进制"
        _bin = binArray[::-1]
        _dec = 0;
        for i,b in enumerate(_bin):
            if b == 1:
                _dec += 2**i
        return _dec
    
    def GetRegion(self,posArray):
        "获取位置"
        assert(len(posArray) == CommonData.SamplingFrameArrayc.GROUPPARAMELEN)
        _region = self.regionMap(posArray[:5])
        _unit = self.unitMap(posArray[5:])
        return _region,_unit
     

if __name__ == "__main__":
    r = RegionMap()
    r.GetRegion([0,1,0,1,1,1,1])
        