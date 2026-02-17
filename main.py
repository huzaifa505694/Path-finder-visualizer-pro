import pygame
import time
from environment import GridEnvironment
from ALGORITHM import SearchAlgorithms

# --- Configuration ---
WINDOW_TITLE = "Pathfinding Visualizer Pro"
GRID_SIZE = 20
CELL_SIZE = 35  
GRID_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
PANEL_WIDTH = 350 
SCREEN_WIDTH = GRID_PIXEL_SIZE + PANEL_WIDTH
SCREEN_HEIGHT = GRID_PIXEL_SIZE

# --- Modern Color Palette ---
WHITE = (255, 255, 255)
GRID_BG = (236, 240, 241) 
GRID_LINES = (220, 225, 225)

# Node Colors
GREEN = (46, 204, 113)   
BLUE = (52, 152, 219)    
RED = (231, 76, 60)      
DARK_GRAY = (52, 73, 94) 
ORANGE = (243, 156, 18)  
LIGHT_BLUE = (100, 200, 240) 
YELLOW = (241, 196, 15)  
CYAN = (26, 188, 156)    

# UI Panel Colors
PANEL_BG = (44, 62, 80)  
TEXT_WHITE = (236, 240, 241)
TEXT_GRAY = (189, 195, 199)
BTN_NORMAL = (52, 73, 94)
BTN_HOVER = (65, 90, 115)
BTN_ACTIVE = (39, 174, 96) 
STATUS_BG = (30, 45, 60)

class Button:
    def __init__(self, x, y, w, h, text, action_code):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action_code = action_code
        self.is_hovered = False

    def draw(self, screen, font, is_active=False):
        if is_active:
            color = BTN_ACTIVE
            border_c = (46, 204, 113)
        elif self.is_hovered:
            color = BTN_HOVER
            border_c = (85, 110, 140)
        else:
            color = BTN_NORMAL
            border_c = (40, 55, 70)

        # Shadow & Body
        pygame.draw.rect(screen, (30, 40, 50), (self.rect.x + 2, self.rect.y + 4, self.rect.w, self.rect.h), border_radius=8)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, border_c, self.rect, 2, border_radius=8)
        
        text_surf = font.render(self.text, True, TEXT_WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class PathfinderApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        self.title_font = pygame.font.SysFont('Segoe UI', 26, bold=True) 
        self.header_font = pygame.font.SysFont('Segoe UI', 16, bold=True)
        self.btn_font = pygame.font.SysFont('Segoe UI', 14)
        self.stats_font = pygame.font.SysFont('Consolas', 13) 
        self.cell_font = pygame.font.SysFont('Arial', 18, bold=True)

        self.env = GridEnvironment(GRID_SIZE)
        self.algo = SearchAlgorithms(GRID_SIZE)
        
        self.start = (2, 2)
        self.target = (17, 17)
        self.current_pos = self.start
        
        self.status_msg = "Ready"
        self.nodes_visited = 0
        self.path_len = 0
        self.is_dragging = False 
        self.animation_speed = 0.02 
        self.speed_label = "Fast"
        self.current_mode = 'WALL' 
        
        self.setup_ui()
        self.env.add_static_wall(5, 5, 10)

    def setup_ui(self):
        # --- FIXED SPACING TO PREVENT OVERLAP ---
        btn_w = 280
        btn_h = 32  # Smaller height
        gap = 8     # Smaller gap
        center_x = GRID_PIXEL_SIZE + (PANEL_WIDTH - btn_w) // 2
        
        self.buttons = []
        self.header_y_positions = {}

        # 1. Algorithms Section
        current_y = 65 
        self.header_y_positions["ALGORITHMS"] = current_y
        current_y += 30 # Space after header

        algo_names = [
            "BFS (Breadth-First)", "DFS (Depth-First)", "UCS (Uniform-Cost)", 
            "DLS (Depth-Limited)", "IDDFS (Iterative Deep)", "Bidirectional Search"
        ]
        
        for i, name in enumerate(algo_names):
            self.buttons.append(Button(center_x, current_y, btn_w, btn_h, f"{i+1}. {name}", i+1))
            current_y += btn_h + gap

        # 2. Map Controls Section
        current_y += 15 # Section Spacer
        self.header_y_positions["MAP EDITOR"] = current_y
        current_y += 30

        half_w = (btn_w - gap) // 2
        self.btn_set_start = Button(center_x, current_y, half_w, btn_h, "Set Start (S)", 'SET_S')
        self.btn_set_target = Button(center_x + half_w + gap, current_y, half_w, btn_h, "Set Target (T)", 'SET_T')
        self.buttons.extend([self.btn_set_start, self.btn_set_target])
        
        current_y += btn_h + gap
        self.btn_map_mode = Button(center_x, current_y, btn_w, btn_h, "Map: Custom Wall", 'TOGGLE_MAP')
        self.buttons.append(self.btn_map_mode)

        # 3. Simulation Controls
        current_y += 15 # Section Spacer (More breathing room)
        current_y += btn_h + gap # Push down slightly
        
        self.header_y_positions["SIMULATION"] = current_y
        current_y += 30

        self.buttons.append(Button(center_x, current_y, half_w, btn_h, "Reset (R)", 'R'))
        self.speed_btn = Button(center_x + half_w + gap, current_y, half_w, btn_h, f"Speed: {self.speed_label}", 'S')
        self.buttons.append(self.speed_btn)

    def draw_grid_cell(self, r, c, color):
        rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, GRID_LINES, rect, 1) 
        
        if (r, c) == self.start: 
            text = self.cell_font.render("S", True, WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))
        if (r, c) == self.target:
            text = self.cell_font.render("T", True, WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def draw_ui(self):
        # 1. Backgrounds
        self.screen.fill(GRID_BG)
        panel_rect = pygame.Rect(GRID_PIXEL_SIZE, 0, PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)

        # 2. Draw Grid Cells
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                color = WHITE 
                if self.env.grid[r][c] == -1: color = DARK_GRAY
                elif (r, c) in self.traced_set: color = CYAN 
                elif (r, c) in self.path_set: color = YELLOW
                elif (r, c) in self.explored_set: color = LIGHT_BLUE
                elif (r, c) in self.frontier_set: color = ORANGE
                if (r, c) == self.start: color = GREEN
                if (r, c) == self.target: color = BLUE
                if (r, c) == self.current_pos: color = RED
                self.draw_grid_cell(r, c, color)

        # 3. Panel Title & Headers
        title_surf = self.title_font.render("SEARCHING VISUALIZER", True, TEXT_WHITE)
        self.screen.blit(title_surf, (GRID_PIXEL_SIZE + 20, 15))
        
        # Dynamic Section Headers
        for text, y_pos in self.header_y_positions.items():
            self.screen.blit(self.header_font.render(text, True, TEXT_GRAY), (GRID_PIXEL_SIZE + 35, y_pos))

        # 4. Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.is_hovered = btn.rect.collidepoint(mouse_pos)
            is_active = False
            if btn.action_code == 'SET_S' and self.current_mode == 'START': is_active = True
            if btn.action_code == 'SET_T' and self.current_mode == 'TARGET': is_active = True
            btn.draw(self.screen, self.btn_font, is_active)
            
        # 5. Status Dashboard (Fixed Bottom)
        # Positioned securely at the bottom to avoid overlap
        dash_y = SCREEN_HEIGHT - 110
        dash_rect = pygame.Rect(GRID_PIXEL_SIZE + 20, dash_y, PANEL_WIDTH - 40, 90)
        pygame.draw.rect(self.screen, STATUS_BG, dash_rect, border_radius=12)
        pygame.draw.rect(self.screen, (60, 80, 100), dash_rect, 2, border_radius=12)
        
        stats = [
            f"STATUS:  {self.status_msg}",
            f"VISITED: {self.nodes_visited}",
            f"LENGTH:  {self.path_len}",
            f"MODE:    {self.current_mode}"
        ]
        
        for i, line in enumerate(stats):
            col = CYAN if i == 0 else TEXT_WHITE
            text = self.stats_font.render(line, True, col)
            self.screen.blit(text, (GRID_PIXEL_SIZE + 35, dash_y + 12 + (i * 19)))

        pygame.display.flip()

    def handle_grid_click(self, r, c):
        if self.current_mode == 'START':
            if (r, c) != self.target and self.env.grid[r][c] != -1:
                self.start = (r, c)
                self.current_pos = (r, c)
        elif self.current_mode == 'TARGET':
            if (r, c) != self.start and self.env.grid[r][c] != -1:
                self.target = (r, c)
        elif self.current_mode == 'WALL':
            if (r, c) != self.start and (r, c) != self.target:
                self.env.toggle_obstacle(r, c)

    def viz_callback(self, node, frontier, explored):
        self.nodes_visited = len(explored)
        self.frontier_set = set(frontier)
        self.explored_set = set(explored)
        self.draw_ui()
        time.sleep(self.animation_speed)
        pygame.event.pump()

    def move_agent(self, path):
        if not path: return
        self.path_set, self.path_len = set(path), len(path)
        self.draw_ui()
        time.sleep(0.5)
        self.status_msg = "Moving Agent..."
        self.traced_set = set() 
        for i in range(1, len(path)):
            self.traced_set.add(self.current_pos)
            self.current_pos = path[i]
            self.traced_set.add(self.current_pos)
            self.draw_ui()
            time.sleep(0.15) 
        self.status_msg = "Target Reached!"

    def run_algo(self, code):
        self.last_algo_code = code
        self.nodes_visited = 0
        self.frontier_set, self.explored_set, self.path_set, self.traced_set = set(), set(), set(), set()
        self.status_msg = "Searching..."
        if self.current_pos == self.target: self.current_pos = self.start
            
        methods = {
            1: lambda: self.algo.bfs(self.current_pos, self.target, self.env.grid, self.viz_callback),
            2: lambda: self.algo.dfs(self.current_pos, self.target, self.env.grid, self.viz_callback),
            3: lambda: self.algo.ucs(self.current_pos, self.target, self.env.grid, self.viz_callback),
            4: lambda: self.algo.dls(self.current_pos, self.target, self.env.grid, 20, self.viz_callback),
            5: lambda: self.algo.iddfs(self.current_pos, self.target, self.env.grid, 30, self.viz_callback),
            6: lambda: self.algo.bidirectional_search(self.current_pos, self.target, self.env.grid, self.viz_callback)
        }
        
        if code in methods:
            path = methods[code]()
            if path: self.move_agent(path)
            else: self.status_msg = "No Path Found!"

    def toggle_speed(self):
        self.animation_speed = 0.1 if self.speed_label == "Fast" else 0.02
        self.speed_label = "Slow" if self.speed_label == "Fast" else "Fast"
        self.speed_btn.text = f"Speed: {self.speed_label}"

    def toggle_map_mode(self):
        if self.btn_map_mode.text == "Map: Custom Wall":
            self.btn_map_mode.text = "Map: Auto Maze"
            self.env.generate_maze()
            self.status_msg = "Maze Generated"
        elif self.btn_map_mode.text == "Map: Auto Maze":
            self.btn_map_mode.text = "Map: Trap Case"
            self.env.reset_grid()
            sr, sc = self.start
            points = [(sr-1, sc+1), (sr, sc+1), (sr+1, sc+1), (sr-1, sc), (sr-1, sc-1), (sr+1, sc), (sr+1, sc-1)]
            for r, c in points:
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    self.env.grid[r][c] = -1
                    self.env.static_obstacles.add((r, c))
            self.status_msg = "Trap Generated"
        else:
            self.btn_map_mode.text = "Map: Custom Wall"
            self.env.reset_grid()
            self.status_msg = "Map Cleared"
        self.current_pos = self.start
        self.frontier_set, self.explored_set, self.path_set, self.traced_set = set(), set(), set(), set()

    def run(self):
        running = True
        self.frontier_set, self.explored_set, self.path_set, self.traced_set = set(), set(), set(), set()
        while running:
            self.draw_ui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if mx < GRID_PIXEL_SIZE: 
                        self.is_dragging = True
                        self.handle_grid_click(my // CELL_SIZE, mx // CELL_SIZE)
                    else: 
                        for btn in self.buttons:
                            if btn.check_click((mx, my)):
                                if isinstance(btn.action_code, int): self.run_algo(btn.action_code)
                                elif btn.action_code == 'R': 
                                    self.env.reset_grid()
                                    self.current_pos = self.start
                                    self.frontier_set, self.explored_set, self.path_set, self.traced_set = set(), set(), set(), set()
                                elif btn.action_code == 'C': self.env.clean_dynamic()
                                elif btn.action_code == 'S': self.toggle_speed()
                                elif btn.action_code == 'TOGGLE_MAP': self.toggle_map_mode()
                                elif btn.action_code == 'SET_S': 
                                    if self.current_mode == 'START':
                                        self.current_mode = 'WALL' 
                                        self.status_msg = "Mode: Draw Walls"
                                    else:
                                        self.current_mode = 'START'
                                        self.status_msg = "Mode: Set Start"
                                elif btn.action_code == 'SET_T': 
                                    if self.current_mode == 'TARGET':
                                        self.current_mode = 'WALL' 
                                        self.status_msg = "Mode: Draw Walls"
                                    else:
                                        self.current_mode = 'TARGET'
                                        self.status_msg = "Mode: Set Target"
                                        
                elif event.type == pygame.MOUSEBUTTONUP: self.is_dragging = False
                elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                    mx, my = pygame.mouse.get_pos()
                    if mx < GRID_PIXEL_SIZE: self.handle_grid_click(my // CELL_SIZE, mx // CELL_SIZE)

if __name__ == "__main__":
    app = PathfinderApp()
    app.run()