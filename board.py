import pygame
import math
import astar
from constants import *
#Setting up the grid
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding")

#Defining colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.width = width
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row,self.col

    def is_visited(self):
        #*Visited node is marked colored as RED
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def mark_visited(self):
        self.color = RED
    
    def mark_open(self):
        self.color = GREEN
    
    def mark_start(self):
        self.color = ORANGE

    def mark_obstacle(self):
        self.color = BLACK

    def mark_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        #* If not an obstacle then add the node to the neighbor list of the current node, Checking in each direction with edge case
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_obstacle(): #* Down
            self.neighbors.append(grid[self.row+1][self.col])
        
        if self.row > 0 and not grid[self.row-1][self.col].is_obstacle(): #* Up
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col > 0 and not grid[self.row][self.col-1].is_obstacle(): #* Left
            self.neighbors.append(grid[self.row][self.col-1])
        
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_obstacle(): #* Right
            self.neighbors.append(grid[self.row][self.col+1])


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

#* Draws the Grid "LINES" in the pygame
def draw_grid_lines(win,rows,width):
    node_width = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*node_width),(width,i*node_width))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*node_width,0),(j*node_width,width))


#* Draw the Grid in pygame, this function is called everytime to update the board
def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win,rows,width)
    pygame.display.update()


#* Returns the position of the node that is clicked in terms of row and col
def get_clicked_pos(pos,rows,width):
    node_width = width//rows
    y,x = pos
    row = y // node_width
    col = x // node_width
    return row,col

def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    start = None
    end = None 
    run = True
    started = False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:   #*Left Button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start and node!=end:
                    start = node
                    start.mark_start()
                
                elif not end and node!=start:
                    end = node
                    end.mark_end()
                
                elif node!=end and node!=start:
                    node.mark_obstacle()

            elif pygame.mouse.get_pressed()[2]:  #*Right Button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors()
                    #TODO: Check without using lambda function
                    astar(lambda:draw(win,grid,ROWS,width),grid,start,end)

    pygame.quit()

main(WIN,WIDTH)