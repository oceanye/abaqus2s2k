fileHandler = open("sys4.inp","r")
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
for line in listOfLines:
    if (l_t > l_area and l_t<l_end):
        temp_area = line.replace(" ", "").strip('\n').split(",")
        inp_data_areas.append(temp_area)
    elif (l_t > l_node and l_t < l_area-1):
        temp_node = line.replace(" ", "").strip('\n').split(",")
        temp_node2 = [int(temp_node[0]),"GLOBAL", "Cartesian",round(float(temp_node[1]), 2),round(float(temp_node[2]), 2),round(float(temp_node[3]), 2)]
        #print(type(temp_node2))
        inp_data_nodes.append(temp_node2)
        #print(temp_node2)
        #print(line)
    l_t = l_t+1

print((inp_data_areas[-1]))
print((inp_data_nodes[-1]))




