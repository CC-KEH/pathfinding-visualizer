import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    # Set node colors based on their state
    node_colors = ['white' if v['visited'] == 0 else 'green' for v in G.nodes.values()]
    node_colors[i] = 'red'  # Highlight current node
    
    # Set edge colors based on whether they lead to a visited node or not
    edge_colors = ['gray' if G.nodes[u]['visited'] == 0 or G.nodes[v]['visited'] == 0 else 'black' for u, v in G.edges()]
    
    # Draw the graph with updated colors
    nx.draw(G, pos, node_color=node_colors, edge_color=edge_colors, with_labels=True)
    
    # Perform BFS step
    if len(queue) > 0:
        curr_node = queue.pop(0)
        G.nodes[curr_node]['visited'] = 1
        for neighbor in G.neighbors(curr_node):
            if G.nodes[neighbor]['visited'] == 0:
                queue.append(neighbor)
                
    return plt

# Initialize graph
G = nx.Graph()
G.add_edges_from([(1,2),(1,3),(2,4),(2,5),(3,6),(3,7),(4,8),(5,9),(7,10)])
for node in G.nodes():
    G.nodes[node]['visited'] = 0
    
# Set layout
pos = nx.spring_layout(G)

# Set up queue and start animation
queue = [1]
anim = FuncAnimation(plt.gcf(), animate, frames=range(len(G)), interval=250, repeat=False)
plt.show()
