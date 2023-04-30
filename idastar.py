from board import *
from constants import *
import pygame
import math
from queue import PriorityQueue

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    open_set = PriorityQueue()
    open_set.put((0,start))
    came_from = {}
    g_score = {node:float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node:float("inf") for row in grid for node in row}\
    

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[1]
        if current == end:
            reconstruct_path(came_from,end,draw)
            end.mark_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if(temp_g_score < g_score[neighbor]):
                came_from[neighbor] = current
                if(neighbor == end):
                    reconstruct_path(came_from,end,draw)
                    end.mark_end()
                    return True
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(),end.get_pos())
                open_set.put((f_score[neighbor],neighbor))
                neighbor.mark_open()
        
        draw()
        
        if current!=start: #* If the current node is not the start node, then we mark it as closed, Color(RED)
            current.mark_visited()


    return False


def idastar(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    start = None
    end = None 
    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:   #*Left Button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start and node!=end: #* Cannot make your end node as start, if we click on the same node again
                    start = node
                    start.mark_start()
                
                elif not end and node!=start:   #* Cannot make your start node as end, if we click on the same node again
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
                if event.key == pygame.K_SPACE and start and end:   #* Start the algo if start and end are marked 
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pygame.quit()

idastar(WIN,WIDTH)