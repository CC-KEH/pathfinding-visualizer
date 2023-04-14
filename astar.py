import pygame
import math
from queue import PriorityQueue

#Setting up the board
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption(title="A* Algorithm")

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
        return self.color == PURPLE
    
    def reset(self):
        return self.color == WHITE
    
    