import bitarray
import pandas as pd
from sympy.combinatorics.graycode import gray_to_bin

class skiroc2cmsdata:
    
    def __init__(self,data,chipID):
        self.data=data
        self.MASK_ADC = 0x0FFF;
        self.MASK_ROLL = 0x1FFF;
        self.MASK_GTS_MSB = 0x3FFF;
        self.MASK_GTS_LSB = 0x1FFF;
        self.MASK_ID = 0xFF;
        self.MASK_HEAD = 0xF000;
        self.N_CHANNELS_PER_SKIROC=64;
        self.NUMBER_OF_SCA = 13;
        self.ADCLOW_SHIFT = 0;
        self.ADCHIGH_SHIFT = 64;
        self.SCA_SHIFT = 128;
        self.SKIROC_DATA_SIZE = 1924; #number of 16 bits words
        self.chipID=chipID
        
    def grayToBinary(self,gray):
        return int( gray_to_bin( bin(gray)[2:] ),2 )
        
    def ADCLow(self,chan, sca):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        sca=self.NUMBER_OF_SCA-1-sca;
        if sca>=0 and sca<self.NUMBER_OF_SCA:
            return self.grayToBinary( self.data[chan+self.ADCLOW_SHIFT+self.SCA_SHIFT*sca] & self.MASK_ADC)
        else:
            return 10000

    def ADCHigh(self,chan, sca):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        sca=self.NUMBER_OF_SCA-1-sca;
        if sca>=0 and sca<self.NUMBER_OF_SCA:
            return self.grayToBinary( self.data[chan+self.ADCHIGH_SHIFT+self.SCA_SHIFT*sca] & self.MASK_ADC)
        else:
            return 10000

    def TOTFast(self,chan):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        return self.grayToBinary( self.data[chan+self.ADCLOW_SHIFT+self.SCA_SHIFT*(self.NUMBER_OF_SCA+1)] & self.MASK_ADC)

    def TOTSlow(self,chan):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        return self.grayToBinary( self.data[chan+self.ADCHIGH_SHIFT+self.SCA_SHIFT*(self.NUMBER_OF_SCA+1)] & self.MASK_ADC)

    def TOAFall(self,chan):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        return self.grayToBinary( self.data[chan+self.ADCLOW_SHIFT+self.SCA_SHIFT*self.NUMBER_OF_SCA] & self.MASK_ADC)

    def TOARise(self,chan):
        chan=self.N_CHANNELS_PER_SKIROC-1-chan;
        return self.grayToBinary( self.data[chan+self.ADCHIGH_SHIFT+self.SCA_SHIFT*self.NUMBER_OF_SCA] & self.MASK_ADC)

    def rollMask(self):
        return self.data[self.SKIROC_DATA_SIZE-4]&self.MASK_ROLL; 

    def rollPositions(self):
        positions=[0 for i in range(self.NUMBER_OF_SCA)]

        rollmask=self.rollMask()
        bits=bitarray.bitarray(self.NUMBER_OF_SCA)
        for i in range(self.NUMBER_OF_SCA):
            bits[self.NUMBER_OF_SCA-1-i]=(rollmask>>i)&1

        if bits[0]==1 and bits[self.NUMBER_OF_SCA-1]==1: #ie 100...001
            positions[0]=12;
            for i in range(1,self.NUMBER_OF_SCA):
	        positions[i]=i-1
        else:
            for i in range(self.NUMBER_OF_SCA):
                if bits[i]==1:
                    positions[i]=self.NUMBER_OF_SCA-2
                    positions[i+1]=self.NUMBER_OF_SCA-1
                    for j in range(self.NUMBER_OF_SCA-2):
                        positions[(i+2+j)%self.NUMBER_OF_SCA]=j
                break
        
        return positions

    def dataFrame(self):
        chips=[self.chipID for ch in range (self.N_CHANNELS_PER_SKIROC)]
        channels=[ch for ch in range (self.N_CHANNELS_PER_SKIROC)]
        totSlow=[self.TOTSlow(ch) for ch in range (self.N_CHANNELS_PER_SKIROC)]
        totFast=[self.TOTFast(ch) for ch in range (self.N_CHANNELS_PER_SKIROC)]
        toaRise=[self.TOARise(ch) for ch in range (self.N_CHANNELS_PER_SKIROC)]
        toaFall=[self.TOAFall(ch) for ch in range (self.N_CHANNELS_PER_SKIROC)]
        hg_sca0=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca1=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca2=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca3=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca4=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca5=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca6=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca7=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca8=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca9=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca10=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca11=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        hg_sca12=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca0=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca1=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca2=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca3=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca4=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca5=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca6=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca7=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca8=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca9=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca10=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca11=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        lg_sca12=[0 for ch in range(self.N_CHANNELS_PER_SKIROC)]
        timesamps=self.rollPositions()
        for ch in range(self.N_CHANNELS_PER_SKIROC):
            hg_sca0[ch] = self.ADCLow(ch,0) if timesamps[0]<9 else 0
            hg_sca1[ch] = self.ADCLow(ch,1) if timesamps[1]<9 else 0
            hg_sca2[ch] = self.ADCLow(ch,2) if timesamps[2]<9 else 0
            hg_sca3[ch] = self.ADCLow(ch,3) if timesamps[3]<9 else 0
            hg_sca4[ch] = self.ADCLow(ch,4) if timesamps[4]<9 else 0
            hg_sca5[ch] = self.ADCLow(ch,5) if timesamps[5]<9 else 0
            hg_sca6[ch] = self.ADCLow(ch,6) if timesamps[6]<9 else 0
            hg_sca7[ch] = self.ADCLow(ch,7) if timesamps[7]<9 else 0
            hg_sca8[ch] = self.ADCLow(ch,8) if timesamps[8]<9 else 0
            hg_sca9[ch] = self.ADCLow(ch,9) if timesamps[9]<9 else 0
            hg_sca10[ch]= self.ADCLow(ch,10) if timesamps[10]<9 else 0
            hg_sca11[ch]= self.ADCLow(ch,11) if timesamps[11]<9 else 0
            hg_sca12[ch]= self.ADCLow(ch,12) if timesamps[12]<9 else 0
            lg_sca0[ch] = self.ADCLow(ch,0) if timesamps[0]<9 else 0
            lg_sca1[ch] = self.ADCLow(ch,1) if timesamps[1]<9 else 0
            lg_sca2[ch] = self.ADCLow(ch,2) if timesamps[2]<9 else 0
            lg_sca3[ch] = self.ADCLow(ch,3) if timesamps[3]<9 else 0
            lg_sca4[ch] = self.ADCLow(ch,4) if timesamps[4]<9 else 0
            lg_sca5[ch] = self.ADCLow(ch,5) if timesamps[5]<9 else 0
            lg_sca6[ch] = self.ADCLow(ch,6) if timesamps[6]<9 else 0
            lg_sca7[ch] = self.ADCLow(ch,7) if timesamps[7]<9 else 0
            lg_sca8[ch] = self.ADCLow(ch,8) if timesamps[8]<9 else 0
            lg_sca9[ch] = self.ADCLow(ch,9) if timesamps[9]<9 else 0
            lg_sca10[ch]= self.ADCLow(ch,10) if timesamps[10]<9 else 0
            lg_sca11[ch]= self.ADCLow(ch,11) if timesamps[11]<9 else 0
            lg_sca12[ch]= self.ADCLow(ch,12) if timesamps[12]<9 else 0
            
        # highGains=[[self.ADCHigh(ch,sca) for sca in range(self.NUMBER_OF_SCA)] for ch in range(self.N_CHANNELS_PER_SKIROC)]
        # lowGains=[[self.ADCHigh(ch,sca) for sca in range(self.NUMBER_OF_SCA)] for ch in range(self.N_CHANNELS_PER_SKIROC)]
        #timeSamples=[[self.rollPositons(ch,sca) for sca in range(self.NUMBER_OF_SCA)] for ch in range(self.N_CHANNELS_PER_SKIROC)]
        mydata={'chips':chips,'channels':channels,
              'hg_sca0':hg_sca0,'lg_sca0':lg_sca0,
              'hg_sca1':hg_sca1,'lg_sca1':lg_sca1,
              'hg_sca2':hg_sca2,'lg_sca2':lg_sca2,
              'hg_sca3':hg_sca3,'lg_sca3':lg_sca3,
              'hg_sca4':hg_sca4,'lg_sca4':lg_sca4,
              'hg_sca5':hg_sca5,'lg_sca5':lg_sca5,
              'hg_sca6':hg_sca6,'lg_sca6':lg_sca6,
              'hg_sca7':hg_sca7,'lg_sca7':lg_sca7,
              'hg_sca8':hg_sca8,'lg_sca8':lg_sca8,
              'hg_sca9':hg_sca9,'lg_sca9':lg_sca9,
              'hg_sca10':hg_sca10,'lg_sca10':lg_sca10,
              'hg_sca11':hg_sca11,'lg_sca11':lg_sca11,
              'hg_sca12':hg_sca12,'lg_sca12':lg_sca12,
              'totSlow':totSlow,'totFast':totFast,
              'toaRise':toaRise,'toaFall':toaFall}
        return pd.DataFrame(data=mydata)
    
    def __str__(self):
        stream="CHIP ID = "+str(self.chipID)+",\t rollMask = "+hex(self.rollMask())
        stream=stream+"\n \t ChannelID, LowGain*13, ToARise, ToTSlow \t HighGain*13, ToAFall, ToTFast : "
        for ch in range(self.N_CHANNELS_PER_SKIROC):
            stream=stream+"\n \t\t"+str(ch)+""
            for sca in range(self.NUMBER_OF_SCA):
                stream=stream+" "+str(self.ADCLow(ch,sca))
            stream=stream+" "+str(self.TOARise(ch))
            stream=stream+" "+str(self.TOTSlow(ch))
            stream=stream+"\t\t"
            for sca in range(self.NUMBER_OF_SCA):
                stream=stream+" "+str(self.ADCHigh(ch,sca))
            stream=stream+" "+str(self.TOAFall(ch))
            stream=stream+" "+str(self.TOTFast(ch))
        # stream=stream+"\n \t ChannelID, HighGain*13, ToAFall, ToTFast : "
        # for ch in range(self.N_CHANNELS_PER_SKIROC):
        #     stream=stream+"\n \t\t"+str(ch)+""
        #     for sca in range(self.NUMBER_OF_SCA):
        #         stream=stream+" "+str(self.ADCHigh(ch,sca))
        #     stream=stream+" "+str(self.TOAFall(ch))
        #     stream=stream+" "+str(self.TOTFast(ch))
        return stream

#   bool check(bool printErrors=false)
#   {
#     for( size_t j=0; j<N_CHANNELS_PER_SKIROC; j++ ){
#       uint16_t head=(m_data.at(j)&MASK_HEAD)>>4*3;
#       if(head!=8&&head!=9){
# 	if( printErrors ) std::cout << "ISSUE : we expected 8(1000) or 9(1001) for the adc header and I find " << head << std::endl;
# 	return false;
#       }
#       for( size_t k=0; k<NUMBER_OF_SCA+1; k++){
# 	if( ((m_data.at(j+SCA_SHIFT*k)&MASK_HEAD)>>4*3)!=head ){
# 	  if( printErrors ) std::cout << "\n We have a major issue (LG)-> " << head << " should be the same as " << ((m_data.at(j+SCA_SHIFT*k)&MASK_HEAD)>>4*3) << std::endl;
# 	  return false;
# 	}
#       }
#       head=(m_data.at(j+N_CHANNELS_PER_SKIROC)&MASK_HEAD)>>4*3;
#       if(head!=8&&head!=9){
# 	if( printErrors ) std::cout << "ISSUE : we expected 8(1000) or 9(1001) for the adc header and I find " << head << std::endl;
# 	return false;
#       }
#       for( size_t k=0; k<NUMBER_OF_SCA+1; k++){
# 	if( ((m_data.at(j+SCA_SHIFT*k+N_CHANNELS_PER_SKIROC)&MASK_HEAD)>>4*3)!=head ){
# 	  if( printErrors ) std::cout << "\n We have a major issue (HG)-> " << head << " should be the same as " << ((m_data.at(j+SCA_SHIFT*k+N_CHANNELS_PER_SKIROC)&MASK_HEAD)>>4*3) << std::endl;
# 	  return false;
# 	}
#       }
#     }
#     return true;
#   }
  
# };
