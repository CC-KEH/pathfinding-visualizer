from board import *
import pygame
from constants import *
from system import *
import numpy as np


def floydWarshall(draw,grid,start,end,output, win, width):
    visited = [start]
    came_from = {}
    vis = 0
    for i in range(len(grid)-1):
        for j in range(len(grid)):
            for k in range(len(grid)):
                if grid[j][k].is_barrier():
                    continue
                if grid[j][k].is_weight():
                    c = 5
                else:
                    c = 1
                for neighbor in grid[j][k].neighbors:
                    if neighbor.is_barrier():
                        continue
                    if neighbor.is_weight():
                        c = 5
                    if grid[j][k].distance + c < neighbor.distance:
                        neighbor.distance = grid[j][k].distance + c
                        came_from[neighbor] = grid[j][k]
                        if neighbor == end:
                            path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
                            start.make_start()
                            output.set_text1(f"Path Length: {inc}")
                            output.set_text2(f"#Visited nodes: {vis}")
                            if vis != 0:
                                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
                            return visited, path
                        visited.append(neighbor)
                        neighbor.make_open()
                        vis+=c
                        neighbor.make_visit()
                        visit_animation(visited)
                        for rows in grid:
                            for node in rows:
                                node.draw(win)
                        draw_grid(win, len(grid), width)
                        pygame.display.update()
    return visited, False