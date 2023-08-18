import numpy as np

class Node():
    def __init__(self, position, parent=None, g=0, h=0, f=0) -> None:
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f
    
    def __eq__(self, __value) -> bool:
        return self.position == __value.position
    


def getNextCell(open):
    fValuesArr = [x.f for x in open]
    idxs = [i for i, v in enumerate(fValuesArr) if v == min(fValuesArr)]
    minCells = [open[i] for i in idxs]
    if len(minCells) > 1:
        hValuesArr = [x.h for x in minCells ]
        return minCells[hValuesArr.index(min(hValuesArr))]
    else:
        return minCells[0]


class World():
    def __init__(self, size) -> None:
        self.size = size
        pass

    def getNeighbours(self, cell,end,closed,obstacles):
        deltas = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
        neighbours = []
        for delta in deltas:
            position = (cell.position[0] + delta[0], cell.position[1] + delta[1])
            notAllowed = obstacles + [x.position for x in closed]
            if (position not in notAllowed ) and (0 <= position[0] < self.size[0]) and (0 <= position[1] < self.size[1]) :
                g = cell.g+1
                h = (end.position[1] - position[1])**2 + (end.position[0] - position[0])**2
                f = h + g
                neighbours.append(Node(position,cell,g,h,f))
        return neighbours
        
        

def aStar(start, end, obstacles, world):
    open = [start]
    closed = []
    current = getNextCell(open)
    while current != end:
        closed.append(open.pop(open.index(current)))
        availableNeighbours = world.getNeighbours(current, end,closed,obstacles) # return new Cells with values calculated
        for n in availableNeighbours:
            if n in open and n.f < open[open.index(n)].f:
                #parent already updated
                open[n] = n
            if n not in open:
                open.append(n)
        current = getNextCell(open)
    closed.append(current)

    path = []
    cell = closed[-1]
    while cell.parent:
        path.append(cell.position)
        cell = cell.parent
    path.append(cell.position)
    print([x.position for x in closed])
    return path[::-1]        


world = World((20,20))
start = Node((0,0))
end = Node((18,18))
obstacles = [(2,2), (2,1), (2,3), (2,4),(2,5)]
path =  aStar(start, end,obstacles,world)
print(path)
# for y in range(world.size[1]+1):
#     for x in range(world.size[0]+1):
#         if (x,y) in path:
#             print("1 ", end="")
#         elif (x,y) in world.obstacles:
#             print("X ", end="") 
#         else:
#             print("0 ", end="")
#     print()
