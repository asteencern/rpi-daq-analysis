import math as m

class detid:
    #CHIP  CHANNEL  layer  module_IX  module_IV  IX  IV  TYPE
    def __init__(self,coord):
        self.chip=(4-int(coord[0])+1)%4
        self.channel=int(coord[1])
        self.layer=int(coord[2])
        self.IU=int(coord[3])
        self.IV=int(coord[4])
        self.iu=int(coord[5])
        self.iv=int(coord[6])
        self.ptype=int(coord[7])

    def __str__(self):
        print("chip, channel, layer, IU, IV, iu, iv, ptype = ",self.chip, self.channel, self.layer, self.IU, self.IV, self.iu, self.iv, self.ptype)
    
class cellCoordinates:
    def __init__(self,cellSide):
        self.cellSide=cellSide
        self.sensorSide = 11*cellSide; # One side of a full 6" sensor(neglecting the cut at the MB)
	self.x_a = m.sqrt(3) / 2; # cosine pi/6
	self.vy_a = 3. / 2;
        self.delta=0

        #Translation in u,v co-ordinates in terms of TB cartesian -x,y.
	self.x0 = 2 * self.x_a * self.cellSide; #Translation in Cartesian x for 1 unit of iu
	self.vx0 = self.x_a * self.cellSide; # Cartesian x component of translation for 1 unit of iv
	self.vy0 = self.vy_a * self.cellSide; # Cartesian y component of translation for 1 unit of iv
        # Translation in Sensor_u, Sensor_v co-ordinates in terms of TB cartesian -x,y.
        self.X0 = 2 * self.x_a * self.sensorSide; #Translation in Cartesian x for 1 unit of Sensor_iu
        self.VX0 = self.x_a * self.sensorSide; # Cartesian x component of translation for 1 unit of Sensor_iv
        self.VY0 = self.vy_a * self.sensorSide; # Cartesian y component of translation for 1 unit of Sensor_iv

    def xy(self,adetid):
        x_y=[0,0]
        if adetid.iu * self.x0 + adetid.iv * self.vx0 < 0 :
            x_y[1]=(adetid.iu * self.x0 + adetid.iv * self.vx0) + self.delta
        else:
            x_y[1]=(adetid.iu * self.x0 + adetid.iv * self.vx0) - self.delta
            
	if adetid.iv * self.vy0 < 0:
            x_y[0]=(adetid.iv * self.vy0) + self.delta
        else:
            x_y[0]=(adetid.iv * self.vy0) - self.delta
        x_y[0]=-x_y[0]
	x_y[0] += adetid.IU*self.X0 + adetid.IV*self.VX0;
        x_y[1] += adetid.IV*self.VY0;
        return x_y
