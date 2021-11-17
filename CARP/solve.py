import read_data as rd
from gurobipy import Model,GRB,quicksum


def solve(nNodes,nEdges,nVehicles,depot,capacity,edges,costs,demand):

    M = 10*10
    #nVehicles = 1
    #add reverse edges
    onewayEdges = edges[:]
    for edge in onewayEdges:
        edges.append((edge[1],edge[0]))
        costs[(edge[1],edge[0])] = costs[(edge[0],edge[1])]
        demand[(edge[1],edge[0])] = demand[(edge[0],edge[1])]
    # #add zero edge (= dont use the vehicle)
    # edges.append((0,0))
    # costs[(0,0)] = 0
    # demand[(0,0)] = 0
    

    model = Model("CARP")
    model.modelSense = GRB.MINIMIZE

    #Vars
    x = {}
    "x_edge,k = 1 iff vehicle k uses edge"
    for k in range(nVehicles):
        for edge in edges:
            x[edge[0],edge[1],k] = model.addVar(vtype=GRB.BINARY, name="x_(%s,%s),%s"%(edge[0],edge[1],k))
            
    z = {}
    "z_edge,k = 1 iff vehicle k serves edge"
    for k in range(nVehicles):
        for edge in edges:
            z[edge[0],edge[1],k] = model.addVar(vtype=GRB.BINARY, name="z_(%s,%s),%s"%(edge[0],edge[1],k))
            
    f = {}
    "subtour elimination"
    for k in range(nVehicles):
        for edge in edges:
            f[edge[0],edge[1],k] = model.addVar(vtype=GRB.CONTINUOUS,lb=0, name="f_(%s,%s),%s"%(edge[0],edge[1],k))

    #objective function
    model.setObjective(quicksum(x[edge[0],edge[1],k] * costs[(edge[0],edge[1])] for k in range(nVehicles) for edge in edges)#+
                       #quicksum(z[edge[0],edge[1],k] * costs[(edge[0],edge[1])] for k in range(nVehicles) for edge in edges)
                       )

    
    #Constraints
    "each vehicle starts at the depot"
    for k in range(nVehicles):
        model.addConstr(quicksum(x[depot,edge[1],k] for edge in (e for e in edges if e[0] == depot)) == 1)
    "each vehicle ends at the depot"
    for k in range(nVehicles):
        model.addConstr(quicksum(x[edge[0],depot,k] for edge in (e for e in edges if e[1] == depot)) == 1)
    
    "flow conservation"
    for k in range(nVehicles):
        for node in range(nNodes):
            model.addConstr(quicksum(x[edge[0],node,k] for edge in (e for e in edges if e[1] == node)) - quicksum(x[node,edge[1],k] for edge in (e for e in edges if e[0] == node)) == 0)

    "link x and z"
    for k in range(nVehicles):
        for edge in edges:
            model.addConstr(z[edge[0],edge[1],k] <= x[edge[0],edge[1],k])

    "respect the capacity"
    for k in range(nVehicles):
        model.addConstr(quicksum(z[edge[0],edge[1],k] * demand[(edge[0],edge[1])] for edge in edges) <= capacity)

    "serve every edge with demand"
    for edge in onewayEdges:
        model.addConstr(M*quicksum(z[edge[0],edge[1],k] for k in range(nVehicles)) + M*quicksum(z[edge[1],edge[0],k] for k in range(nVehicles)) >= demand[(edge[0],edge[1])])

    "subtour elimination"
    for k in range(nVehicles):
        for edge in edges:
            model.addConstr(f[edge[0],edge[1],k] <= M*x[edge[0],edge[1],k])

    for k in range(nVehicles):
        for node in range(1,nNodes):
            model.addConstr(quicksum(f[node,edge[1],k] for edge in [e for e in edges if(e[0] == node)]) - quicksum(f[edge[0],node,k] for edge in [e for e in edges if(e[1] == node)]) == quicksum(z[node,edge[1],k] for edge in [e for e in edges if(e[0] == node)]))

    #print(depot)

    model.update()
    model.write('model.lp')
    model.optimize()

    
    if model.status == GRB.OPTIMAL:
        print(depot)
        for k in range(nVehicles):
            c = 0
            d = 0
            route = []
            print("Route %s"%(k))

            for edge in edges:
                if(x[edge[0],edge[1],k].x != 0):
                    c = c + costs[edge[0],edge[1]]
                    #print("x %s, %s"%(edge[0],edge[1]))
                    route.append((edge[0],edge[1]))
                    #route.append((chr(edge[0]+97),chr(edge[1]+97)))
            for edge in edges:    
                if(z[edge[0],edge[1],k].x != 0):
                    d = d + demand[edge[0],edge[1]]
                    #print("z %s, %s"%(edge[0],edge[1]))
            print(route)
            print("Demand of route: %s"%(d))
            #print("Costs of route: %s"%(c))
            print("\n")
        



if __name__ == "__main__":
    #path = "./Instanzen/1B.dat"
    path = "./Instanzen/C01.dat"
    #path = "./Instanzen/Pearn.dat"
    nNodes,nEdges,nVehicles,depot,capacity,edges,costs,demand = rd.readData(path)

    solve(nNodes,nEdges,nVehicles,depot,capacity,edges,costs,demand)