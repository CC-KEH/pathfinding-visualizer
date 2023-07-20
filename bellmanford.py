from board import *
import pygame
from constants import *
from system import *
import numpy as np


def calculate_distance(node1, node2):
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)
      
    
def bellmanFord(draw, grid, start, end, output, win, width):
    count = 0
    vis = 0
    nodes = [node for row in grid for node in row]
    distance = {node: float("inf") for node in nodes}
    distance[start] = 0
    visited = []

    for _ in range(len(nodes) - 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for node in nodes:
            for neighbor in node.neighbors:
                # Modify the cost based on weight status of the neighbor node
                if neighbor.is_weight():
                    c = 5
                else:
                    c = 1

                if distance[node] + c < distance[neighbor]:
                    distance[neighbor] = distance[node] + c
                    neighbor.make_open()
        
        # Visualization steps similar to A_star function
        visited.append(node)
        node.make_visit()

        visit_animation(visited)
        for row in grid:
            for node in row:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    # Backtrack to find the shortest path and visualize it
    path = []
    current = end
    while current != start:
        path.append(current)
        current = current.previous
    path.append(start)
    path.reverse()
    
    # Highlight the shortest path
    for node in path:
        node.make_path()
        for row in grid:
            for node in row:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()
    
    # Set the text for the output
    output.set_text1(f"Path Length: {distance[end]}")
    output.set_text2(f"#Visited nodes: {len(visited)}")
    if len(visited) != 0:
        output.set_text3(f"Efficiency: {np.round(len(path)/len(visited), decimals=3)}")

    return visited, path
