import gc
import heapq

import sys
from VEXLib.Geometry.GeometryUtil import distance, hypotenuse
from VEXLib.Util.PathfindingEnvironment import PathfindingEnvironment


class DijkstraPathfinding:
    """
    Dijkstra's algorithm implementation to find the shortest path between two points on a 2D grid.

    Attributes:
        _start_position (tuple): The starting position as a tuple (x, y).
        _target_position (tuple): The goal position as a tuple (x, y).
        _valid_moves (list of tuples): A list of valid moves that an agent can make in the environment.
        _open_heap (list): A list to store nodes to be explored, ordered by cost.
        _closed_set (list): A list to store nodes that have been explored.
        _parent_dict (dict): A dictionary that maps child nodes to their parent nodes in the path.
        _g_values (dict): A dictionary that stores the cost from the start position to each node.
    """

    def __init__(self, start_pos, goal_pos, accessible_tiles_file_object, valid_moves):
        """
        Initialize the Dijkstra algorithm with start and goal points.

        Args:
            start_pos (tuple[int, int]): An (x, y) point representing the starting point.
            goal_pos (tuple[int, int]): An (x, y) point representing the goal point.
        """
        self._start_position = start_pos
        self._target_position = goal_pos
        self._valid_moves = valid_moves
        self._move_costs = {
            move: hypotenuse(*move) for move in valid_moves
        }
        self.pathfinding_environment = PathfindingEnvironment()
        self.pathfinding_environment.load_from_file(accessible_tiles_file_object)

        # self._open_heap = BinaryHeap()
        self._open_heap = []
        self._closed_set = set()
        self._parent_dict = {}
        self._g_values = {}

    def _insert_to_open_list(self, item):
        """
        Insert a node into the open_list while maintaining the sorted order based on the cost.

        Args:
            item (tuple[float, tuple[int, int]]): (cost, position) to be inserted into the open_list.
        """
        heapq.heappush(self._open_heap, item)
        # self._open_heap.push(item)

    def _pop_lowest_cost_node(self):
        """
        Remove and return the node with the lowest cost from the open_list.

        Returns:
            lowest_cost_node (tuple[float, tuple[int, int]]): The (cost, position) of the lowest cost node.
        """
        return heapq.heappop(self._open_heap)
        # return self._open_heap.pop()

    def find_path(self):
        """
        Find the shortest path from the start position to the goal position using Dijkstra's algorithm.

        Returns:
             Tuple containing the path as a list of positions and the list of visited positions.
        """
        self._parent_dict[self._start_position] = self._start_position
        self._g_values[self._start_position] = 0
        self._g_values[self._target_position] = float("inf")
        self._insert_to_open_list((0, self._start_position))

        # Sanity checks

        assert (
            self.pathfinding_environment.is_available(self._start_position)
        ), 'Tile "start_position" is not in accessible_tiles'
        assert (
            self.pathfinding_environment.is_available(self._target_position)
        ), 'Tile "target_position" is not in accessible_tiles'

        while self._open_heap:
            _, current_pos = self._pop_lowest_cost_node()

            self._closed_set.add(current_pos)

            if current_pos == self._target_position:
                break

            for neighbor_pos in self._get_valid_neighbors(current_pos):
                # new_cost = self._g_values[current_pos] + self._calculate_cost(
                #     current_pos, neighbor_pos
                # )
                if self._is_collision(current_pos, neighbor_pos):
                    move_cost = float("inf")
                else:
                    move_cost = self._move_costs[abs(current_pos[0] - neighbor_pos[0]), abs(current_pos[1] - neighbor_pos[1])]

                # print(f"Additional cost: {move_cost}")
                # print(f"Total node cost: {self._g_values[current_pos] + move_cost}")
                new_cost = self._g_values[current_pos] + move_cost

                if neighbor_pos not in self._g_values:
                    self._g_values[neighbor_pos] = float("inf")

                if new_cost < self._g_values[neighbor_pos]:
                    self._g_values[neighbor_pos] = new_cost
                    self._parent_dict[neighbor_pos] = current_pos
                    self._insert_to_open_list((new_cost, neighbor_pos))

        gc.collect()

        # print(self._open_heap)
        # print(self._closed_set)
        # print(self._g_values)
        # print(self._parent_dict)

        print(f"Open heap: {sys.getsizeof(self._open_heap)}")
        print(f"Closed heap: {sys.getsizeof(self._closed_set.copy())}")
        print(f"G values: {sys.getsizeof(self._g_values.copy())}")
        print(f"Parent dict: {sys.getsizeof(self._parent_dict.copy())}")

        # print("Time taken: " + str(round((time.perf_counter() - start_time) * 1000)) + "ms")
        return self._extract_path(self._parent_dict), self._closed_set

    def _get_valid_neighbors(self, pos):
        """
        Get valid neighboring positions from the given position.

        :param pos: Tuple (x, y) representing the current position.
        :return: List of tuples representing the valid neighboring positions.
        """
        return {(pos[0] + move[0], pos[1] + move[1]) for move in self._valid_moves}

    def _calculate_cost(self, start_pos, end_pos):
        """
        Calculate the cost from the start position to the end position.

        :param start_pos: Tuple (x, y) representing the start position.
        :param end_pos: Tuple (x, y) representing the end position.
        :return: Float value representing the cost from the start position to the end position.
        """
        if self._is_collision(start_pos, end_pos):
            return float("inf")

        return distance(start_pos, end_pos)

    def _is_collision(self, start_pos, end_pos):
        """
        Check if there is a collision between the start and end positions with obstacles.

        :param start_pos: Tuple (x, y) representing the start position.
        :param end_pos: Tuple (x, y) representing the end position.
        :return: True if there is a collision, False otherwise.
        """
        return self.pathfinding_environment.is_collision(end_pos) or self.pathfinding_environment.is_collision(start_pos)

    def _extract_path(self, parent_dict):
        """
        Extract the path from the parent_dict starting from the goal position to the start position.

        :param parent_dict: Dictionary mapping child positions to their parent positions.
        :return: List of tuples representing the path from the start position to the goal position.
        """
        path = [self._target_position]
        current_pos = self._target_position

        while True:
            assert current_pos in parent_dict, "Heap exhausted: No Path to target"

            current_pos = parent_dict[current_pos]
            path.append(current_pos)

            if current_pos == self._start_position:
                break

        path.reverse()
        return path
