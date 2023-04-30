import pygame
from queue import PriorityQueue
from constants import *
from board import *
from system import *

class button():
    def __init__(self, x, y,width,height, text=''):
        self.color = BUTTON_COLOR
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            pygame.draw.circle(win, outline, (self.x, self.y+self.height//2), self.height//2+2)
            pygame.draw.circle(win, outline, (self.x+self.width, self.y+self.height//2), self.height//2+2)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        pygame.draw.circle(win, self.color, (self.x, self.y+self.height//2), self.height//2)
        pygame.draw.circle(win, self.color, (self.x+self.width, self.y+self.height//2), self.height//2)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 35)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_hover(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x-self.height//2 and pos[0] < self.x + self.width+self.height//2:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class screen():
    def __init__(self, x,y,width,height, text=''):
        self.color = SCREEN_COLOR
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label1 = ""
        self.text1 = text
        self.text2 = ""
        self.text3 = ""
        
    def set_label1(self, label):
        self.label1 = label
    
    def set_text1(self, text):
        self.text1 = text
    def set_text2(self, text):
        self.text2 = text
    def set_text3(self, text):
        self.text3 = text
        
    def get_text1(self):
        return self.text1

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.label1 != '':
            font = pygame.font.SysFont('sans', 20)
            label = font.render(self.label1, 1, (0,0,0))
            win.blit(label, (self.x + 10, self.y + 10))
        
        if self.text1 != '':
            font = pygame.font.SysFont('sans', 30)
            text = font.render(self.text1, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2) - 50))
        if self.text2 != '':
            font = pygame.font.SysFont('sans', 30)
            text = font.render(self.text2, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        if self.text3 != '':
            font = pygame.font.SysFont('sans', 30)
            text = font.render(self.text3, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), 50 + self.y + (self.height/2 - text.get_height()/2)))

    def is_hover(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def visit_animation(visited):
    for node in visited:
        if node.color == VISIT1 or node.color == VISIT3:
            visited.remove(node)
            continue
        r, g, b = node.color
        if g < 255:
            g += 1
        node.color = (r, g, b)


def visit_animation2(node):
    if node.color == VISIT1:
        return True
    else:
        r, g, b = node.color
        b += 1
        node.color = (r, g, b)
        return False
    
def path_animation(path):
    for node in path:
        if not node.is_start():
            r, g, b = node.color
            if node.dec_animation:
                g -= 1
                if g <= PATH1[1]:
                    node.dec_animation = False
            else:
                g += 1
                if g >= PATH2[1]:
                    node.dec_animation = True
        node.color = (r, g, b)

def reconstruct_path(came_from, start, current, draw, visited,  win, width, grid, is_draw = True):
    path = []
    c = 0
    while current in came_from:
        visit_animation(visited)
        current = came_from[current]
        if current.is_weight():
            c+= 5
        else:
            c+=1
        if current in visited:
            visited.remove(current)
        if current != start:
            path.insert(0, current)
        current.make_path()
#         path_animation(path)
        if is_draw:
            for rows in grid:
                for node in rows:
                    node.draw(win)
            draw_grid(win, len(grid), width)
            pygame.display.update()
    return path, c-1

def draw(win, grid, rows, width, algorithms, mazes, options, output, menu = True):
    win.fill(BG_COLOR)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    if menu:
        n = 17
        delta = 700
        ht = 900
        width = ht
        w = 1600
        font = pygame.font.SysFont('comicsans', 35)
        text = font.render("Algorithms", 1, WHITE)
        top = 0
        end = ht//40
        win.blit(text, (width+delta//6, (end-top)/2.5))
        for algorithm in algorithms:
            algorithm.draw(win, BLACK)
        
        text = font.render("Generate Maze", 1, WHITE)
        but_height = ht//15
        top += (4*but_height)
        end += (1.9*(3*but_height//2)) + but_height + ht//12
        win.blit(text, (width+delta//6, ((end-top)/2) + top))
        for maze in mazes:
            maze.draw(win, BLACK)
            
        end += (1.3*(3*but_height//2)) + ht//6
        top += (5*but_height//2)
        
        text = font.render("Options", 1, WHITE)
        win.blit(text, (width+delta//6, ((end-top)/2) + top))
        for option in options:
            option.draw(win, BLACK)
        output.draw(win, BLACK)
    pygame.display.update()