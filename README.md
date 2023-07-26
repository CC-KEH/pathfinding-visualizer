# Pathfinding and Maze Generation Algorithms

This repository contains various pathfinding algorithms and maze generation algorithms implemented in Python using Pygame. These algorithms can be visualized on a grid-based maze.

## Pathfinding Algorithms
1. A* Search Algorithm
2. Bidirectional A* Search Algorithm
3. Iterative Deepening A* (IDA*) Search Algorithm
4. Breadth-First Search (BFS) Algorithm
5. Depth-First Search (DFS) Algorithm
6. Bidirectional BFS (Bi-BFS) Algorithm
7. Dijkstra's Algorithm

## Maze Generation Algorithms
1. Maze Generation using Depth-First Search (DFS)
2. Maze Generation using the Random module

## Getting Started
1. Clone this repository to your local machine.
2. Make sure you have Python 3.x and Pygame installed.
3. Run the `main.py` file to launch the graphical interface.

## How to Use
1. Upon running the `main.py` file, you will see a grid-based maze on the screen.
2. Select the desired algorithm from the dropdown menu.
3. Click on the "Generate Maze" button to create a new maze using the selected algorithm.
4. Click on the "Find Path" button to visualize the selected pathfinding algorithm on the maze.
5. Left-click on any cell to add barriers (obstacles) to the maze.
6. Right-click on any cell to remove barriers.
7. The algorithm's progress will be animated, and the found path will be highlighted.

## About the Algorithms
- A* Search Algorithm: Finds the shortest path using a heuristic that estimates the distance from a node to the goal.
- Bidirectional A* Search Algorithm: Utilizes two A* searches to find the shortest path from both the start and the end simultaneously.
- Iterative Deepening A* (IDA*) Search Algorithm: A memory-efficient version of A* search that uses iterative deepening to find the shortest path.
- Breadth-First Search (BFS) Algorithm: Explores all possible nodes at the present depth before moving on to nodes at the next depth level.
- Depth-First Search (DFS) Algorithm: Explores as far as possible along each branch before backtracking.
- Bidirectional BFS (Bi-BFS) Algorithm: Uses two BFS searches, one from the start node and one from the end node, to find the shortest path.
- Dijkstra's Algorithm: Finds the shortest path from the start node to all other nodes in the graph.

## Maze Generation
- Maze Generation using Depth-First Search (DFS): Creates a maze using the depth-first search algorithm.
- Maze Generation using the Random module: Creates a maze using a randomized approach.

## Credits
The graphical interface is created using Pygame, a Python library for game development.

## Contributions
Contributions to this repository are welcome! If you have any improvements, bug fixes, or new algorithms to add, feel free to create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
