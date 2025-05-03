import tkinter as tk
import random
import time
from copy import deepcopy

class TabuSearch8Puzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver with Tabu Search")

        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=10)

        self.tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", font=('Arial', 24), width=4, height=2)
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.tiles.append(row)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.scramble_btn = tk.Button(self.btn_frame, text="Scramble", command=self.scramble_board)
        self.scramble_btn.grid(row=0, column=0, padx=10)

        self.solve_btn = tk.Button(self.btn_frame, text="Solve with Tabu Search", command=self.solve)
        self.solve_btn.grid(row=0, column=1, padx=10)

        tk.Label(self.btn_frame, text="Tabu Tenure:").grid(row=0, column=2, padx=5)
        self.tenure_entry = tk.Entry(self.btn_frame, width=5)
        self.tenure_entry.insert(0, "10")
        self.tenure_entry.grid(row=0, column=3, padx=5)

        self.status_label = tk.Label(root, text="", font=('Arial', 12))
        self.status_label.pack(pady=5)

        self.state = []
        self.goal = [[1,2,3],[4,5,6],[7,8,0]]
        self.tabu_list = []
        self.iterations = 100

        self.scramble_board()

    def scramble_board(self):
        nums = list(range(9))
        random.shuffle(nums)
        self.state = [nums[i*3:(i+1)*3] for i in range(3)]
        self.update_board(self.state)
        self.status_label.config(text="")

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                self.tiles[i][j].config(text="" if val == 0 else str(val), bg="lightblue")
        self.root.update()

    def find_zero(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def get_neighbors(self, state):
        neighbors = []
        x, y = self.find_zero(state)
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def heuristic(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    goal_i, goal_j = divmod(val - 1, 3)
                    distance += abs(goal_i - i) + abs(goal_j - j)
        return distance

    def solve(self):
        try:
            tabu_tenure = int(self.tenure_entry.get())
        except ValueError:
            self.status_label.config(text="Invalid tabu tenure. Please enter a number.")
            return

        current = deepcopy(self.state)
        best = deepcopy(current)
        best_score = self.heuristic(best)
        self.tabu_list = []

        for iteration in range(self.iterations):
            neighbors = self.get_neighbors(current)
            candidates = []

            for neighbor in neighbors:
                if neighbor not in self.tabu_list:
                    candidates.append((neighbor, self.heuristic(neighbor)))

            if not candidates:
                break

            candidates.sort(key=lambda x: x[1])
            next_state, next_score = candidates[0]

            if next_score < best_score:
                best = deepcopy(next_state)
                best_score = next_score

            self.tabu_list.append(deepcopy(current))
            if len(self.tabu_list) > tabu_tenure:
                self.tabu_list.pop(0)

            current = deepcopy(next_state)
            self.update_board(current)
            self.status_label.config(text=f"Iteration {iteration+1} | Heuristic: {next_score} | Tabu List Size: {len(self.tabu_list)}")
            time.sleep(0.5)

            if current == self.goal:
                break

        self.update_board(best)
        if best == self.goal:
            self.status_label.config(text="Puzzle solved!")
        else:
            self.status_label.config(text=f"Best effort reached. Heuristic: {best_score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabuSearch8Puzzle(root)
    root.mainloop()
