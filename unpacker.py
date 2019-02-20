import skiroc2cmsdata

class unpacker:
    compressedRawData=True
    sk2cms_data=[]
    rollMask=0

    def __init__(self,compressedRawData=True):
        self.compressedRawData=compressedRawData
        print("compressedRawData",compressedRawData)
        #self.sk2cms_data=[[[0 for sca in range(15)] for ch in range(128)] for sk in range(4)]
        
    def grayToBinary(self,gray):
        binary=gray
        binary ^= (gray >> 8);
        binary ^= (gray >> 4);
        binary ^= (gray >> 2);
        binary ^= (gray >> 1);
        return binary
    
        
    def unpack(self,rawdata):
        #decode raw data :
        sk2cmsdata=[]
        ev=[ [0 for i in range(1924)] for sk in range(4) ]
        if self.compressedRawData==False:
            for i in range(1924):
                for j in range(16):
                    x = rawdata[i*16 + j]
                    x = x&0xf
                    for sk in range(4):
                        ev[sk][i] = ev[sk][i] | (((x >> (3-sk) ) & 1) << (15 - j))

        else:
            for i in range(1924):
                for j in range(8):
                    x = rawdata[i*8 + j]
                    y = (x >> 4) & 0xf
                    x = x & 0xf
                    for sk in range(4):
                        ev[sk][i] = ev[sk][i] | ( ((x >> sk) & 1) << (14 - j*2) )
                        ev[sk][i] = ev[sk][i] | ( ((y >> sk) & 1) << (15 - j*2) )

        for sk in range(4):
            sk2cms=skiroc2cmsdata.skiroc2cmsdata(ev[sk],sk)
            sk2cmsdata.append(sk2cms)

        return sk2cmsdata

    def showData(self,eventID):
        for sk in range(4):
            print("Event = "+str(eventID)+"\t Chip = "+str(sk)+"\t RollMask = "+hex(self.rollMask))
            for ch in range(128):
                stream="channelID = "+str(63-ch%64)+""
                for sca in range(15):
                    stream=stream+" "+str(self.sk2cms_data[sk][ch][sca])
                print(stream)

