import tkinter as tk
from tkinter import messagebox
import time
import random

# --- GUI Class --- #
class SearchVisualizer:
    
    # setting up the vizualization
    def __init__(self, root):
        self.root = root
        self.root.title("Uninformed Search Visualization (DFS & BFS)")
        self.root.geometry("1000x700")

        # Create Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.node_count_label = tk.Label(control_frame, text="Number of Nodes:")
        self.node_count_label.grid(row=0, column=0, padx=5)

        self.node_count_entry = tk.Entry(control_frame, width=5)
        self.node_count_entry.grid(row=0, column=1, padx=5)
        self.node_count_entry.insert(0, "7")

        self.generate_button = tk.Button(control_frame, text="Generate Tree", command=self.create_tree_graph)
        self.generate_button.grid(row=0, column=2, padx=10)

        self.dfs_button = tk.Button(control_frame, text="Run DFS", command=self.run_dfs)
        self.dfs_button.grid(row=0, column=3, padx=10)

        self.bfs_button = tk.Button(control_frame, text="Run BFS", command=self.run_bfs)
        self.bfs_button.grid(row=0, column=4, padx=10)

        # Create Canvas to Draw Graph
        self.canvas = tk.Canvas(self.root, width=950, height=600, bg="white")
        self.canvas.pack(pady=20)

        # Placeholder for Graph Data
        self.nodes = {}
        self.edges = []
        self.node_widgets = {}

        self.create_tree_graph()

    def create_tree_graph(self):
        try:
            N = int(self.node_count_entry.get())
            if N < 2:
                messagebox.showerror("Error", "Number of nodes must be at least 2.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        self.canvas.delete("all")
        self.nodes = {}
        self.edges = []
        self.node_widgets = {}

        # Create nodes in levels like a tree
        levels = []
        level = 0
        count = 0
        while count < N:
            nodes_in_level = min(2 ** level, N - count) # each level has 2 ** n nodes
            levels.append(nodes_in_level)
            count += nodes_in_level
            level += 1

        y_gap = 100
        node_index = 0
        for lvl, num_nodes in enumerate(levels):
            x_gap = 900 // (num_nodes + 1)
            for i in range(num_nodes):
                x = (i + 1) * x_gap
                y = (lvl + 1) * y_gap
                node_name = chr(65 + node_index)  # A, B, C, ... above 26 letters, you get non letters
                self.nodes[node_name] = (x, y)
                node_index += 1

        node_list = list(self.nodes.keys())
        for i in range(1, len(node_list)):
            parent_index = (i - 1) // 2
            self.edges.append((node_list[parent_index], node_list[i]))

        for edge in self.edges:
            x1, y1 = self.nodes[edge[0]]
            x2, y2 = self.nodes[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2)

        for node, (x, y) in self.nodes.items():
            oval = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue", tags=node)
            text = self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))
            self.node_widgets[node] = oval

    # helper code for resetting node colors after calling dfs and bfs respectively
    def reset_node_colors(self):
        for node in self.node_widgets:
            self.canvas.itemconfig(self.node_widgets[node], fill="lightblue")
        self.root.update()

    # helper code for highlighting node colors after calling dfs and bfs respectively
    def highlight_node(self, node):
        self.canvas.itemconfig(self.node_widgets[node], fill="yellow")
        self.root.update()
        time.sleep(0.5)

    def run_dfs(self):
        self.reset_node_colors()
        visited = set()

        def dfs(current):
            if current in visited:
                return
            visited.add(current)
            self.highlight_node(current)
            for neighbor in self.get_neighbors(current):
                dfs(neighbor)

        messagebox.showinfo("DFS", "Starting Depth-First Search...")
        start_node = list(self.nodes.keys())[0]
        dfs(start_node)

    def run_bfs(self):
        self.reset_node_colors()
        visited = set()
        queue = [list(self.nodes.keys())[0]]

        messagebox.showinfo("BFS", "Starting Breadth-First Search...")

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                self.highlight_node(current)
                queue.extend([n for n in self.get_neighbors(current) if n not in visited])

    # helper nodes for getting neighbors
    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append(edge[1])
            elif edge[1] == node:
                neighbors.append(edge[0])
        return neighbors

# --- Main Program --- #
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchVisualizer(root)
    root.mainloop()
