from queue import PriorityQueue
from board import *
import pygame
from constants import *
from system import *
import numpy as np

def A_star(draw, grid, start, end, output, win, width):
    count = 0
    vis = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    visited = []
    nebrs = []
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
            start.make_start()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
            return visited, path
        c = 1      
        for neighbor in current.neighbors:
            if not neighbor.is_barrier():
                if neighbor.is_weight():
                    c = 5

                temp_g_score = g_score[current] + c
                temp_f_score = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_f_score
                    if neighbor not in open_set_hash:
                        count+=1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                    if neighbor != end:
                        nebrs.append(neighbor)
                        neighbor.make_open()
        
        if current != start:
            vis+=c
            visited.append(current)
            current.make_visit()
        visit_animation(visited)
        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()
            
    return False