Here is the updated **README.md** with a dedicated section for you and your partner.

---

```markdown
# 🔍 Searching Visualizer

A powerful, interactive Python application built with **Pygame** to visualize how various **Uninformed Search Algorithms** work in a grid environment. This tool allows users to create custom maps, generate mazes, and watch AI agents find their way from a Start point to a Target using different strategies.

## 🚀 Features

* **6 Core Search Algorithms:** Visualizes BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search.
* **Interactive Map Editor:**
    * **Draw Walls:** Click and drag to create custom barriers.
    * **Set Points:** Easily toggle modes to place the **Start (S)** and **Target (T)** nodes.
    * **Auto Maze:** Generates a perfect maze using a Recursive Backtracker algorithm.
    * **Trap Patterns:** Pre-loaded map patterns to test algorithm limitations (e.g., DFS getting stuck).
* **Real-Time Visualization:**
    * Watch the algorithm "flood" the grid (Orange/Blue nodes).
    * See the **Planned Path** (Yellow) once a solution is found.
    * Watch the **Agent Trace** (Cyan) as it physically traverses the path.
* **Live Dashboard:** Displays real-time metrics including **Nodes Visited** and **Path Length**.
* **Custom Movement Logic:** Implements a specific 6-direction movement pattern (excluding Top-Right and Bottom-Left diagonals).
* **Modern UI:** A clean, dark-themed control panel with intuitive buttons and status feedback.

## 🛠️ Prerequisites

To run this project, you need to have **Python 3.x** installed along with the **Pygame** library.

### Installation

1.  **Clone the Repository** (or download the files):
    ```bash
    git clone [https://github.com/your-username/searching-visualizer.git](https://github.com/your-username/searching-visualizer.git)
    cd searching-visualizer
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pygame
    ```

## 🎮 How to Run

Execute the main script to launch the application:

```bash
python main.py

```

## 🕹️ Controls & Usage

The application features a side control panel for easy interaction.

### **Map Controls**

| Button / Action | Description |
| --- | --- |
| **Left Click (Grid)** | Draw Walls, or place Start/Target if that mode is active. |
| **Set Start (S)** | Switch click mode to place the **Green Start Node**. |
| **Set Target (T)** | Switch click mode to place the **Blue Target Node**. |
| **Map: Custom Wall** | Toggle between **Custom**, **Auto Maze**, and **Trap** map modes. |
| **Reset (R)** | Clears the grid and resets all search states. |

### **Simulation Controls**

| Button / Action | Description |
| --- | --- |
| **Algorithms (1-6)** | Starts the selected search algorithm immediately. |
| **Speed: Fast/Slow** | Toggles the visualization speed. |

## 🧠 Algorithms Implemented

1. **Breadth-First Search (BFS):** Explores neighbor nodes level by level. Guarantees the shortest path in unweighted graphs.
2. **Depth-First Search (DFS):** Explores as far as possible along each branch before backtracking. Not guaranteed to find the shortest path.
3. **Uniform-Cost Search (UCS):** Explores paths based on the lowest cumulative cost.
4. **Depth-Limited Search (DLS):** A DFS traversal with a specific depth limit to prevent infinite searching.
5. **Iterative Deepening DFS (IDDFS):** Combines the space efficiency of DFS with the completeness of BFS by repeatedly running DLS with increasing depth limits.
6. **Bidirectional Search:** Runs two simultaneous searches (one from Start, one from Target) that meet in the middle, often significantly reducing search time.

## 📂 Project Structure

* `main.py`: The entry point of the application. Handles the GUI, user input, and the main game loop.
* `environment.py`: Manages the grid logic, static obstacles, and map generation algorithms (like maze generation).
* `ALGORITHM.py`: Contains the `SearchAlgorithms` class with the implementation of all 6 pathfinding strategies and neighbor logic.

## 👥 Authors / Team Members

| Name | Roll Number |
| --- | --- |
| **[Huzaifa Waqar]** | **[24F-0013]** |
| **[Aairus Irfan]** | **[24F-0043]** |

**Course:** AI 2002 - Artificial Intelligence
**Semester:** Spring 2026

## 🎨 Legend

* 🟩 **Green:** Start Node
* 🟦 **Blue:** Target Node
* ⬛ **Dark Gray:** Wall / Obstacle
* 🟧 **Orange:** Frontier (Nodes being considered)
* 💠 **Light Blue:** Explored (Nodes already visited)
* 🟨 **Yellow:** Final Calculated Path
* 🟦 **Cyan:** Actual path taken by the agent

---

*Created for AI 2002 - Artificial Intelligence Assignment.*

```

```
