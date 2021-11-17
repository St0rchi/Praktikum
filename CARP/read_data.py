
def readData(path):
    """read the data file from "The Capacitatted Arc Routing Problem. Lower Bounds"
    Args:
        path (string): path of the file
    Returns:
        nNodes      (int) : number of nodes
        nEdges      (int) : number of edges
        nVehicles   (int) : number of vehicles
        capacity    (int) : capacity
        edges       (list): list of edges e.g. (node1,node2)
        costs       (dict): cost of edges
        demand      (dict): demand of edges
    """

    rawData = []
    with open(path) as fp:
        line = fp.readline()
        while(line != ""):
            rawData.append(line.strip("\n"))
            line = fp.readline()

    nEdgesREQ = 0
    nEdgesNOREQ = 0

    for count,line in enumerate(rawData):
        if(line[:8] == "VERTICES"):
            nNodes = int(line[10:])
        if(line[:11] == "ARISTAS_REQ"):
            nEdgesREQ = int(line[13:])
        if(line[:13] == "ARISTAS_NOREQ"):
            nEdgesNOREQ = int(line[15:])
        if(line[:9] == "VEHICULOS"):
            nVehicles = int(line[11:])
        if(line[:9] == "CAPACIDAD"):
            capacity = int(line[11:])
        if(line == "LISTA_ARISTAS_REQ :"):
            dataSectionREQ = count+1
        if(nEdgesNOREQ != 0):
            if(line == "LISTA_ARISTAS_NOREQ :"):
                dataSectionNOREQ = count+1
                #print(dataSection)
        if(line[:8]=="DEPOSITO"):
            depot = int(line[10:])-1


    edges = []
    costs = {}
    demand = {}
    if(nEdgesREQ != 0):
        for line in rawData[dataSectionREQ:dataSectionREQ+nEdgesREQ]:
            node1 = int(line[1:8].split(",")[0])-1
            node2 = int(line[1:8].split(",")[1])-1

            edges.append((node1,node2))
            costs[(node1,node2)] = int(line[17:26])
            demand[(node1,node2)] = int(line[33:])

    if(nEdgesNOREQ != 0):
        for line in rawData[dataSectionNOREQ:dataSectionNOREQ+nEdgesNOREQ]:
            node1 = int(line[1:8].split(",")[0])-1
            node2 = int(line[1:8].split(",")[1])-1

            edges.append((node1,node2))
            costs[(node1,node2)] = int(line[17:26])
            demand[(node1,node2)] = 0
        
    return nNodes,nEdgesREQ+nEdgesNOREQ,nVehicles,depot,capacity,edges,costs,demand
    
    
    

if __name__ == "__main__":
    #path ="./Instanzen/Pearn.dat"
    #path="./Instanzen/1A.dat"
    path="./Instanzen/C01.dat"
    nNodes,nEdges,nVehicles,depot,capacity,edges,costs,demand = readData(path)

    #print the data
    # for edge in edges:
    #     print("%s, %s \tcost: %s \tdemand: %s"%(edge[0],edge[1],costs[edge],demand[edge]))