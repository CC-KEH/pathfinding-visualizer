import networkx as nx
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def heuristic(node, goal):
    # Calculate the heuristic distance from node to goal
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar_animation(G, start, goal):
    visited = set()
    frontier = [(0, start, None)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

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
            nx.draw(G, pos, node_color=colors, with_labels=True)
            plt.pause(0.1)
            return path

        visited.add(current)
        colors = ['yellow' if n == current else 'gray' if n in visited else 'white' for n in G.nodes()]
        nx.draw(G, pos, node_color=colors, with_labels=True)
        plt.pause(0.1)

        for neighbor in G.neighbors(current):
            if neighbor in visited:
                continue

            tentative_g_score = g_score[current] + G[current][neighbor]['weight']
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_score[neighbor], neighbor, current))

    return None

# Initialize graph
G = nx.Graph()
G.add_weighted_edges_from([((i,j), (i-1,j), 1) for i in range(5, 0, -1) for j in range(5, 0, -1) if i > 1] + [((i,j), (i,j-1), 1) for i in range(5, 0, -1) for j in range(5, 0, -1) if j > 1])

# Set layout
pos = {node: node for node in G.nodes()}

# Set up animation
fig, ax = plt.subplots()
def animate(i):
    path = astar_animation(G, (1,1), (5,5))
    return ax.collections + ax.lines + ax.texts

anim = FuncAnimation(fig, animate, frames=range(1), interval=500, repeat=False)

plt.show()
