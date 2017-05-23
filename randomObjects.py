import numpy as np
import pickle
from sys import platform
from pylab import *

# returns 3D bounds of obj
def getObjBounds(objWnid, objID):
    if platform == "linux" or platform == "linux2":
        objectsDirectory='/homes/el216/Workspace/SceneNetData/Objects'
    elif platform == "darwin":
        objectsDirectory='/Users/lingevan/Workspace/SceneNet/SceneNetDataOriginal/Objects'

    objFile = objectsDirectory + '/' + objWnid + '/' + objID \
                + '/models/model_normalized.obj'
    r = open(objFile,'r')
    init = True
    for line in r:
        if line.startswith('v '):
            numStr = line[2:].split()
            vec3 = np.array([float(numStr[0]), float(numStr[1]), 
                             float(numStr[2])])
            if init:
                x_min = vec3[0]
                x_max = vec3[0]
                y_min = vec3[1]
                y_max = vec3[1]
                z_min = vec3[2]
                z_max = vec3[2]
                init = False
            else:
                if vec3[0] < x_min: x_min = vec3[0]
                if vec3[0] > x_max: x_max = vec3[0]
                if vec3[1] < y_min: y_min = vec3[1]
                if vec3[1] > y_max: y_max = vec3[1]
                if vec3[2] < z_min: z_min = vec3[2]
                if vec3[2] > z_max: z_max = vec3[2]

    return x_min, x_max, y_min, y_max, z_min, z_max

def getTmatrix(s, theta_y, d):
    S = np.array([[s[0], 0,    0,    0],
                  [0,    s[1], 0,    0],
                  [0,    0,    s[2], 0],
                  [0,    0,    0,    1]])
    R = np.array([[np.cos(theta_y),0,np.sin(theta_y),0],
                  [0,1,0,0],
                  [-np.sin(theta_y),0,np.cos(theta_y),0],
                  [0,0,0,1]])
    D = np.array([[1, 0, 0, d[0]],
                  [0, 1, 0, d[1]],
                  [0, 0, 1, d[2]],
                  [0, 0, 0,  1 ]])

    T = np.dot(np.dot(D,R),S);
    return T

def getNormalRand(mean, sd):
    while True: 
        rand = np.random.normal(mean, sd)
        if rand > 0: break
    return rand

def cell2WorldCoord(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * (i + 0.5)
    x = origin_ocMap[1] + cellSide * (j + 0.5)
    return np.array([z,x])

def world2CellCoord(world):
    [z,x] = world
    i = int( np.floor((z - origin_ocMap[0]) / cellSide) )
    j = int( np.floor((x - origin_ocMap[1]) / cellSide) )
    return np.array([i,j])

def visualiseMap():
    fig, ax = plt.subplots()

    # define the colormap
    cmap = plt.cm.jet
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmaplist[0] = (.5,.5,.5,1.0)
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

    bounds = np.linspace(0,numRooms+1,numRooms+2)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)
    x = objs_cell[:,1]
    y = objs_cell[:,0]
    plt.scatter(x=x, y=y, c='r', s=10)

    plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
                    ticks=bounds, boundaries=bounds, format='%1i')
    ax.set_title('Rooms Layout with objects')
    savefig('roomsLayout+Objects.png')
    show()
    return

f = open ('fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
 roomsTopLeftCoord, roomsCentreCoord, roomsSize] = pickle.load(f)
f.close()

totalNumObjects = 0
maxIteration = 500

objIDs = []
objWnids = []
Ts = []
scales = []
objs_cell = np.empty((0,2),int)

for r in range(numRooms):
    # numObjects = int(round(getNormalRand(5, 2))) # mean, SD
    numObjects = int(round(getNormalRand(3, 1))) # mean, SD
    room_origin = cell2WorldCoord(roomsTopLeftCoord[r])
    room_zwidth, room_xwidth = roomsSize[r] * cellSide
    print 'Random objects progress: ', round(float(r)/numRooms * 100,2),'%'

    for obj in range(numObjects):
        objID = 'eb073520d0c4db4d346f9a49ab523ba7' #bus
        objWnid = 'SmallObjs'
        x_min, x_max, y_min, y_max, z_min, z_max = getObjBounds(objWnid, objID)
        objSmallestWidth = min(x_max - x_min, z_max - z_min)
        objYwidth = y_max - y_min
        y_height = getNormalRand(0.10,0.025) # in metres
        scale_factor = y_height / objYwidth
        for i in range(maxIteration):
            rand_zx = np.random.rand(2)
            rand_theta_y = np.random.rand()
            buf = objSmallestWidth * scale_factor / 2

            d_zx = (room_origin + [buf,buf]) + \
                    rand_zx * [room_zwidth - 2*buf, room_xwidth - 2*buf]
            theta_y = np.deg2rad(rand_theta_y * 360)
            break

        # d_y = floorHeight - 0.6 * y_height
        d_y = floorHeight

        d = np.array([d_zx[1], d_y, d_zx[0]])
        s = np.array([1.,1.,1.])
        T = getTmatrix(s, theta_y, d)

        objIDs.append(objID)
        objWnids.append(objWnid)
        Ts.append(T[0:3])
        scales.append(y_height)
        objs_cell = np.vstack( (objs_cell,world2CellCoord(d_zx)) )

    totalNumObjects += numObjects

toSave = [totalNumObjects, objIDs, objWnids, scales, Ts]
f = open('fromRandomObjects.pckl','wb')
pickle.dump(toSave, f)
f.close()

print totalNumObjects, 'random objects generated and saved.'

visualiseMap()









