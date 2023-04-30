from board import *
from constants import *
import pygame
from queue import PriorityQueue
from system import *

def IDA_star(draw, win, width, output,  grid, start, end, threshold=100, moving_target= False, visited_old = []):
    if threshold < len(grid)**2:
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
        while not open_set.empty():
            if moving_target:
                li = [i for i in end.neighbors if i.is_neutral()]
                if len(li):
                    end.reset()
                    end = li[np.random.randint(len(li))]
                    end.make_end()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]

            if current == end:
                path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
                start.make_start()
                output.set_text1(f"Path Length: {inc}")
                output.set_text2(f"#Visited nodes: {vis}")
                if vis != 0:
                    output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
                return visited, path
            
            c = 1
            if f_score[current] <= threshold:
                for neighbor in current.neighbors:
                    if not neighbor.is_barrier():
                        if neighbor.is_weight():
                            c = 5
                        temp_g_score = g_score[current] + c
                        temp_f_score = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                        if temp_f_score < f_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = temp_g_score
                            f_score[neighbor] = temp_f_score
                            count+=1
                            open_set.put((f_score[neighbor], count, neighbor))
                            if neighbor != end:
                                nebrs.append(neighbor)
                                neighbor.make_open()

            if current != start:
                visited.append(current)
                vis+=c
                current.make_visit()

            visit_animation(visited)
            for rows in grid:
                for node in rows:
                    node.draw(win)
            draw_grid(win, len(grid), width)
            pygame.display.update()
            
        if visited == visited_old:
            return visited, False
        return IDA_star(draw, win, width, output ,grid, start, end, threshold+10, moving_target, visited)
    return [], False

# def reconstruct_path(came_from,current,draw):
#     while current in came_from:
#         current = came_from[current]
#         current.make_path()
#         draw()

# def IDA_star(draw, win, width, output,  grid, start, end, threshold=100, moving_target= False, visited_old = []):
#     if threshold < len(grid)**2:
#         count = 0
#         vis = 0
#         open_set = PriorityQueue()
#         open_set.put((0, count, start))
#         came_from = {}
#         g_score = {node: float("inf") for row in grid for node in row}
#         g_score[start] = 0
#         f_score = {node: float("inf") for row in grid for node in row}
#         f_score[start] = heuristic(start.get_pos(), end.get_pos())

#         visited = []
#         nebrs = []
#         while not open_set.empty():
#             if moving_target:
#                 li = [i for i in end.neighbors if i.is_neutral()]
#                 if len(li):
#                     end.reset()
#                     end = li[np.random.randint(len(li))]
#                     end.make_end()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()

#             current = open_set.get()[2]

#             if current == end:
#                 path, inc = reconstruct_path(came_from, start, end, draw, visited, win, width, grid)
#                 start.make_start()
#                 output.set_text1(f"Path Length: {inc}")
#                 output.set_text2(f"#Visited nodes: {vis}")
#                 if vis != 0:
#                     output.set_text3(f"Efficiency: {np.round(inc/vis, decimals=3)}")
#                 return visited, path
            
#             c = 1
#             if f_score[current] <= threshold:
#                 for neighbor in current.neighbors:
#                     if not neighbor.is_barrier():
#                         if neighbor.is_weight():
#                             c = 5
#                         temp_g_score = g_score[current] + c
#                         temp_f_score = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
#                         if temp_f_score < f_score[neighbor]:
#                             came_from[neighbor] = current
#                             g_score[neighbor] = temp_g_score
#                             f_score[neighbor] = temp_f_score
#                             count+=1
#                             open_set.put((f_score[neighbor], count, neighbor))
#                             if neighbor != end:
#                                 nebrs.append(neighbor)
#                                 neighbor.make_open()

#             if current != start:
#                 visited.append(current)
#                 vis+=c
#                 current.make_visit()


#             for rows in grid:
#                 for node in rows:
#                     node.draw(win)
#             draw()
#             pygame.display.update()
            
#         if visited == visited_old:
#             return visited, False
#         return IDA_star(draw, win, width, output ,grid, start, end, threshold+10, moving_target, visited)
#     return [], False

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
#                     idastar(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
#                 if event.key == pygame.K_c:
#                     start = None
#                     end = None
#                     grid = make_grid(ROWS,width)

#     pygame.quit()

# if __name__ == "__main__":
#     main(WIN,WIDTH)