#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for Abaqus inp file
fileHandler = open("output_cxt.inp","r")
listOfLines = fileHandler.readlines()
fileHandler.close()

l_t = 0
inp_data_areas =[]
inp_data_nodes = []
for line in listOfLines:
    #inp_data[l_t] = line.split(',')
    if "*NODE" in line:
        l_node = l_t # Node 起始行 l_t ->l_area-1
    elif "*ELEMENT" in line :
        l_area = l_t # Area 起始行 l_area -> l_end -1
    elif "*****" in line:
        l_end =l_t
    l_t=l_t+1
print (l_node,l_area,l_end)

l_t = 0
dec = 4
for line in listOfLines:
    if (l_t > l_area and l_t<l_end):
        temp_area = line.replace(" ", "").strip('\n').split(",")
        inp_data_areas.append(temp_area)
    elif (l_t > l_node and l_t < l_area-0):
        temp_node = line.replace(" ", "").strip('\n').split(",")
        temp_node2 = [int(temp_node[0]),"GLOBAL", "Cartesian",round(float(temp_node[1]), dec),round(float(temp_node[2]), dec),round(float(temp_node[3]), dec)]
        inp_data_nodes.append(temp_node2)
        #print(temp_node2)
        #print(line)
    l_t = l_t+1

######################


#for Rhino-Grasshopper


def create_joint_objects(joints):
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 功能：创建节点对象
    # 参数：joints为节点信息列表，其内元素为单个结点对象信息列表，依次表示节点标签、坐标系名称、坐标系类型、点的三个坐标值。
    # 返回：无
    # jointnum = len(joints)  # 节点总数
    # dictkeys = s2kDatabase.keys() # 字典键名
    for joint in joints:
        label, coordcsys, coordtype, x, y, z = joint[0], joint[1], joint[2], joint[3], joint[4], joint[5]
        # 节点标签、坐标系编号、坐标系类型、坐标值
        coordSys, coordType = ["GLOBAL", ], ["Cartesian", ]
        if coordcsys not in coordSys:
            coordcsys = "GLOBAL"
        if coordtype not in coordType:
            coordtype = "Cartesian"
        s = "   Joint=%s   CoordSys=%s   CoordType=%s   XorR=%s   Y=%s   Z=%s" % (label, coordcsys, coordtype, x, y, z)
        global s2kDatabase  # 全局变量/s2k文件数据库
        s2kDatabase["JOINT COORDINATES"].append(s)


def create_frame_objects(frames):
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 功能：创建框架对象/直线框架
    # 参数：frames为框架对象信息列表，其内元素为单个框架对象信息列表，依次表示框架编号、框架起点编号、框架终点编号
    # 返回：无
    for frame in frames:
        label, joini, jointj = frame[0], frame[1], frame[2]  # 框架编号、框架起点编号、框架终点编号
        s = "   Frame=%s   JointI=%s   JointJ=%s" % (label, joini, jointj)
        global s2kDatabase  # 全局变量/s2k文件数据库
        s2kDatabase["CONNECTIVITY - FRAME"].append(s)



def create_area_objects(areas):
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 功能：创建面对象/平面对象
    # 参数：areas为框面对象信息列表，其内元素为单个面对象信息列表，依次表示面对象编号、组成面对象的结点标签（顺/逆时针排列）
    # 返回：无
    for area in areas:
        arealabel = area[0]  # 面对象的标签
        jointlabels = area[1:]  # 组成面对象的节点标签列表
        numjoints = len(jointlabels)
        rst1, rst2 = numjoints // 4, numjoints % 4  # 整数、余数
        global s2kDatabase  # 全局变量/s2k文件数据库
        if rst1 == 0:
            if rst2 == 3:
                # 三角形板
                joint1, joint2, joint3 = jointlabels[0], jointlabels[1], jointlabels[2]
                s1 = "   Area=%s   NumJoints=3   Joint1=%s   Joint2=%s   Joint3=%s   Order=1" % (arealabel, joint1, joint2, joint3)
                s2kDatabase["CONNECTIVITY - AREA"].append(s1)
        else:
            joint1, joint2, joint3, joint4 = jointlabels[:4]
            s1 = "   Area=%s   NumJoints=%s   Joint1=%s   Joint2=%s   Joint3=%s   Joint4=%s   Order=1" % (arealabel, numjoints, joint1, joint2, joint3, joint4)
            s2kDatabase["CONNECTIVITY - AREA"].append(s1)
            for k in range(rst1 - 1):
                i, j = int(4 * (k + 1)), int(4 * (k + 1) + 4)
                joint1, joint2, joint3, joint4 = jointlabels[i:j]
                s2 = "   Area=%s   Joint1=%s   Joint2=%s   Joint3=%s   Joint4=%s   Order=%s" % (arealabel, joint1, joint2, joint3, joint4, int(k+1))
                s2kDatabase["CONNECTIVITY - AREA"].append(s2)
            if rst2 > 0:
                s3 = "   Area=%s" % arealabel
                for k in range(rst2):
                    index = int(-rst2 + k)
                    jointlabel = jointlabels[index]
                    s4 = "   Joint%s=%s" % (int(k + 1), jointlabel)
                    s3 = s3 + s4
                s3 = s3 + "   Order=%s" % int(rst1 + 1)
                s2kDatabase["CONNECTIVITY - AREA"].append(s3)


def create_solid_objects(solids):
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 功能：创建体对象/8节点体对象
    # 参数：solids为体对象信息列表，其内元素为单个体对象信息列表，依次表示体对象的编号、组成体对象的结点标签（顺序排列）
    # 返回：无
    for solid in solids:
        solidlabel = solid[0]  # 体对象的标签
        jointlabels = solid[1:]  # 组成体对象的节点标签列表
        numjoints = len(jointlabels)
        global s2kDatabase  # 全局变量/s2k文件数据库
        if numjoints == 8:
            joint1, joint2, joint3, joint4 = jointlabels[0], jointlabels[1], jointlabels[2], jointlabels[3]
            joint5, joint6, joint7, joint8 = jointlabels[4], jointlabels[5], jointlabels[6], jointlabels[7]
            s = "   Solid=%s   Joint1=%s   Joint2=%s   Joint3=%s   Joint4=%s   Joint5=%s   Joint6=%s   Joint7=%s   Joint8=%s" % (solidlabel, joint1, joint2, joint3, joint4, joint5, joint6, joint7, joint8)
            s2kDatabase["CONNECTIVITY - SOLID"].append(s)


def create_s2k_file(path, data):
    # 作者：DalNur；邮箱：liyang@alu.hit.edu.cn
    # 功能：创建s2k文件
    # 参数：path为创建的s2k文件绝对路径；data为s2k文件数据库。
    # 返回：创建的s2k文件绝对路径。
    import time
    currtime = time.localtime()
    currtime = time.strftime("%Y-%m-%d %H:%M:%S", currtime)
    with open(path, 'w') as f:
        # 01-书写标题数据块及项目控制数据块
        dtname = "Heading"
        line1 = data[dtname][0]
        s1, s2 = "D:\SAPWorkDir\JN-GTC.s2k", path
        line1.replace(s1, s2)
        line2 = data[dtname][1]
        line3 = data[dtname][2]
        # line4 = data[dtname][3]
        # s1, s2 = "2021-09-18 11:11:59", currtime
        # line4.replace(s1, s2)
        line4 = "Time: %s." % currtime
        f.write(line1 + "\n")  # 写入数据
        f.write(line2 + "\n")  # 写入数据
        f.write(line3 + "\n")  # 写入数据
        f.write(line4 + "\n")  # 写入数据
        f.write("" + "\n")  # 数据块尾部空行
        dtname = "PROGRAM CONTROL"
        f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
        for line in data[dtname]:
            f.write(line + "\n")  # 写入数据
        f.write("" + "\n")  # 数据块尾部空行
        # 02-书写坐标系数据块
        dtname = "COORDINATE SYSTEMS"
        f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
        for line in data[dtname]:
            f.write(line + "\n")  # 写入数据
        f.write("" + "\n")  # 数据块尾部空行
        # 03-书写默认材料属性数据块
        dtnames = ["MATERIAL PROPERTIES 01 - GENERAL", "MATERIAL PROPERTIES 02 - BASIC MECHANICAL PROPERTIES",
                   "MATERIAL PROPERTIES 03A - STEEL DATA", ]
        for dtname in dtnames:
            f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
            for line in data[dtname]:
                f.write(line + "\n")  # 写入数据
            f.write("" + "\n")  # 数据块尾部空行
        # 04-书写默认截面属性数据块
        dtnames = ["FRAME SECTION PROPERTIES 01 - GENERAL", "AREA SECTION PROPERTIES", "SOLID PROPERTY DEFINITIONS", ]
        for dtname in dtnames:
            f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
            for line in data[dtname]:
                f.write(line + "\n")  # 写入数据
            f.write("" + "\n")  # 数据块尾部空行
        # 05-书写对象数据块/点对象/面对象/体对象
        dtnames = ["JOINT COORDINATES", "CONNECTIVITY - FRAME", "CONNECTIVITY - AREA", "CONNECTIVITY - SOLID"]
        for dtname in dtnames:
            if len(data[dtname]) > 0:
                f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
                for line in data[dtname]:
                    f.write(line + "\n")  # 写入数据
                f.write("" + "\n")  # 数据块尾部空行
        # 06-书写对象分组数据块/点对象分组/面对象分组/体对象分组
        dtnames = ["GROUPS 1 - DEFINITIONS", "GROUPS 2 - ASSIGNMENTS", ]
        for dtname in dtnames:
            if len(data[dtname]) > 0:
                f.write("TABLE:  " + '"' + dtname + '"' + "\n")  # 数据块表表头
                for line in data[dtname]:
                    f.write(line + "\n")  # 写入数据
                f.write("" + "\n")  # 数据块尾部空行
    return path





"""
    =================================
    Author: DalNur/LiYang
    Email: liyang@alu.hit.edu.cn
    Date: 2021/09/18 11:11:59 Beijing
    =================================
"""

s2kDatabase = {}  # SAP2000 s2k 文件数据库
s2kDatabase = {"JOINT COORDINATES": [], "CONNECTIVITY - FRAME": [], "CONNECTIVITY - AREA": [],
               "CONNECTIVITY - SOLID": [], "GROUPS 1 - DEFINITIONS": [], "GROUPS 2 - ASSIGNMENTS": []}


"01-标题数据块"

s2kDatabase["Heading"] = ["File D:\SAPWorkDir\JN-GTC.s2k was saved on m/d/yy at h:mm:ss",
                          "Hello, world! This s2k file was created by python.",
                          "Author: DalNur/LiYang; Email: liyang@alu.hit.edu.cn",
                          "Time: 2021-09-18 11:11:59."]  # 标题


"02-项目数据块"

s2kDatabase["PROGRAM CONTROL"] = ['   ProgramName=SAP2000   Version=21.0.2   CurrUnits="N, mm, C"',]  # 软件版本与单位制


"03-坐标系数据块"

s2kDatabase["COORDINATE SYSTEMS"] = [
    '   Name=GLOBAL   Type=Cartesian   X=0   Y=0   Z=0   AboutZ=0   AboutY=0   AboutX=0',]  # 坐标系


"04-默认材料属性数据块"

s2kDatabase["MATERIAL PROPERTIES 01 - GENERAL"] = [
    "   Material=DalNur   Type=Steel   SymType=Isotropic   TempDepend=No   Color=Blue",]
s2kDatabase["MATERIAL PROPERTIES 02 - BASIC MECHANICAL PROPERTIES"] = [
    "   Material=DalNur   UnitWeight=76.970   UnitMass=7.849   E1=200000000.000   G12=76923076.9230769   U12=0.3   A1=6.5E-09",]
s2kDatabase["MATERIAL PROPERTIES 03A - STEEL DATA"] = [
    "   Material=DalNur   Fy=345000.000   Fu=490000.000   EffFy=379500.000   EffFu=539000.000   SSCurveOpt=Simple   SSHysType=Kinematic   SHard=0.015   SMax=0.11   SRup=0.17   FinalSlope=-0.1",]
s2kDatabase["MATERIAL PROPERTIES 06 - DAMPING PARAMETERS"] = [
    "   Material=DalNur   ModalRatio=0   VisMass=0   VisStiff=0   HysMass=0   HysStiff=0",]


"05-1 默认框架截面属性数据块"

s2kDatabase["FRAME SECTION PROPERTIES 01 - GENERAL"] = [
    "    SectionName=P400x20   Material=DalNur   Shape=Pipe   t3=400   tw=20   Area=0   TorsConst=0   I33=0   I22=0   I23=0   AS2=0 _",
    "         AS3=0   S33=0   S22=0   Z33=0   Z22=0   R33=0   R22=0   ConcCol=No   ConcBeam=No   Color=Blue _",
    "         TotalWt=0   TotalMass=0   FromFile=No   AMod=1   A2Mod=1   A3Mod=1   JMod=1   I2Mod=1   I3Mod=1   MMod=1   WMod=1"]


"05-2 默认板壳截面属性数据块"

s2kDatabase["AREA SECTION PROPERTIES"] = [
    "    Section=S150   Material=DalNur   MatAngle=0   AreaType=Shell   Type=Shell-Thin   DrillDOF=Yes   Thickness=150   BendThick=150   Color=Blue   F11Mod=1   F22Mod=1   F12Mod=1   M11Mod=1   M22Mod=1   M12Mod=1   V13Mod=1   V23Mod=1 _",
    "         MMod=1   WMod=1", ]

"05-3 默认实体截面属性数据块"

s2kDatabase["SOLID PROPERTY DEFINITIONS"] = [
    "    SolidProp=DalNur   Material=DalNur   MatAngleA=0   MatAngleB=0   MatAngleC=0   InComp=Yes   Color=Blue   TotalWt=0   TotalMass=0", ]



length, width, height = 20, 10, 5
x1, x2 = -0.5 * length, 0.5 * length
y1, y2 = -0.5 * width, 0.5 * width
z1, z2 = 0, height




joint1 = [1, "GLOBAL", "Cartesian", 14649.432948, 26802.725511, 13150.0]  # 1号节点
joint2 = [2, "GLOBAL", "Cartesian", 15968.658752, 28686.775213, 13150.0]  # 2号节点
joint3 = [3, "GLOBAL", "Cartesian", 8513.710794, 33906.78597, 13150.0]  # 3号节点
joint4 = [4, "GLOBAL", "Cartesian", 13790.614008, 41442.984778, 13150.0]  # 4号节点
joint5 = [5, "GLOBAL", "Cartesian", 22064.714011, 35649.397584, 13150.0]  # 5号节点
joint6 = [6, "GLOBAL", "Cartesian", 21376.422287, 34666.415131, 13150.0]  # 6号节点
joint7 = [7, "GLOBAL", "Cartesian", 23751.963215, 33003.043466, 13150.0]  # 7号节点
joint8 = [8, "GLOBAL", "Cartesian", 20884.081034, 28907.283244, 13150.0]  # 8号节点
joint9 = [9, "GLOBAL", "Cartesian", 20392.589807, 29251.429106, 13150.0]  # 9号节点
joint10 = [10, "GLOBAL", "Cartesian", 17352.634694, 24909.923271, 13150.0]  # 10号节点
joint11 = [11, "GLOBAL", "Cartesian", 8095.892249, 33833.113288, 13450.0]  # 11号节点
joint12 = [12, "GLOBAL", "Cartesian", 0, y2, z2]  # 12号节点
joint13 = [13, "GLOBAL", "Cartesian", 0, 0, z2]  # 13号节点
joint14 = [14, "GLOBAL", "Cartesian", 0, 0, z1]  # 14号节点
joint15 = [15, "GLOBAL", "Cartesian", x1, 0, z1]  # 15号节点
joint16 = [16, "GLOBAL", "Cartesian", 0, y1, z1]  # 16号节点
joint17 = [17, "GLOBAL", "Cartesian", x2, 0, z1]  # 17号节点
joint18 = [18, "GLOBAL", "Cartesian", 0, y2, z1]  # 18号节点
joints = [joint1, joint2, joint3, joint4, joint5, joint6, joint7,
          joint8, joint9, joint10, joint11, joint12, joint13,
          joint14, joint15, joint16, joint17, joint18, ]



area1 = [1, 1, 2, 3, 4,5,6,7,8,9,10]  # 1号面对象/组成节点编号5、9、13和12
#area2 = [2, 10, 7, 11, 13]  # 2号面对象/组成节点编号4、7、11和13
areas = [area1]
create_area_objects(inp_data_areas)  # 写入数据库
create_joint_objects(inp_data_nodes)  # 写入数据库

#Test command
#create_area_objects(areas)  # 写入数据库
#create_joint_objects(joints)  # 写入数据库


#print(type(inp_data_areas[0]))
#print(type(area1))


#path = r"C:\Users\ocean\Documents\Project\徐汇滨江\沉香亭\ctx-4.0\ctx_v4_srf.s2k"  # 新建s2k文件的绝对路径
path = r"ctx_v4_srf.s2k"
data = s2kDatabase  # s2k数据库
create_s2k_file(path, data)


