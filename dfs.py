from board import *
import pygame
from constants import *
from system import *
import numpy as np


def dfs(draw,grid,start,end,output, win, width):
    stack = [start]
    visited = [start]
    came_from = {}
    vis = 0

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
         
        current = stack.pop()
        if current == end:
            path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
            start.make_start()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
            return visited, path
        c = 1      
        visited.append(current)
        for neighbor in current.neighbors:
            if not neighbor.is_barrier():
                if neighbor.is_weight():
                    c = 5
                if neighbor not in visited:
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    neighbor.make_open()
                    if(neighbor == end):
                        path,inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
                        start = start.make_start()
                        output.set_text1(f"Path Length: {inc}")
                        output.set_text2(f"#Visited nodes: {vis}")
                        if vis != 0:
                            output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
                        return visited, path                                           
        
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




#     stack = [start]
#     visited = {start}
#     came_from = {}
#     while stack:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
         
#         current = stack.pop()
#         if current == end:
#             reconstruct_path(came_from,end,draw)
#             end = end.mark_end()
#             return True
        
#         for neighbor in current.neighbors:
#             if neighbor not in visited:
#                 came_from[neighbor] = current
#                 if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
#                     reconstruct_path(came_from,end,draw)
#                     end = end.mark_end()
#                     return True
#                 stack.append(neighbor)
#                 visited.add(neighbor)
#                 neighbor.mark_open()
#         draw()

#         if current!=start:
#             current.mark_visited()



# def main(win,width):
#     ROWS = 50
#     grid = make_grid(ROWS,width)
#     start = None
#     end = None 
#     run = True
#     while run:
#         draw(win,grid,ROWS,width)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False

#             if pygame.mouse.get_pressed()[0]:   #*Left Button
#                 pos = pygame.mouse.get_pos()
#                 row,col = get_clicked_pos(pos,ROWS,width)
#                 node = grid[row][col]
#                 if not start and node!=end: #* Cannot make your end node as start, if we click on the same node again
#                     start = node
#                     start.mark_start()
                
#                 elif not end and node!=start:   #* Cannot make your start node as end, if we click on the same node again
#                     end = node
#                     end.mark_end()
                
#                 elif node!=end and node!=start:
#                     node.mark_obstacle()

#             elif pygame.mouse.get_pressed()[2]:  #*Right Button
#                 pos = pygame.mouse.get_pos()
#                 row,col = get_clicked_pos(pos,ROWS,width)
#                 node = grid[row][col]
#                 node.reset()
#                 if node == start:
#                     start = None
#                 elif node == end:
#                     end = None

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and start and end:   #* Start the algo if start and end are marked 
#                     for row in grid:
#                         for node in row:
#                             node.update_neighbors(grid)
#                     dfs(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
#                 if event.key == pygame.K_c:
#                     start = None
#                     end = None
#                     grid = make_grid(ROWS,width)

#     pygame.quit()
    
# if __name__ == "__main__":
#     main(WIN,WIDTH)