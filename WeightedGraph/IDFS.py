import networkx as nx
import matplotlib.pyplot as plt


def iddfs_animation(G, start, goal, max_depth):
    # Initialize variables
    visited = set()
    colors = ['white' for _ in G.nodes()]
    frontier = [(start, 0)]
    depth_limit = 0
    found_goal = False
    came_from = {}

    # Loop until goal is found or max depth is reached
    while not found_goal and depth_limit <= max_depth:
        # Increment depth limit and reset visited and frontier sets
        depth_limit += 1
        visited = set()
        frontier = [(start, 0)]
        nx.draw(G, with_labels=True, node_color=colors)
        plt.pause(0.1)

        # Loop through the frontier
        while frontier:
            current, depth = frontier.pop()

            # Check if goal is found
            if current == goal:
                found_goal = True
                path = [current]
                parent = current
                while parent != start:
                    parent = came_from[parent]
                    path.append(parent)
                path.append(start)
                path.reverse()
                colors = ['yellow' if n in path else 'white' for n in G.nodes()]
                nx.draw(G, with_labels=True, node_color=colors)
                plt.pause(0.1)
                return path

            # Check if node has been visited and depth limit is not exceeded
            if current not in visited and depth < depth_limit:
                visited.add(current)
                colors = ['yellow' if n == current else 'white' for n in G.nodes()]
                nx.draw(G, with_labels=True, node_color=colors)
                plt.pause(0.1)

                # Add unvisited neighbors to frontier
                for neighbor in G.neighbors(current):
                    if neighbor not in visited:
                        frontier.append((neighbor, depth + 1))
                        came_from[neighbor] = current

    return None
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
path = iddfs_animation(G, 0, 6, 5)
print(path)
plt.show()