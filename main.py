import math as m

import hexaPlot
import detectorid
import pandas as pd

from optparse import OptionParser
from struct import *
import unpacker,skiroc2cmsdata

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-a", "--radius", dest="radius",action="store",type='int',
                      help="radius of hexagon cells (in cm)",default=0.65)
    parser.add_option("-b", "--fileName", dest="fileName",action="store",
                      help="name for raw data file",default="toto.raw")
    parser.add_option("-c", "--headerSize", dest="headerSize",action="store",type='int',
                      help="number of bytes in header",default=48)
    parser.add_option("-d", "--eventTrailerSize", dest="eventTrailerSize",action="store",type='int',
                      help="number of bytes in header",default=2)
    parser.add_option("-e", "--nSkipEvents", dest="nSkipEvents",action="store",type='int',
                      help="number of event to skip (better to skip 1st event)",default=0)
    parser.add_option("-f","--maxEvents", dest="maxEvents",action="store",type='int',
                      help="maximum number of events to process (0 means no limits)",default=0)
    parser.add_option("-g","--dataNotCompressed", dest="dataNotCompressed",action="store_true",
                      help="",default=False)
    # parser.add_option("-g","", dest="",action="store",type='int',
    #                   help="",default=0)
    
    (options, args) = parser.parse_args()
    print(options)

    eventID=0
    nWords=15392
    if options.dataNotCompressed:
        nWords=30784

    data_unpacker=unpacker.unpacker(not options.dataNotCompressed)

    myDataFrame=pd.DataFrame()
    with open(options.fileName, "rb") as f:
        headerBytes = f.read(options.headerSize)
        myints=unpack('B'*options.headerSize,headerBytes)
        print([hex(i) for i in myints])
        datatoskip=f.read(options.nSkipEvents*(nWords+options.eventTrailerSize))
        rawdata=f.read(nWords+options.eventTrailerSize)
        while rawdata:
            myints=unpack('B'*(nWords+options.eventTrailerSize),rawdata)
            sk2cmsdata=data_unpacker.unpack(myints)
            for iski in sk2cmsdata:
                myDataFrame=myDataFrame.append(iski.dataFrame(),ignore_index=True)
            rawdata=f.read(nWords+options.eventTrailerSize)
            eventID=eventID+1
            if eventID>=options.maxEvents and options.maxEvents!=0:
                break
            if eventID%1==0:
                print("eventID=",eventID)
                
    with open("emap_1layer_v3.txt") as f:
        detids=[]
        for line in f: 
            if "#" in line:
                continue
            words=line.split()
            adetid=detectorid.detid(words)
            detids.append(adetid)

    hexaplot=hexaPlot.hexaPlot(detids,options.radius)

    medians=[]
    iqrs=[]
    for i in detids:
        median=myDataFrame[ (myDataFrame['chips']==i.chip) & (myDataFrame['hg_sca0']>0) & (myDataFrame['channels']==i.channel) ]['hg_sca0'].median()
        medians.append(median)
        iqr=( myDataFrame[ (myDataFrame['chips']==i.chip) & (myDataFrame['hg_sca0']>0) & (myDataFrame['channels']==i.channel) ]['hg_sca0'].quantile(0.84)-myDataFrame[ (myDataFrame['chips']==i.chip) & (myDataFrame['hg_sca0']>0) & (myDataFrame['channels']==i.channel) ]['hg_sca0'].quantile(0.16) )/2
        print(i.chip,i.channel,median,iqr)
        iqrs.append(iqr)

    hexaplot.setValues(medians)
    hexaplot.draw(150,250)
    hexaplot.setValues(iqrs)
    hexaplot.draw(0,10)
