import random

class GridEnvironment:
    def __init__(self, size=20):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        # REMOVED: specific logic for dynamic spawn probability essentially ignored by main.py
        self.obstacle_chance = 0.0 
        self.static_obstacles = set()
        self.dynamic_obstacles = set()

    def add_static_wall(self, start_row, col, length):
        for i in range(length):
            if start_row + i < self.size:
                r, c = start_row + i, col
                self.grid[r][c] = -1
                self.static_obstacles.add((r, c))

    def toggle_obstacle(self, r, c):
        if 0 <= r < self.size and 0 <= c < self.size:
            if self.grid[r][c] == -1:
                self.grid[r][c] = 0
                if (r, c) in self.static_obstacles:
                    self.static_obstacles.remove((r, c))
            else:
                self.grid[r][c] = -1
                self.static_obstacles.add((r, c))

    # NOTE: These methods remain but are unused by main.py
    def spawn_dynamic_obstacle(self, start, target, current_agent_pos):
        return None

    def reset_grid(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.static_obstacles.clear()
        self.dynamic_obstacles.clear()

    def clean_dynamic(self):
        for r, c in self.dynamic_obstacles:
            if (r, c) not in self.static_obstacles:
                self.grid[r][c] = 0
        self.dynamic_obstacles.clear()

    def generate_maze(self):
        self.reset_grid()
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = -1
                self.static_obstacles.add((r, c))
        def carve(r, c):
            self.grid[r][c] = 0
            if (r, c) in self.static_obstacles:
                self.static_obstacles.remove((r, c))
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == -1:
                    wr, wc = r + dr // 2, c + dc // 2
                    self.grid[wr][wc] = 0
                    if (wr, wc) in self.static_obstacles:
                        self.static_obstacles.remove((wr, wc))
                    carve(nr, nc)
        carve(0, 0)
        safe_spots = [(0, 0), (self.size-1, self.size-1), (2, 2), (17, 17)]
        for r, c in safe_spots:
            if 0 <= r < self.size and 0 <= c < self.size:
                self.grid[r][c] = 0
                if (r, c) in self.static_obstacles: self.static_obstacles.remove((r, c))