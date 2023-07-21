import pygame
from constants import *
import numpy as np
#Setting up the grid
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding")


class Node:
    def __init__(self,row,col,width,total_rows):
        self.last = pygame.time.get_ticks()
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.width = width
        self.neighbors = []
        self.total_rows = total_rows
        self.weight = False
        self.dec_animation = False
        self.cooldown = 300
        self.distance = float('inf')

    def set_distance(self, distance):
        self.distance = distance
    
    def get_distance(self):
        return self.distance
    
    def get_pos(self):
        return self.row,self.col

    def is_visited(self):
        #*Visited node is marked colored as RED
        return self.color == VISIT1

    def is_open(self):
        return self.color == OPEN
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_barrier(self):
        return self.color == BLACK

    def is_weight(self):
        return self.weight

    def is_start(self):
        return self.color == START
    
    def is_end(self):
        return self.color == END

    def is_neutral(self):
        return self.color == WHITE

    def is_looked(self):
        return self.color == LOOK

    def reset(self):
        self.color = WHITE
        self.weight = False

    def make_visit(self):
        if not self.is_weight():
            self.color = VISIT2
        else:
            self.color = VISIT3
    
    def make_open(self):
        if not self.is_weight():
            self.color = OPEN
        else:
            self.color = OPEN1
    
    def make_start(self):
        self.color = START
        self.weight = False

    def make_barrier(self):
        if not self.is_start() and not self.is_end():
            self.color = BLACK
            self.weight = False

    def make_weight(self):
        if not self.is_start() and not self.is_end():
            self.color = BROWN
            self.weight = True

    def make_end(self):
        self.color = RED
        self.weight = False

    def make_path(self):
        if not self.is_weight():
            self.color = PATH1
        else:
            self.color = PATH3

    def looking_at(self):
        self.color = LOOK

    def draw(self, win):
        try:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        except:
            print(self.color)
            input()
    
    def update_neighbors(self, grid, diag = False):
        r = self.row 
        c = self.col
        if r < self.total_rows-1 and not grid[r+1][c].is_barrier():
            self.neighbors.append(grid[r+1][c])
            
        if r > 0 and not grid[r-1][c].is_barrier():
            self.neighbors.append(grid[r-1][c])
            
        if c < self.total_rows-1 and not grid[r][c+1].is_barrier():
            self.neighbors.append(grid[r][c+1])
            
        if c > 0 and not grid[r][c-1].is_barrier():
            self.neighbors.append(grid[r][c-1])
        
        if diag:
            if r < self.total_rows-1 and c < self.total_rows-1 and not grid[r+1][c+1].is_barrier():
                self.neighbors.append(grid[r+1][c+1])

            if r > 0 and c < self.total_rows-1 and not grid[r-1][c+1].is_barrier():
                self.neighbors.append(grid[r-1][c+1])

            if r > 0 and c > 0 and not grid[r-1][c-1].is_barrier():
                self.neighbors.append(grid[r-1][c-1])

            if r < self.total_rows-1 and c > 0 and not grid[r+1][c-1].is_barrier():
                self.neighbors.append(grid[r+1][c-1])

    def __lt__(self,other):
        return False
    
def heuristic(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#* This function creates the board, by creating nodes and storing them in a grid and then returns the grid
def make_grid(rows,width):
    grid = []
    node_width = width // rows
    for i in range(rows):
        grid.append([])             #* Creating Lists to store nodes [[],[],[]]
        for j in range(rows):
            node = Node(i,j,node_width,rows)    #* Creating nodes in each row
            grid[i].append(node)                #* Storing nodes, in the list for each row
    
    return grid




def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return np.array(grid)



#* Draws the Grid "LINES" in the pygame
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows+1):
        pygame.draw.line(win, GREY, (0, i*gap), (rows*gap, i*gap))
    for i in range(rows+1):
        pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, rows*gap))


#* Tells us about the node we click, returning the position of that node in terms of row and col
def get_clicked_pos(pos,rows,width):
    node_width = width//rows
    y,x = pos
    row = y // node_width
    col = x // node_width
    return row,col

def is_free(grid, x, y):
    count = 0
    if y+1 < len(grid) and grid[x][y+1].is_barrier() :
        count +=1
    if y-1>=0 and grid[x][y-1].is_barrier():
        count +=1
    if x+1 < len(grid) and grid[x+1][y].is_barrier():
        count+=1
    if x-1>=0 and grid[x-1][y].is_barrier():
        count+=1
    if count >= 3:
        return True
    return False


def unvisited_n(grid, x, y):
    n = []
    if y+1 < len(grid) and grid[x][y+1].is_barrier() and is_free(grid, x, y+1):
        n.append((x, y+1))
    if y-1>=0 and grid[x][y-1].is_barrier() and is_free(grid, x, y-1):
        n.append((x, y-1))
    if x+1 < len(grid) and grid[x+1][y].is_barrier() and is_free(grid, x+1, y):
        n.append((x+1, y))
    if x-1>=0 and grid[x-1][y].is_barrier() and is_free(grid, x-1, y):
        n.append((x-1, y))
    return n