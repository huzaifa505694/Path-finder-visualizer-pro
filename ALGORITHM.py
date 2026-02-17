import collections
import heapq

class SearchAlgorithms:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        # --- MOVEMENT RESTRICTION APPLIED HERE ---
        # This list defines the valid moves for ALL algorithms.
        # EXCLUDED: Top-Right (-1, 1) and Bottom-Left (1, -1)
        # ORDER: Up, Right, Bottom, Bottom-Right, Left, Top-Left
        self.directions = [
            (-1, 0),  # Up
            (0, 1),   # Right
            (1, 0),   # Bottom
            (1, 1),   # Bottom-Right
            (0, -1),  # Left
            (-1, -1)  # Top-Left
        ]

    def get_neighbors(self, node, grid):
        """
        Returns a list of valid neighbors for a given node.
        Used by ALL algorithms, so the direction restriction applies globally.
        """
        neighbors = []
        r, c = node
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                # Check for walls (-1)
                if grid[nr][nc] != -1: 
                    neighbors.append((nr, nc))
        return neighbors

    # --- 1. BFS (Breadth-First Search) ---
    def bfs(self, start, target, grid, callback):
        queue = collections.deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == target: return self.reconstruct_path(visited, target)
            
            # BFS uses a Queue (FIFO), so we add neighbors in standard order.
            for neighbor in self.get_neighbors(current, grid):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
                    callback(neighbor, list(queue), visited.keys())
        return None

    # --- 2. DFS (Depth-First Search) - ITERATIVE ---
    def dfs(self, start, target, grid, callback):
        stack = [start]
        visited = {start: None}
        while stack:
            current = stack.pop()
            if current == target: return self.reconstruct_path(visited, target)
            
            # DFS uses a Stack (LIFO). 
            # To visit 'Up' first, we must push it LAST.
            # So we iterate through neighbors in REVERSE order.
            neighbors = self.get_neighbors(current, grid)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    visited[neighbor] = current
                    stack.append(neighbor)
                    callback(neighbor, list(stack), visited.keys())
        return None

    # --- 3. UCS (Uniform-Cost Search) ---
    def ucs(self, start, target, grid, callback):
        pq = [(0, start)]
        visited = {start: (0, None)}
        while pq:
            cost, current = heapq.heappop(pq)
            if current == target: return self.reconstruct_path_dict(visited, target)
            
            # UCS checks all neighbors.
            for neighbor in self.get_neighbors(current, grid):
                new_cost = cost + 1
                if neighbor not in visited or new_cost < visited[neighbor][0]:
                    visited[neighbor] = (new_cost, current)
                    heapq.heappush(pq, (new_cost, neighbor))
                    callback(neighbor, [n for c, n in pq], visited.keys())
        return None

    # --- 4. DLS (Depth-Limited Search) - ITERATIVE ---
    def dls(self, start, target, grid, limit, callback):
        stack = [(start, 0)]
        parent_map = {start: None}
        visited_depths = {start: 0}

        while stack:
            current, depth = stack.pop()
            if current == target: return self.reconstruct_path(parent_map, target)
            
            if depth < limit:
                neighbors = self.get_neighbors(current, grid)
                # DLS is stack-based, so we REVERSE neighbors here too.
                for neighbor in reversed(neighbors):
                    if neighbor not in visited_depths or (depth + 1) < visited_depths[neighbor]:
                        visited_depths[neighbor] = depth + 1
                        parent_map[neighbor] = current
                        stack.append((neighbor, depth + 1))
                        callback(neighbor, [n[0] for n in stack], visited_depths.keys())
        return None

    # --- 5. IDDFS (Iterative Deepening DFS) ---
    def iddfs(self, start, target, grid, max_depth, callback):
        # Calls DLS repeatedly, so it inherits the restriction and stack logic.
        for depth in range(max_depth):
            result = self.dls(start, target, grid, depth, callback)
            if result: return result
        return None

    # --- 6. Bidirectional Search ---
    def bidirectional_search(self, start, target, grid, callback):
        f_queue = collections.deque([start])
        b_queue = collections.deque([target])
        f_visited = {start: None}
        b_visited = {target: None}

        while f_queue and b_queue:
            # Forward step
            if f_queue:
                f_curr = f_queue.popleft()
                for n in self.get_neighbors(f_curr, grid):
                    if n not in f_visited:
                        f_visited[n] = f_curr
                        f_queue.append(n)
                        callback(n, list(f_queue), f_visited.keys())
                        if n in b_visited: return self.join_paths(f_visited, b_visited, n)
            
            # Backward step
            if b_queue:
                b_curr = b_queue.popleft()
                for n in self.get_neighbors(b_curr, grid):
                    if n not in b_visited:
                        b_visited[n] = b_curr
                        b_queue.append(n)
                        callback(n, list(b_queue), b_visited.keys())
                        if n in f_visited: return self.join_paths(f_visited, b_visited, n)
        return None

    # --- Helper Functions ---
    def join_paths(self, f_visited, b_visited, meeting_node):
        path_f = self.reconstruct_path(f_visited, meeting_node)
        path_b = []
        if meeting_node in b_visited:
            curr = b_visited[meeting_node]
            while curr is not None:
                path_b.append(curr)
                curr = b_visited[curr]
        return path_f + path_b

    def reconstruct_path(self, visited, current):
        path = []
        while current is not None:
            path.append(current)
            current = visited[current]
        return path[::-1]

    def reconstruct_path_dict(self, visited, current):
        path = []
        while current is not None:
            path.append(current)
            current = visited[current][1]
        return path[::-1]