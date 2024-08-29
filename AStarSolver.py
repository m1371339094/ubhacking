import PIL.Image as Image
import math
import heapq
class Node:
    def __init__(self, coordinate, h):
        self.coord = coordinate
        self.parent = None
        self.hValue = h
        '''Heuristics value'''
        self.fValue = math.inf
        '''Distance from start'''



def getEnds(image):
    width, height = image.size

    topRow = 0
    botRow = height - 1

    topCoord: tuple[int, int] = None
    botCoord: tuple[int, int] = None

    for col in range(0, width):
        tCoord = (col, topRow)
        bCoord = (col, botRow)
        if image.getpixel(tCoord) == (255, 255, 255):
            topCoord = tCoord
        if image.getpixel(bCoord) == (255, 255, 255):
            botCoord = bCoord

    return (topCoord, botCoord)

def load_image(file_path):
    image = Image.open(file_path)
    image = image.convert('RGB')
    return image

def create_graph(image, end):
    endX = end[0]
    endY = end[1]
    graph = {}
    

    width, height = image.size
    
    for row in range(0, height):
        for col in range(0, width):

            coord = (col, row)

            if(image.getpixel(coord) == (255, 255, 255)):

                hX = int(math.fabs(col - endX))
                hY = int(math.fabs(row - endY))

                node = Node(coord, hX + hY)
                graph[coord] = node

    return graph

def AStar_check_neighbor(graph, current, neighbor, open, closed,fvalue):
    #Check if the neighbor is in the graph
    if neighbor not in graph:
        return
    if neighbor in closed:
        return
    threshhold=10
    newF = threshhold + graph[neighbor].hValue
    #Check if the f values are less than the old ones
    if(newF < graph[neighbor].fValue) or (neighbor not in open):
        graph[neighbor].parent = current
        graph[neighbor].fValue = newF
        heapq.heappush(open, (newF, neighbor))
        #print(open)

    

def AStar(graph, fcurrent, end, open, closed):
    fvalue,current=fcurrent
    
    closed.add(current)

    if current == end:
        return
    
    north = (current[0], current[1] - 1)
    south = (current[0], current[1] + 1)
    east = (current[0] + 1, current[1])
    west = (current[0] - 1, current[1])

    AStar_check_neighbor(graph, current, north, open, closed,fvalue)
    AStar_check_neighbor(graph, current, south, open, closed,fvalue)
    AStar_check_neighbor(graph, current, east, open, closed,fvalue)
    AStar_check_neighbor(graph, current, west, open, closed,fvalue)

def get_nodes(image):
    
    #Get the start and end points
    start, end = getEnds(image)
    #Create the graph
    graph = create_graph(image, end)
    #Empty open and closed list
    graph[start].fValue = 0
    open = [(0,start)]
    closed = set()
    while end not in closed:
        small=heapq.heappop(open)
        AStar(graph, small, end, open, closed)
    queue = []

    par = end
    while par != None:
        queue.append(par)
        par = graph[par].parent

    return queue

