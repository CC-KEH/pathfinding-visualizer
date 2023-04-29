from queue import PriorityQueue
from board import *
import pygame
from constants import *
FPS = 60
# fpsClock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def astar(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    
    #* Inserting 3 vars in queue ie -> F(n) ie FScore, count to keep the check of which node was inserted first, start node
    open_set.put((0,count,start))
    came_from = {}
    
    #* Assigning G-Score for each node to infinity except start node which is 0
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    #* Assigning F-Score for each node to infinity except start node which is calculated using heuristic function
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(),end.get_pos())

    open_set_hash = {start} #* To keep track of all the items in the priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] #* Getting the node from the queue
        open_set_hash.remove(current) #* Removing the node from the queue
        
        if current == end: #* If we have reached the end node
            reconstruct_path(came_from,end,draw)
            end = end.mark_end()
            return True
        
        for neighbor in current.neighbors: #* Checking all the neighbors of the current node
            temp_g_score = g_score[current] + 1 #* Calculating the g_score of the neighbor node

            if(temp_g_score < g_score[neighbor]):
                came_from[neighbor] = current #* If the g_score of the neighbor node is less than the g_score of the current node, then we update the came_from dict
                
                
                if(neighbor == end): #* If the neighbor node is the end node, then we reconstruct the path and return True
                    reconstruct_path(came_from,end,draw)
                    end = end.mark_end()
                    return True

                g_score[neighbor] = temp_g_score #* Updating the g_score of the neighbor node
                
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(),end.get_pos()) #* Updating the f_score of the neighbor node
                
                if neighbor not in open_set_hash: #* If the neighbor node is not in the queue, then we add it to the queue
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.mark_open()

        draw()
        # pygame.display.update()
        # fpsClock.tick(FPS)
        if current!=start: #* If the current node is not the start node, then we mark it as closed, Color(RED)
            current.mark_visited()

    return False


        
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
                    astar(lambda:draw(win,grid,ROWS,width),grid,start,end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pygame.quit()

main(WIN,WIDTH)