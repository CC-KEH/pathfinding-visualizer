# Description: Bidirectional BFS Algorithm
from board import *
import pygame
from constants import *
from system import *
import numpy as np


def bi_bfs(draw,grid,start,end,output, win, width):
    queue1 = [start]
    queue2 = [end]
    visited1 = [start]
    visited2 = [end]
    came_from1 = {}
    came_from2 = {}
    vis = 0
    while queue1 and queue2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current1 = queue1.pop(0)
        current2 = queue2.pop(0)

        if (current1 in visited2):
            path1,inc1 = reconstruct_path(came_from1,start,current1,draw,visited1, win, width, grid)
            start.make_start()
            path2,inc2 = reconstruct_path(came_from2,end,current1,draw,visited2, win, width, grid)
            end.make_end()
            current1.make_path()
            output.set_text1(f"Path Length: {inc1+inc2+1}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc1+inc2+1+1/vis, decimals=3)}")
            return visited2+visited1, path1+path2
                      
        elif (current2 in visited1):
            path1,inc1 = reconstruct_path(came_from1,start,current2,draw,visited1, win, width, grid)
            start.make_start()
            path2,inc2 = reconstruct_path(came_from2,end,current2,draw,visited2, win, width, grid)
            end.make_end()
            current2.make_path()
            output.set_text1(f"Path Length: {inc1+inc2+1}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc1+inc2+1+1/vis, decimals=3)}")
            return visited1+visited2, path1 + path2
        

        if current1 == end:
            path,inc = reconstruct_path(came_from1,start,end,draw,visited1, win, width, grid)
            start.make_start()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
            return visited1, path
        
        elif current2 == start:
            path,inc = reconstruct_path(came_from1,start,end,draw,visited2, win, width, grid)
            start.make_start()
            output.set_text1(f"Path Length: {inc}")
            output.set_text2(f"#Visited nodes: {vis}")
            if vis != 0:
                output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
            return visited2, path

        c = 1

        for neighbor in current1.neighbors: #*Check all the neighbors of the current node
            if not neighbor.is_barrier():
                if neighbor not in visited1:
                    came_from1[neighbor] = current1
                    if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
                        path1, inc1 = reconstruct_path(came_from1, start, end, draw, visited1, win, width, grid)
                        start.make_start()
                        output.set_text1(f"Path Length: {inc1}")
                        output.set_text2(f"#Visited nodes: {vis}")
                        if vis != 0:
                            output.set_text3(f"Efficiency: {np.round(inc1/vis, decimals=3)}")
                        return visited1, path1   
                    queue1.append(neighbor)
                    visited1.append(neighbor)
                    neighbor.make_open()
        
        for neighbor in current2.neighbors: 
            if not neighbor.is_barrier():
                if neighbor not in visited2:
                    came_from2[neighbor] = current2
                    if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
                        path2, inc2 = reconstruct_path(came_from1, start, end, draw, visited2, win, width, grid)
                        start.make_start()
                        output.set_text1(f"Path Length: {inc2}")
                        output.set_text2(f"#Visited nodes: {vis}")
                        if vis != 0:
                            output.set_text3(f"Efficiency: {np.round(inc2/vis, decimals=3)}")
                        return visited2, path2  
                    queue2.append(neighbor)
                    visited2.append(neighbor)
                    neighbor.make_open() 
        
        if current1 != start:
            vis+=c
            current1.make_visit()
        visit_animation(visited1)
        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()
        
        if current2 != end:
            vis+=c
            current2.make_visit()
        visit_animation(visited2)
        for rows in grid:
            for node in rows:
                node.draw(win)
        draw_grid(win, len(grid), width)
        pygame.display.update()

    return visited1+visited2, False

        


# def bidirectonal_bfs(draw,grid,start,end):
#     queue1 = [start]
#     queue2 = [end]
#     visited1 = {start}
#     visited2 = {end}
#     came_from1 = {}
#     came_from2 = {}
#     while queue1 and queue2:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
        
#         current1 = queue1.pop(0)
#         current2 = queue2.pop(0)

#         if (current1 in visited2):
#             reconstruct_path(came_from1,current1,draw)
#             reconstruct_path(came_from2,current1,draw)
#             return True
        
#         elif (current2 in visited1):
#             reconstruct_path(came_from1,current2,draw)
#             reconstruct_path(came_from2,current2,draw)
#             return True
        


#         if current1 == end or current2 == start:
#             reconstruct_path(came_from1,current1,draw)
#             reconstruct_path(came_from2,current2,draw)
#             return True
        
#         for neighbor in current1.neighbors: #*Check all the neighbors of the current node
#             if neighbor not in visited1:
#                 came_from1[neighbor] = current1
#                 if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
#                     reconstruct_path(came_from1,end,draw)
#                     end = end.mark_end()
#                     return True
#                 queue1.append(neighbor)
#                 visited1.add(neighbor)
#                 neighbor.mark_open()   
#         draw()

#         for neighbor in current2.neighbors: #*Check all the neighbors of the current node
#             if neighbor not in visited2:
#                 came_from2[neighbor] = current2
#                 if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
#                     reconstruct_path(came_from2,end,draw)
#                     end = end.mark_end()
#                     return True
#                 queue2.append(neighbor)
#                 visited2.add(neighbor)
#                 neighbor.mark_open()   
#         draw()

#         if current1!=start: #*If the current node is not the start node, mark it as visited
#             current1.mark_visited()
        
#         if current2!=end: #*If the current node is not the start node, mark it as visited
#             current2.mark_visited()

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
#                     bidirectonal_bfs(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
#                 if event.key == pygame.K_c:
#                     start = None
#                     end = None
#                     grid = make_grid(ROWS,width)

#     pygame.quit()

# if __name__ == "__main__":
#     main(WIN,WIDTH)