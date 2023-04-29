# Description: Bidirectional BFS Algorithm
from board import *
import pygame
from constants import *

def reconstruct_path(came_from,current,draw):
    current.make_path()
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def bidirectional_bfs(draw,grid,start,end):
    queue1 = [start]
    queue2 = [end]
    visited1 = {start}
    visited2 = {end}
    came_from1 = {}
    came_from2 = {}
    while queue1 and queue2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current1 = queue1.pop(0)
        current2 = queue2.pop(0)

        if (current1 in visited2):
            reconstruct_path(came_from1,current1,draw)
            reconstruct_path(came_from2,current1,draw)
            return True
        
        elif (current2 in visited1):
            reconstruct_path(came_from1,current2,draw)
            reconstruct_path(came_from2,current2,draw)
            return True
        


        if current1 == end or current2 == start:
            reconstruct_path(came_from1,current1,draw)
            reconstruct_path(came_from2,current2,draw)
            return True
        
        for neighbor in current1.neighbors: #*Check all the neighbors of the current node
            if neighbor not in visited1:
                came_from1[neighbor] = current1
                if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
                    reconstruct_path(came_from1,end,draw)
                    end = end.mark_end()
                    return True
                queue1.append(neighbor)
                visited1.add(neighbor)
                neighbor.mark_open()   
        draw()

        for neighbor in current2.neighbors: #*Check all the neighbors of the current node
            if neighbor not in visited2:
                came_from2[neighbor] = current2
                if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
                    reconstruct_path(came_from2,end,draw)
                    end = end.mark_end()
                    return True
                queue2.append(neighbor)
                visited2.add(neighbor)
                neighbor.mark_open()   
        draw()

        if current1!=start: #*If the current node is not the start node, mark it as visited
            current1.mark_visited()
        
        if current2!=end: #*If the current node is not the start node, mark it as visited
            current2.mark_visited()

def main(win,width):
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
                    bidirectional_bfs(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pygame.quit()

main(WIN,WIDTH)