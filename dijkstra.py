from board import *
import pygame
from constants import *
from system import *
import numpy as np


def dijkstra(draw, grid, start, end, output, win, width):
    visited_list = []
    came_from = {}
    distances = {node: float('inf') for row in grid for node in row}
    distances[start] = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))

    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = priority_queue.get()[1]

        if current_node == end:
            path, inc = reconstruct_path(came_from, start, end, draw, visited_list, win, width, grid)
            start.make_start()
            end.make_end()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {len(visited_list)}")
            if len(visited_list) != 0:
                output.set_text3(f"Efficiency: {np.round(inc / len(visited_list), decimals=3)}")
            visit_animation(visited_list)  # Send visited_list to visit_animation
            return visited_list, path

        if current_node in visited_list:
            continue

        visited_list.append(current_node)

        if current_node != start:
            current_node.make_visit()
        visit_animation(visited_list)
    
        for neighbor in current_node.neighbors:
            if neighbor.is_barrier():
                continue
            if neighbor.is_weight():
                c = 5
            else:
                c = 1

            distance_to_neighbor = distances[current_node] + c

            if distance_to_neighbor < distances[neighbor]:
                came_from[neighbor] = current_node
                distances[neighbor] = distance_to_neighbor
                priority_queue.put((distance_to_neighbor, neighbor))
                neighbor.make_open()

        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()

    return visited_list, False

