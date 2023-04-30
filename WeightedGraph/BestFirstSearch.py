import networkx as nx
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def best_first_search_animation(G, start, goal):
    visited = set()
    frontier = [(0, start, None)]
    came_from = {}

    while frontier:
        _, current, _ = heapq.heappop(frontier)

        if current == goal:
            # Reconstruct the path from start to goal
            path = [current]
            while current != start:
                current = came_from[current]
                path.append(current)
            path.reverse()
            colors = ['yellow' if n in path else 'gray' if n in visited else 'white' for n in G.nodes()]
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            nx.draw(G, pos, node_color=colors, with_labels=True)
            plt.pause(0.1)
            return path

        visited.add(current)
        colors = ['yellow' if n == current else 'gray' if n in visited else 'white' for n in G.nodes()]
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, node_color=colors, with_labels=True)
        plt.pause(0.1)

        for neighbor in G.neighbors(current):
            if neighbor in visited:
                continue

            if neighbor not in came_from:
                # Add new neighbors to the frontier and sort by distance to the goal
                priority = nx.astar_path_length(G, neighbor, goal, weight='weight')
                heapq.heappush(frontier, (priority, neighbor, current))
                came_from[neighbor] = current

    return None

# Initialize graph
G = nx.Graph()
G.add_weighted_edges_from([((0,0), (0,1), 1), ((0,0), (1,0), 2),
                           ((0,1), (1,1), 1), ((1,0), (1,1), 3),
                           ((1,1), (2,1), 2), ((1,1), (1,2), 3),
                           ((2,1), (2,2), 1), ((1,2), (2,2), 2)])

# Set layout
pos = nx.spring_layout(G)

# Set up animation
fig, ax = plt.subplots()
def animate(i):
    path = best_first_search_animation(G, (0,0), (2,2))
    return ax.collections + ax.lines + ax.texts

anim = FuncAnimation(fig, animate, frames=range(60), interval=1000, repeat=False)

plt.show()
