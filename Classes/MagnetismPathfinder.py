import heapq
from typing import Set, Tuple, List
import os
import sys

# Boilerplate to ensure imports work
absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Point import Point
from Edge import Edge
from Vertex import Vertex, VertexType

class MagnetismPathfinder:
    def __init__(self, existing_edges: List[Edge], grid_size: Tuple[int, int]):
        self.width, self.height = grid_size
        # Store occupied unit segments for O(1) lookup
        # Format: tuple of sorted tuples ((x1, y1), (x2, y2))
        self.occupied_segments: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
        self._rasterize_edges(existing_edges)

    def _rasterize_edges(self, edges: List[Edge]):
        """
        Breaks down long edges into unit steps so the A* can 'ride' them.
        Assumes edges are grid-aligned (Manhattan).
        """
        for edge in edges:
            x1, y1 = int(edge.start.x), int(edge.start.y)
            x2, y2 = int(edge.end.x), int(edge.end.y)
            
            # Determine direction
            dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
            dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
            
            curr_x, curr_y = x1, y1
            
            # Walk the edge and mark segments
            while (curr_x != x2 or curr_y != y2):
                next_x = curr_x + dx
                next_y = curr_y + dy
                
                # Create a normalized key for the segment (sorted points)
                p1 = (curr_x, curr_y)
                p2 = (next_x, next_y)
                segment_key = tuple(sorted((p1, p2)))
                
                self.occupied_segments.add(segment_key)
                
                curr_x, curr_y = next_x, next_y

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        # Manhattan distance is best for grid-based metro maps
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Point, end: Point, magnetism_factor: float) -> List[Point]:
        """
        A* Search that discounts movement along existing edges based on magnetism_factor (0 to 1).
        """
        start_node = (int(start.x), int(start.y))
        target_node = (int(end.x), int(end.y))
        
        # Priority Queue: (Total Cost f(n), Current Cost g(n), Current Node, Path)
        open_set = [(0, 0, start_node, [Point(start_node[0], start_node[1])])]
        visited = set()
        
        # Base cost to move 1 unit
        base_cost = 1.0
        
        # The cost to move along an existing edge. 
        # If M=1, cost is 0.1 (sticky). If M=0, cost is 1.0 (same as empty space).
        # We keep a small epsilon (0.1) so it doesn't loop infinitely.
        magnetized_cost = base_cost * (1.0 - (magnetism_factor * 0.9))

        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            
            if current == target_node:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            # Explore Neighbors (Up, Down, Left, Right)
            neighbors = [
                (current[0], current[1] - 1), # Up
                (current[0], current[1] + 1), # Down
                (current[0] - 1, current[1]), # Left
                (current[0] + 1, current[1])  # Right
            ]
            
            for next_node in neighbors:
                nx, ny = next_node
                
                # Bounds check (optional, depending on if your grid is infinite)
                if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height:
                    continue
                
                if next_node in visited:
                    continue

                # Calculate movement cost
                # Check if the segment (current -> next) exists in our occupied set
                segment_key = tuple(sorted((current, next_node)))
                is_magnetized = segment_key in self.occupied_segments
                
                step_cost = magnetized_cost if is_magnetized else base_cost
                new_g = g + step_cost
                new_f = new_g + self._heuristic(next_node, target_node)
                
                new_path = path + [Point(nx, ny)]
                heapq.heappush(open_set, (new_f, new_g, next_node, new_path))
                
        # Fallback if no path found (shouldn't happen in free grid)
        return [start, end]

    @staticmethod
    def points_to_edges(path: List[Point]) -> List[Edge]:
        """Converts the raw point path into simplified Edge objects."""
        if len(path) < 2:
            return []
            
        edges = []
        # Simple simplification: Keep creating edges until direction changes
        # This prevents creating 100 edges for a straight line of 100 pixels
        
        segment_start = path[0]
        if len(path) == 2:
             return [Edge(path[0], path[1])]

        # Determine initial direction
        last_dx = path[1].x - path[0].x
        last_dy = path[1].y - path[0].y
        
        for i in range(2, len(path)):
            curr = path[i]
            prev = path[i-1]
            
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            
            # If direction changed, close the previous edge and start a new one
            if dx != last_dx or dy != last_dy:
                edges.append(Edge(segment_start, prev))
                segment_start = prev
                last_dx = dx
                last_dy = dy
        
        # Add final edge
        edges.append(Edge(segment_start, path[-1]))
        
        return edges
    
    @staticmethod
    def process_path_into_segment_data(path: List[Point]) -> Tuple[List[Edge], List[Vertex]]:
        """
        Converts a raw path of points into a list of Edges and Corner Vertices.
        Detects direction changes to place VertexType.CORNER at intersections.
        """
        if len(path) < 2:
            return [], []

        edges: List[Edge] = []
        corners: List[Vertex] = []

        # Start the first segment
        segment_start = path[0]
        
        # Calculate initial direction
        # We need to handle the case where the first few points might be identical (though A* shouldn't do that)
        last_dx, last_dy = 0, 0
        for i in range(1, len(path)):
            dx = path[i].x - path[i-1].x
            dy = path[i].y - path[i-1].y
            if dx != 0 or dy != 0:
                last_dx, last_dy = dx, dy
                break

        # Iterate through points to find turns
        for i in range(2, len(path)):
            curr = path[i]
            prev = path[i-1]
            
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            
            # Check if direction changed
            # (dx != last_dx or dy != last_dy) works for grid movement (0, 1) vs (1, 0)
            if dx != last_dx or dy != last_dy:
                # 1. Create the incoming edge (Start -> Turn)
                incoming_edge = Edge(segment_start, prev)
                edges.append(incoming_edge)
                
                # 2. Create the Corner Vertex at the turn point (prev)
                # We initialize it with the incoming edge; we'll add the outgoing edge next
                corner = Vertex(VertexType.CORNER, prev, edges=[incoming_edge])
                corners.append(corner)
                
                # 3. Update state for the new segment
                segment_start = prev
                last_dx = dx
                last_dy = dy
        
        # Add the final edge (Last Turn -> End)
        final_edge = Edge(segment_start, path[-1])
        edges.append(final_edge)
        
        # Link the final edge to the last corner if it exists
        if corners:
            corners[-1].add_edge(final_edge)

        # Link intermediate edges to their respective corners
        # A corner at index 'i' connects edges 'i' (incoming) and 'i+1' (outgoing)
        for i, corner in enumerate(corners):
            if i + 1 < len(edges):
                # Ensure the corner knows about its outgoing edge
                # The Vertex init above added the incoming one.
                if edges[i+1] not in corner.edges:
                    corner.add_edge(edges[i+1])

        return edges, corners