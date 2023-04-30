import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def dfs_animation(G, node, visited):
    visited.add(node)
    colors = ['gray' if n in visited else 'white' for n in G.nodes()]
    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.pause(0.1)  # add a short pause to allow the graph to update

    
def dfs(G, node, visited):
    visited.add(node)
    dfs_animation(G, node, visited)
    for neighbor in G.neighbors(node):
        if neighbor not in visited:
            dfs(G, neighbor, visited)

# Initialize graph
G = nx.Graph()
G.add_edges_from([(1,2),(1,3),(2,4),(2,5),(3,6),(3,7),(4,8),(5,9),(7,10)])

# Set layout
pos = nx.spring_layout(G)

# Set up animation
fig, ax = plt.subplots()
def animate(i):
    visited = set()
    dfs(G, 1, visited)
anim = FuncAnimation(fig, animate, frames=range(len(G)), interval=500, repeat=False)

plt.show()
