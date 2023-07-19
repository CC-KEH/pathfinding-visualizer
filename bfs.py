from board import *
import pygame
from constants import *
from system import *
import numpy as np


def bfs(draw,grid,start,end,output, win, width):   #*Breadth First Search
    queue = [start]
    visited = [start]
    came_from = {}
    vis = 0
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = queue.pop(0)
        if current == end:
            path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
            start.make_start()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
            return visited, path
        c = 1      
        
        for neighbor in current.neighbors: #*Check all the neighbors of the current node
            if not neighbor.is_barrier():
                if neighbor.is_weight():
                    c = 5
            if neighbor not in visited:
                came_from[neighbor] = current
                if(neighbor == end): 
                    path,inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
                    start = start.make_start()
                    output.set_text1(f"Path Length: {inc}")
                    output.set_text2(f"#Visited nodes: {vis}")
                    if vis != 0:
                        output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
                    return visited, path
                queue.append(neighbor)
                visited.append(neighbor)
                neighbor.make_open()   

        if current != start:
            vis+=c
            current.make_visit()

        visit_animation(visited)

        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()
            
    return visited, False
