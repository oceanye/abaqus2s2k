import re
import scipy.spatial as spt
#import matplotlib.pyplot as plt
import numpy as np
import math
import os

#file_path ="C://Users//Ye//Documents//PycharmProjects//py2s2k//s2k//test.s2k"
file_path = "C://Users//Ye//Documents//PycharmProjects//py2s2k//s2k//XYS_v1.0 jsj-1.2m-restraint.s2k"



def delLastLine(path):
    with open(path, "rb+") as f:
        lines = f.readlines()  # 读取所有行
        last_line = lines[-1]  # 取最后一行
        if str(last_line).__contains__("END"):
            for i in range(len(last_line) + 2):  ##愚蠢办法，但是有效
                f.seek(-1, os.SEEK_END)
                f.truncate()
    return

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



def convert_joint_coord(data_joint):
    data = []
    for i in data_joint:
        data.append([float(i[0]),float(i[1]),float(i[2])])
    array_coord = np.array(data)
    return array_coord


def gen_body_constraint(file_path,constraint_joints):
    with open(file_path,"a",encoding = 'utf-8') as f:



        f.write("\nTABLE: \"CONSTRAINT DEFINITIONS - BODY\"\n")
        for i in constraint_joints:
            f.write("    Name = BODY"+str(i[0])+"    CoordSys = GLOBAL   UX = Yes   UY = Yes   UZ = Yes   RX = Yes   RY = Yes   RZ = Yes\n")

        f.write("TABLE:  \"JOINT CONSTRAINT ASSIGNMENTS\"\n")
        for i in constraint_joints:
            c_label = str(i[0])
            f.write("   JOINT="+c_label+"   Constraint=BODY"+c_label+"   Type=Body\n")

            print("   JOINT="+c_label+"   Constraint=BODY"+c_label+"   Type=Body")
            for ij in i[1]:
                if int(ij) > 0:
                    f.write("   Joint=" + str(ij) + "   Constraint=BODY"+c_label+"   Type=Body\n")
                    print("   Joint=" + str(ij) + "   Constraint=BODY"+c_label+"   Type=Body")
            print("-----------")
        f.write("\nEND TABLE DATA\n")

    f.close()
    return()



def connect_joint_area(data_joint_label_all,data_frame_joint_label,close_area,joint_area_dist,data_area):
    data_area_label = [data_area[i][0] for i in range(len(data_area))]
    data_area_joint_link = [data_area[i][2:6] for i in range(len(data_area))]
    #[data_joint[i][3:5] for i in range (0,l_joint_end-l_joint-2)]
    data_joint_idx = [data_joint_label_all[i][0] for i in range(len(data_joint_label_all))]
    j_m_r =[]# joint_mesh_relation
    for i in range(len(data_frame_joint_label)):
        #print(close_area[i])
        print(round(i/len(data_frame_joint_label)*100,1),"%，is completed")
        area_item = data_area_label.index(close_area[i])
        #print(close_area[i],area_item)
        area_value = float(data_area[area_item][7])
        try:
            tt=data_area[area_item][2]
            print(tt)
            p1_idx = data_joint_idx.index(data_area[area_item][2])
            p2_idx = data_joint_idx.index(data_area[area_item][3])
            p3_idx = data_joint_idx.index(data_area[area_item][4])
            p4_idx = data_joint_idx.index(data_frame_joint_label[i])
            #print(area_item, p1_idx, p2_idx, p3_idx, i)
            p1 = list(map(float, data_joint_label_all[p1_idx][3:6]))
            p2 = list(map(float, data_joint_label_all[p2_idx][3:6]))
            p3 = list(map(float, data_joint_label_all[p3_idx][3:6]))
            p4 = list(map(float, data_joint_label_all[p4_idx][3:6]))
            # dist = joint_area_dist[i]
            # eqv_r = math.sqrt(area_value)/2
            d1 = point2area_distance(p1, p2, p3, p4)
            if d1 < 50:
                area_j = data_area_joint_link[area_item]
                j_m_r.append([data_joint[i][0], area_j])
                print("area", data_area[area_item][0], "joint,area_joint", data_joint[i][0], area_j, "d1=", d1)

        except Exception as e:
            print('找不到单元'+str(area_item))


    print("total body",len(j_m_r),";",round(len(j_m_r)/len(data_frame_joint_label)*100,1),"%，close joints on srf")

    return(j_m_r)


def define_area(point1, point2, point3):
    """
    法向量    ：n={A,B,C}
    空间上某点：p={x0,y0,z0}
    点法式方程：A(x-x0)+B(y-y0)+C(z-z0)=Ax+By+Cz-(Ax0+By0+Cz0)
    https://wenku.baidu.com/view/12b44129af45b307e87197e1.html
    :param point1:
    :param point2:
    :param point3:
    :param point4:
    :return:（Ax, By, Cz, D）代表：Ax + By + Cz + D = 0
    """
    point1 = np.asarray(point1)
    point2 = np.asarray(point2)
    point3 = np.asarray(point3)
    AB = np.asmatrix(point2 - point1)
    AC = np.asmatrix(point3 - point1)
    N = np.cross(AB, AC)  # 向量叉乘，求法向量
    # Ax+By+Cz
    Ax = N[0, 0]
    By = N[0, 1]
    Cz = N[0, 2]
    D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
    return Ax, By, Cz, D


def point2area_distance(point1, point2, point3, point4):
    """
    :param point1:数据框的行切片，三维
    :param point2:
    :param point3:
    :param point4:
    :return:点到面的距离
    """
    Ax, By, Cz, D = define_area(point1, point2, point3)
    mod_d = Ax * point4[0] + By * point4[1] + Cz * point4[2] + D
    mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
    d = abs(mod_d) / mod_area
    return d



#-----------------------------------
# 使用 open() 函数以只读模式打开我们的文本文件
with open(file_path, 'r',encoding='UTF-8') as file:

	# 使用 read() 函数读取文件内容并将它们存储在一个新变量中
	data = file.read()

	# 使用 replace() 函数搜索和替换文本
	data = data.replace("_\n", "")

# 以只写模式打开我们的文本文件以写入替换的内容
with open(file_path, 'w',encoding='UTF-8') as file:

	# 在我们的文本文件中写入替换的数据
	file.write(data)


fileHandler = open(file_path,"r",encoding = 'utf-8')
listOfLines = fileHandler.readlines()
fileHandler.close()

delLastLine(file_path)


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
    elif "CONNECTIVITY - FRAME" in line:
        l_frame = l_t

    l_t=l_t+1
print (l_joint,l_area,l_area_assign)

l_joint_end=part_count(l_joint,listOfLines)
l_area_end=part_count(l_area,listOfLines)
l_area_assign_end=part_count(l_area_assign,listOfLines)
l_frame_end=part_count(l_frame,listOfLines)
print (l_joint_end,l_area_end,l_area_assign_end)

#print(listOfLines[92])
#print(listOfLines[92].count(' Joint'))
# Area=1   NumJoints=4   Joint1=1   Joint2=2   Joint3=3   Joint4=4   Perimeter=4000   AreaArea=1000000   CentroidX=-11500   CentroidY=-11500   CentroidZ=0   GUID=20e4fd85-02f6-413d-a261-0958da29e572
data_area = Ext_info (listOfLines[l_area:l_area_end])
#   Joint=1   CoordSys=GLOBAL   CoordType=Cartesian   XorR=-12000   Y=-12000   Z=0   SpecialJt=No   GlobalX=-12000   GlobalY=-12000   GlobalZ=0   GUID=3bbbe37d-fa25-4ae5-8309-cdeb953592ba
data_joint_all = Ext_info(listOfLines[l_joint:l_joint_end])

data_area_assign = Ext_info(listOfLines[l_area_assign:l_area_assign_end])
# Frame=3F8   JointI=3505   JointJ=3570   IsCurved=No   Length=13247.7485158898   CentroidX=103009213.993146   CentroidY=16314811.4149305   CentroidZ=-1570.04595486886
data_frame = Ext_info(listOfLines[l_frame:l_frame_end])

# 筛选frame杆端的节点进行分析
data_frame_joint_temp=[data_frame[i][1:3] for i in range (0,l_frame_end-l_frame-1)]
data_frame_joint=[]
for i in data_frame_joint_temp:
    if i not in data_frame_joint:
        data_frame_joint.append(i)

data_joint=[]
temp_id =  [data_joint_all[i][0] for i in range (0,l_joint_end-l_joint-1)]
for i in data_frame_joint:
    print((i[0]))
    try:
        for j in i:
            ind =temp_id .index(j)
            #print(ind)
            data_joint.append(data_joint_all[ind])
            #print(data_joint_all[ind])
    except Exception as e:
        print("找不到匹配节点")



for i in data_area:
    if i[1]=='3':
        i=i.insert(5,'0')

data_area_centre =convert_joint_coord( [data_area[i][8:11] for i in range (0,l_area_end-l_area-1)])
data_joint_coord= convert_joint_coord([data_joint[i][3:6] for i in range (0,len(data_joint))])



kt = spt.KDTree(data=data_area_centre,leafsize=10)
ckt = spt.cKDTree(data_area_centre)

d=[]
x=[]
for joint in data_joint_coord:
    distances, indexes = kt.query(joint, k=2)
    d.append(distances[0])
    x.append(indexes[0])
j_m_num = []
j_m_d=[]
# for i in range(len(data_area_centre)):
#     for j in range(len(x)):
#         if i ==x[j]:
#             j_m_num.append(data_area[i][0])#每个joint所处在area的编号
#             j_m_d.append(d[j])#每个joint所处在area的位置，距离中心点······························


for i in range(len(x)):
    j_m_num.append(data_area[x[i]][0])

j_m_d=d


print(j_m_d)



joint_mesh_relation = connect_joint_area([data_joint_all[i][0:6] for i in range (0,len(data_joint_all))],[data_joint[i][0] for i in range (0,len(data_joint))],j_m_num,j_m_d,data_area)
gen_body_constraint(file_path,joint_mesh_relation)

