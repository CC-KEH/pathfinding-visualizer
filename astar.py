from queue import PriorityQueue
from board import *

def heuristic(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def algorithm(draw_func,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    #* Inserting F(n) ie FScore,count to keep the check of which node was inserted first,the start node in the open priority queue 
    open_set.put((0,count,start))
    came_from = {}
    #* Assigning G-Score for each node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(),end.get_pos())
