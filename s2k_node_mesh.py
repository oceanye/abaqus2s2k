import re
import scipy.spatial as spt
#import matplotlib.pyplot as plt
import numpy as np


fileHandler = open("test_node_mesh.s2k","r")
listOfLines = fileHandler.readlines()
fileHandler.close()

def part_count(key_word_line,Lines_data):
    k=key_word_line
    while Lines_data[k] != Lines_data[1]:
        k=k+1
    return(k)

def Ext_info(line):
    p=r'(?<==).*?(?= )'
    data=[]
    for i in line:
        data.append(re.findall(p,i))
    data.pop(0)
    return data

def pair_joint_area(j_coord,a_centre):
    for i in range(j_coord):
        x = int(j_coord[0])
        y = int(j_coord[1])
        for j in range(a_centre):
            sqrt()

def convert_joint_coord(data_joint):
    data = []
    for i in data_joint:
        data.append([int(i[0]),int(i[1])])
    array_coord = np.array(data)
    return array_coord


l_t = 0
s2k_data_areas =[]
s2k_data_nodes = []

for line in listOfLines:
    #inp_data[l_t] = line.split(',')
    if "JOINT COORDINATES" in line:
        l_joint = l_t # Node 起始行 l_t ->l_area-1
    elif "CONNECTIVITY - AREA" in line :
        l_area = l_t # Area 起始行 l_area -> l_end -1
    elif "AREA SECTION ASSIGNMENTS" in line:
        l_area_assign =l_t
    l_t=l_t+1
print (l_joint,l_area,l_area_assign)

l_joint_end=part_count(l_joint,listOfLines)
l_area_end=part_count(l_area,listOfLines)
l_area_assign_end=part_count(l_area_assign,listOfLines)
print (l_joint_end,l_area_end,l_area_assign_end)

print(listOfLines[92])
#print(listOfLines[92].count(' Joint'))
# Area=1   NumJoints=4   Joint1=1   Joint2=2   Joint3=3   Joint4=4   Perimeter=4000   AreaArea=1000000   CentroidX=-11500   CentroidY=-11500   CentroidZ=0   GUID=20e4fd85-02f6-413d-a261-0958da29e572
data_area = Ext_info (listOfLines[l_area:l_area_end])
#   Joint=1   CoordSys=GLOBAL   CoordType=Cartesian   XorR=-12000   Y=-12000   Z=0   SpecialJt=No   GlobalX=-12000   GlobalY=-12000   GlobalZ=0   GUID=3bbbe37d-fa25-4ae5-8309-cdeb953592ba
data_joint = Ext_info(listOfLines[l_joint:l_joint_end])
data_area_assign = Ext_info(listOfLines[l_area_assign:l_area_assign_end])

data_area_centre =convert_joint_coord( [data_area[i][8:10] for i in range (0,l_area_end-l_area-2)])
data_joint_coord= convert_joint_coord([data_joint[i][3:5] for i in range (0,l_joint_end-l_joint-2)])
kt = spt.KDTree(data=data_area_centre,leafsize=10)
ckt = spt.cKDTree(data_area_centre)

d,x = kt.query(data_joint_coord)

for i in range(len(data_area_centre)):
    if i ==x[1]:
        fp = data_area_centre[i]

print(data_joint_coord[1])
print(fp)


#print(listOfLines[92].substring[equ[1]:blk[1]])

