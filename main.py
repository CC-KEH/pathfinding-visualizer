import pygame
import pygame_menu
from pygame_menu import themes
from astar import astar
pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_algorithm(value, algo):
    print(value)
    print(algo)
 
def start_the_algo():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
 
def algo_menu():
    mainmenu._open(level)

font = pygame.font.Font(None, 40)



mainmenu = pygame_menu.Menu('Pathfinding Visualizer', 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='')
mainmenu.add.button('Start', algo_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)


level = pygame_menu.Menu('Select the Algorithm', 600, 400, theme=themes.THEME_BLUE)
level.add.button('A star', start_the_algo)
level.add.button('BFS', start_the_algo)
level.add.button('Bidirectional-BFS', start_the_algo)
level.add.button('DFS', start_the_algo)
level.add.button('IDFS', start_the_algo)
level.add.button('IDAstar', start_the_algo)

 
loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (15, 15))
 
update_loading = pygame.USEREVENT + 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0) 

        if event.type == pygame.QUIT:
            exit()
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
 
    pygame.display.update()