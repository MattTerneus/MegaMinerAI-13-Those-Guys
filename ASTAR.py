import heapq

def makeGraph(AI):
    graph = [[0 for y in range(AI.getMapHeight())] for x in range(AI.getMapWidth())]
    for droid in AI.droids:
        graph[droid.x][droid.y] = -1
        
    return graph


def aStar(graph, current, end,playerID):
    openSet = set()
    openHeap = []
    closedSet = set()
    parentlist = dict()
    depthlist = dict()
    try:
      graph[end[0]][end[1]] = 0
    except:
      return []

    def retracePath(c):
        path = [c]
        while parentlist.get(c) is not None:
            c = parentlist.get(c)
            path.append(c)
        path.reverse()
        path.pop(len(path)-1)
        return path

    openSet.add(current)
    openHeap.append((0,current))
    depthlist[current] = 0
    while openSet:
        cost, current = heapq.heappop(openHeap)
        if current == end:
            return retracePath(current)
        openSet.remove(current)
        closedSet.add(current)
        for offset in [(-1,0),(1,0),(0,1),(0,-1)]:
            tile = (current[0]+offset[0],current[1]+offset[1])
            if 0 <= tile[0] < len(graph) and 0 <= tile[1] < len(graph[0]):
                if tile not in closedSet and graph[tile[0]][tile[1]] != -1:
                    if tile not in openSet:
                        openSet.add(tile)
                        cost = (abs(end[0]-tile[0])+abs(end[1]-tile[1])) + depthlist[current] + 1
                        heapq.heappush(openHeap, (cost,tile))
                        graph[tile[0]][tile[1]] = cost
                        parentlist[tile] = current
                        depthlist[tile] = depthlist[current] + 1
                    elif graph[tile[0]][tile[1]] > (abs(end[0]-tile[0])+abs(end[1]-tile[1])):
                        cost = (abs(end[0]-tile[0])+abs(end[1]-tile[1])) + depthlist[current] + 1
                        openHeap[openHeap.index((graph[tile[0]][tile[1]], tile))] = cost,tile
                        heapq.heapify(openHeap)
                        graph[tile[0]][tile[1]] = cost
                        parentlist[tile] = current
                        depthlist[tile] = depthlist[current] + 1
    return []