import matplotlib.pyplot as plt
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import math as m
import detectorid

def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)

def dot_product(v,w):
    return v[0]*w[0]+v[1]*w[1]

def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]

def vec_length(v):
    return m.sqrt(v[0]*v[0]+v[1]*v[1])

class hexaCell:
    def __init__(self,adetid,radius):
        self.adetid=adetid
        self.radius=radius
        aCellCoordinate=detectorid.cellCoordinates(self.radius)
        self.xy=aCellCoordinate.xy(self.adetid)
        self.hexagon = mpatches.RegularPolygon(xy=[self.xy[0],self.xy[1]], numVertices=6, radius=self.radius, orientation=m.pi/6)
        if self.adetid.ptype==1:
            self.hexagon = mpatches.RegularPolygon(xy=[self.xy[0],self.xy[1]], numVertices=6, radius=self.radius*(2.0/9), orientation=m.pi/6)
        self.value=0
        ## need to transform hexagon into trapezoid for half cells and mouse bite cells
        if self.adetid.ptype==2 or self.adetid.ptype==3:
            vertices_coords = self.hexagon.get_patch_transform().transform(self.hexagon.get_path().vertices[:-1])
            newcoords=[]
            for i in vertices_coords:#add distance from origin for each vertex
                newcoords.append( [i[0],i[1],m.sqrt(i[0]*i[0]+i[1]*i[1])] )
            vertices_coords=newcoords
            vertices_coords=sorted(vertices_coords, key=lambda coord: coord[2])
            #remove the 2 farthest vertices
            vertices_coords.remove(vertices_coords[len(vertices_coords)-1])
            vertices_coords.remove(vertices_coords[len(vertices_coords)-1])
            barycenter=[0,0]
            for i in vertices_coords:
                barycenter[0]+=i[0]
                barycenter[1]+=i[1]

            barycenter=[i/len(vertices_coords) for i in barycenter]
            #print barycenter
            ux=[1,0]
            for i in vertices_coords:
                vec=[i[0]-barycenter[0],i[1]-barycenter[1]]
                costheta=dot_product(vec,ux)/vec_length(vec)/vec_length(ux)
                theta=m.acos(costheta)
                if determinant(vec,ux)>0:
                    theta=2*m.pi-theta
                i[2]=theta
            
            vertices_coords=sorted(vertices_coords, key=lambda coord: coord[2])
            trapcoords=[[i[0],i[1]] for i in vertices_coords]
            trapezoid = mpatches.Polygon(xy=trapcoords,fill=None)
            self.hexagon=trapezoid #hehe

    def detid(self):
        return self.adetid
    
    def xy(self):
        return self.xy

    def setValue(self,value):
        self.value=value

    def getValue(self):
        return self.value

class hexaPlot:
    def __init__(self,detids,radius):
        self.detids=detids
        self.patches=[]
        self.hexaCells=[]
        self.radius=radius
        # add a Hexagon
        for i in detids:
            ahexacell=hexaCell(i,self.radius)
            self.hexaCells.append(ahexacell)
        self.nCells=len(self.hexaCells)
        
    def setLabels(self,option):
        for i in self.hexaCells:
            xpos=i.xy[0]
            ypos=i.xy[1]
            if i.detid().ptype==1:
                ypos=ypos+ypos/10.0
            elif i.detid().ptype==4:
                ypos=ypos-ypos/10.0
            if option=="cellID":
                label([xpos,ypos], str(1000*(i.detid().chip)+i.detid().channel))
            if option=="values":
                label([xpos,ypos], i.value)

    def setValues(self,values):
        try:
            for i in range(len(values)):
                self.hexaCells[i].setValue(values[i])
        except:
            raise SystemExit('Wrong number of values in hexaPlot::setValues(), must be the same as number of hexaCells')

    def draw(self,vmin=0,vmax=100):
        fig, ax = plt.subplots()
        patches=[]
        colors=[]
        hexagon = mpatches.RegularPolygon(xy=[0,0], numVertices=6, radius=11*self.radius, orientation=m.pi/6) #11 only for 6 inch sensor with 128 silicon pads
        patches.append(hexagon)
        colors.append(vmin)
        for i in self.hexaCells:
            colors.append(i.value)
            patches.append(i.hexagon)

        #self.setLabels("cellID")
        self.setLabels("values")
    
        collection = PatchCollection(patches,cmap=plt.cm.Blues)
        collection.set_array(np.array(colors))
        collection.set_clim(vmin,vmax)
        ax.add_collection(collection)
        plt.axis('equal')
        #plt.axis('off')
        plt.tight_layout()
        plt.show()
