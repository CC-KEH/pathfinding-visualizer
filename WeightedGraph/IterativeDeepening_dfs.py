import pygame
from constants import *
from board import *

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def iterative_deepening_dfs(draw,grid,start,end,depth=20):
    visited = {start}
    came_from = {}
    stack = [start]

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        
        if current == end:
            reconstruct_path(came_from,end,draw)
            end = end.mark_end()
            return True
            
        if depth>0:
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    visited.add(neighbor)
                    neighbor.mark_open()
            draw()
            depth-=1
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
                    iterative_deepening_dfs(lambda: draw(win,grid,ROWS,width),grid,start,end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN,WIDTH)