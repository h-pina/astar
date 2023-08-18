import pygame


class Node():
    def __init__(self, position, parent = None) -> None:
        self.position = position
        self.parent = None
        self.traverssed = 0
        self.estimate = 0
        self.sum = 0
        self.possibleNeighbours = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]

    def __eq__(self, __value) -> bool:
        return self.position == __value.position
    
    def __lt__(self, __value) -> bool: # i have to consider both cases 
        return self.sum < __value.sum
    
    def getPossibleNeighbours(self, obstacleList, closedList, worldSize):
        neightbours = []
        notPossibleList = obstacleList + [cell.position for cell in closedList]
        for neightBourDeltas in self.possibleNeighbours:
            neightbourPosition = ( self.position[0] + neightBourDeltas[0],  self.position[1] + neightBourDeltas[1])
            if ( 0 <= neightbourPosition[0] <= worldSize[0] ) and ( 0 <= neightbourPosition[1] <= worldSize[1] ) and (neightbourPosition not in notPossibleList) :
                neightbours.append(Node(neightbourPosition, self))
        return neightbours


class World():
    def __init__(self, worldMaxX, worldMaxY, obstacles ) -> None:
        self.size = (worldMaxX,worldMaxY)
        self.obstacles = obstacles

def aStar(start: Node, end: Node, world: World):
    obstacleList = world.obstacles
    open = [start]
    closed = []
    current = open[open.index(min(open))]
    
    while current != end:
        closed.append(open.pop(open.index(min(open))))
        neighbours = current.getPossibleNeighbours(obstacleList,closed,world.size) 
        for node in neighbours: 
            node.traverssed = current.traverssed+1
            node.estimate = (node.position[1] - end.position[1]) ** 2 + (node.position[0] - end.position[0]) ** 2
            node.sum = node.traverssed + node.estimate
            open.append(node)
        current = open[open.index(min(open))] 
      
    
    path = []
    while current.parent is not None:
        path.append(current.position)
        current = current.parent
    path.append(current.position)
    return path


if __name__ == "__main__":

    #world = World(5, 5, [(2,2), (2,1), (2,3), (2,4),(2,5)] ) #thats why parents are needed, to find only one
    world = World(5, 5, [] ) #thats why parents are needed, to find only one
    start = Node((0,0))
    end = Node((4,4))

    path =  aStar(start, end, world)
    print(path)
    for y in range(world.size[1]+1):
        for x in range(world.size[0]+1):
            if (x,y) in path:
                print("1 ", end="")
            elif (x,y) in world.obstacles:
                print("X ", end="") 
            else:
                print("0 ", end="")
        print()
    