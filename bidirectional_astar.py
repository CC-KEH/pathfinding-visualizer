import pygame
from queue import PriorityQueue
import numpy as np
from constants import *
from board import *
from system import *



def bi_astar(draw, grid, start, end, output, win, width, moving_target=False):
    count = 0
    vis = 0
    open_set_start = PriorityQueue()
    open_set_start.put((0, count, start))
    came_from_start = {}
    open_set_end = PriorityQueue()
    open_set_end.put((0, count, end))
    came_from_end = {}
    g_score_start = {node: float("inf") for row in grid for node in row}
    g_score_end = {node: float("inf") for row in grid for node in row}
    g_score_start[start] = 0
    g_score_end[end] = 0
    f_score_start = {node: float("inf") for row in grid for node in row}
    f_score_end = {node: float("inf") for row in grid for node in row}
    f_score_start[start] = heuristic(start.get_pos(), end.get_pos())
    f_score_end[end] = heuristic(start.get_pos(), end.get_pos())
    x1, y1 = start.get_pos()
    x2, y2 = end.get_pos()
    threshold = max((abs(x1-x2) + abs(y1-y2))//2, len(grid)//3)
    lock = False
    
    visited1 = []
    visited2 = []
    nebrs = []
    v1, v2 = [], []
    
    open_set_hash_start = {start}
    open_set_hash_end = {end}
    while len(open_set_hash_start) and len(open_set_hash_end):
        if moving_target:
            li = [i for i in end.neighbors if i.is_neutral()]
            if len(li):
                end.reset()
                end = li[np.random.randint(len(li))]
                end.make_end()
                for rows in grid:
                    for node in rows:
                        node.draw(win)
                        draw_grid(win, len(grid), width)
                        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set_start.get()[2]
        open_set_hash_start.remove(current)
        
        c = 1
        for neighbor in current.neighbors:
            if not neighbor.is_barrier():
                if (neighbor.is_neutral() or neighbor.color == BROWN or neighbor.is_open()):
                    if neighbor.is_weight():
                        c = 5
                    temp_g_score = g_score_start[current] + c
                    temp_f_score = (temp_g_score**(heuristic(neighbor.get_pos(), end.get_pos())*temp_g_score))
                    if temp_f_score < f_score_start[neighbor]:
                        came_from_start[neighbor] = current
                        g_score_start[neighbor] = temp_g_score
                        f_score_start[neighbor] = temp_f_score
                        if neighbor not in open_set_hash_start:
                            count+=1
                            open_set_start.put((f_score_start[neighbor], count, neighbor))
                            open_set_hash_start.add(neighbor)
                            nebrs.append(neighbor)
                            neighbor.make_open()
                elif neighbor != start and neighbor not in v1:
                    neighbor.color = (254, 102, 1)
                    draw_grid(win, len(grid), width)
                    pygame.display.update()
                    came_from_start[neighbor] = current
                    path1, inc1 = reconstruct_path(came_from_start, start, neighbor, draw, visited1, win, width, grid)
                    start.make_start()
                    path2, inc2 = reconstruct_path(came_from_end, end, neighbor, draw, visited1, win, width, grid)
                    end.make_end()
                    output.set_text1(f"Path Length: {inc1+inc2+1}")
                    output.set_text2(f"#Visited nodes: {vis}")
                    if vis != 0:
                        output.set_text3(f"Efficiency: {np.round((inc1+inc2+1+1)/vis, decimals=3)}")
                    return visited1+visited2, path1+path2
        if current != start:
            if current in visited1:
                visited1.remove(current)
            current.make_visit()
            v1.append(current)
            visited1.append(current)
            vis+=c

        visit_animation(visited1)
#         nebr_animation(nebrs)
        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()
        if not lock:
            current = open_set_end.get()[2]
            open_set_hash_end.remove(current)
            if g_score_end[current] > threshold:
                lock = True
            c = 1
            for neighbor in current.neighbors:
                if not neighbor.is_barrier():
                    if (neighbor.is_neutral() or neighbor.color == BROWN or neighbor.is_open()):
                        if neighbor.is_weight():
                            c = 5
                        temp_g_score = g_score_end[current] + c
                        temp_f_score = temp_g_score
                        if temp_f_score < f_score_end[neighbor]:
                            came_from_end[neighbor] = current
                            g_score_end[neighbor] = temp_g_score
                            f_score_end[neighbor] = temp_f_score
                            if neighbor not in open_set_hash_end:
                                count+=1
                                open_set_end.put((f_score_end[neighbor], count, neighbor))
                                open_set_hash_end.add(neighbor)
                                nebrs.append(neighbor)
                                neighbor.make_open()
                    elif neighbor != end and neighbor not in v2:
                        neighbor.color = (254, 102, 1)
                        draw_grid(win, len(grid), width)
                        pygame.display.update()
                        came_from_end[neighbor] = current
                        path1, inc1 = reconstruct_path(came_from_end, end, neighbor, draw, visited2, win, width, grid)
                        end.make_end()
                        path2, inc2 = reconstruct_path(came_from_start, start, neighbor, draw, visited2, win, width, grid)
                        start.make_start()
                        output.set_text1(f"Path Length: {inc1+inc2+1}")
                        output.set_text2(f"#Visited nodes: {vis}")
                        if vis != 0:
                            output.set_text3(f"Efficiency: {np.round((inc1+inc2+1)/vis, decimals=3)}")
                        return visited2+visited1, path1+path2

            if current != end:
                if current in visited2:
                    visited2.remove(current)
                current.make_visit()
                v2.append(current)
                visited2.append(current)
                vis+=c

            visit_animation(visited2)
    #         nebr_animation(nebrs)
            for rows in grid:
                for node in rows:
                    node.draw(win)
            draw_grid(win, len(grid), width)
            pygame.display.update()
            
    return visited2+visited1, False
#     count = 0
#     vis = 0
#     open_set_start = PriorityQueue()
#     open_set_start.put((0, count, start))
#     came_from_start = {}
#     open_set_end = PriorityQueue()
#     open_set_end.put((0, count, end))
#     came_from_end = {}
#     g_score_start = {node: float("inf") for row in grid for node in row}
#     g_score_end = {node: float("inf") for row in grid for node in row}
#     g_score_start[start] = 0
#     g_score_end[end] = 0
#     f_score_start = {node: float("inf") for row in grid for node in row}
#     f_score_end = {node: float("inf") for row in grid for node in row}
#     f_score_start[start] = heuristic(start.get_pos(), end.get_pos())
#     f_score_end[end] = heuristic(start.get_pos(), end.get_pos())
#     x1, y1 = start.get_pos()
#     x2, y2 = end.get_pos()
#     threshold = max((abs(x1-x2) + abs(y1-y2))//2, len(grid)//3)
#     lock = False
    
#     visited1 = []
#     visited2 = []
#     nebrs = []
#     v1, v2 = [], []
    
#     open_set_hash_start = {start}
#     open_set_hash_end = {end}
#     while len(open_set_hash_start) and len(open_set_hash_end):
#         if moving_target:
#             li = [i for i in end.neighbors if i.is_neutral()]
#             if len(li):
#                 end.reset()
#                 end = li[np.random.randint(len(li))]
#                 end.make_end()
#                 for rows in grid:
#                     for node in rows:
#                         node.draw(win)
#                         draw_grid(win, len(grid), width)
#                         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
        
#         current = open_set_start.get()[2]
#         open_set_hash_start.remove(current)
        
#         c = 1
#         for neighbor in current.neighbors:
#             if not neighbor.is_barrier():
#                 if (neighbor.is_neutral() or neighbor.color == BROWN or neighbor.is_open()):
#                     if neighbor.is_weight():
#                         c = 5
#                     temp_g_score = g_score_start[current] + c
#                     temp_f_score = (temp_g_score**(heuristic(neighbor.get_pos(), end.get_pos())*temp_g_score))
#                     if temp_f_score < f_score_start[neighbor]:
#                         came_from_start[neighbor] = current
#                         g_score_start[neighbor] = temp_g_score
#                         f_score_start[neighbor] = temp_f_score
#                         if neighbor not in open_set_hash_start:
#                             count+=1
#                             open_set_start.put((f_score_start[neighbor], count, neighbor))
#                             open_set_hash_start.add(neighbor)
#                             nebrs.append(neighbor)
#                             neighbor.make_open()
#                 elif neighbor != start and neighbor not in v1:
#                     neighbor.color = (254, 102, 1)
#                     draw_grid(win, len(grid), width)
#                     pygame.display.update()
#                     came_from_start[neighbor] = current
#                     path1, inc1 = reconstruct_path(came_from_start, start, neighbor, draw, visited1, win, width, grid)
#                     start.make_start()
#                     path2, inc2 = reconstruct_path(came_from_end, end, neighbor, draw, visited1, win, width, grid)
#                     end.make_end()
#                     output.set_text1(f"Path Length: {inc1+inc2+1}")
#                     output.set_text2(f"#Visited nodes: {vis}")
#                     if vis != 0:
#                         output.set_text3(f"Efficiency: {np.round((inc1+inc2+1+1)/vis, decimals=3)}")
#                     return visited1+visited2, path1+path2
#         if current != start:
#             if current in visited1:
#                 visited1.remove(current)
#             current.make_visit()
#             v1.append(current)
#             visited1.append(current)
#             vis+=c

#         visit_animation(visited1)
# #         nebr_animation(nebrs)
#         for rows in grid:
#             for node in rows:
#                 node.draw(win)
#         draw_grid(win, len(grid), width)
#         pygame.display.update()
#         if not lock:
#             current = open_set_end.get()[2]
#             open_set_hash_end.remove(current)
#             if g_score_end[current] > threshold:
#                 lock = True
#             c = 1
#             for neighbor in current.neighbors:
#                 if not neighbor.is_barrier():
#                     if (neighbor.is_neutral() or neighbor.color == BROWN or neighbor.is_open()):
#                         if neighbor.is_weight():
#                             c = 5
#                         temp_g_score = g_score_end[current] + c
#                         temp_f_score = temp_g_score
#                         if temp_f_score < f_score_end[neighbor]:
#                             came_from_end[neighbor] = current
#                             g_score_end[neighbor] = temp_g_score
#                             f_score_end[neighbor] = temp_f_score
#                             if neighbor not in open_set_hash_end:
#                                 count+=1
#                                 open_set_end.put((f_score_end[neighbor], count, neighbor))
#                                 open_set_hash_end.add(neighbor)
#                                 nebrs.append(neighbor)
#                                 neighbor.make_open()
#                     elif neighbor != end and neighbor not in v2:
#                         neighbor.color = (254, 102, 1)
#                         draw_grid(win, len(grid), width)
#                         pygame.display.update()
#                         came_from_end[neighbor] = current
#                         path1, inc1 = reconstruct_path(came_from_end, end, neighbor, draw, visited2, win, width, grid)
#                         end.make_end()
#                         path2, inc2 = reconstruct_path(came_from_start, start, neighbor, draw, visited2, win, width, grid)
#                         start.make_start()
#                         output.set_text1(f"Path Length: {inc1+inc2+1}")
#                         output.set_text2(f"#Visited nodes: {vis}")
#                         if vis != 0:
#                             output.set_text3(f"Efficiency: {np.round((inc1+inc2+1)/vis, decimals=3)}")
#                         return visited2+visited1, path1+path2

#             if current != end:
#                 if current in visited2:
#                     visited2.remove(current)
#                 current.make_visit()
#                 v2.append(current)
#                 visited2.append(current)
#                 vis+=c

#             visit_animation(visited2)
#     #         nebr_animation(nebrs)
#             for rows in grid:
#                 for node in rows:
#                     node.draw(win)
#             draw_grid(win, len(grid), width)
#             pygame.display.update()
            
#     return visited2+visited1, False