from enum import Enum
import tkinter as tk
from tkinter import messagebox
from search import Problem, astar_graph_search

class MapViewer:
    def __init__(self, nodes, max_cols, max_rows):
        self.nodes = nodes
        self.max_cols = max_cols
        self.max_rows = max_rows
        self.window = None
        self.animation_running = False
        self.canvas = None # Add canvas as an instance variable
        self.problem = None
        self.initial_state = None
        self.solution_actions = None
        self.animation_delay = 500

    def show(self):
        if self.window is not None:
            return  # Prevent multiple windows

        self.window = tk.Tk()
        self.window.title("Map Viewer")

        self.canvas = tk.Canvas(self.window, width=self.max_cols * 20, height=self.max_rows * 20, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.draw_map(self.nodes)
        self.add_legend(self.window)

        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Schedule the animation to start after a delay, within the mainloop
        if self.problem and self.initial_state and self.solution_actions:
            self.window.after(100, self._start_animation)

        self.window.mainloop()

    def _start_animation(self):
        self.animate_solution(self.problem, self.initial_state, self.solution_actions, self.animation_delay)

    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None

    @staticmethod
    def get_color(node_type):
        colors = {
            NodeType.FREE: "white",
            NodeType.WALL: "black",
            NodeType.BOX: "orange",
            NodeType.TARGET: "blue",
            NodeType.PLAYER: "green",
            NodeType.PLAYER_ON_TARGET: "lightgreen",
            NodeType.BOX_ON_TARGET: "yellow",
        }
        return colors.get(node_type, "gray")

    def add_legend(self, window):
        legend_frame = tk.Frame(window)
        legend_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(legend_frame, text="Legend", font=("Arial", 12, "bold")).pack(pady=5)

        legend_items = [
            (NodeType.FREE, "white", "Free Space"),
            (NodeType.WALL, "black", "Wall"),
            (NodeType.BOX, "orange", "Box"),
            (NodeType.TARGET, "blue", "Target"),
            (NodeType.PLAYER, "green", "Player"),
            (NodeType.PLAYER_ON_TARGET, "lightgreen", "Player on Target"),
            (NodeType.BOX_ON_TARGET, "yellow", "Box on Target"),
        ]

        for node_type, color, description in legend_items:
            frame = tk.Frame(legend_frame)
            frame.pack(anchor="w", pady=2)
            tk.Canvas(frame, width=20, height=20, bg=color).pack(side=tk.LEFT)
            tk.Label(frame, text=description).pack(side=tk.LEFT)

    def draw_map(self, nodes):
        if not self.canvas:
            return
        self.canvas.delete("all") # Clear the canvas
        for node in nodes:
            x1, y1 = node.x * 20, (self.max_rows - node.y - 1) * 20
            x2, y2 = x1 + 20, y1 + 20
            color = self.get_color(node.type)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if node.type == NodeType.BOX or node.type == NodeType.BOX_ON_TARGET:
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(node.cost), fill="black")

    def update_map(self, new_nodes):
        self.nodes = new_nodes
        if self.window and self.canvas:
            self.draw_map(self.nodes)
            self.window.update() # Force immediate update

    def animate_solution(self, problem, initial_state, solution_actions, delay=500):
        """
        Animate the solution with a delay between each step.

        Args:
            problem: The SokobanProblem instance.
            initial_state: The initial state of the problem.
            solution_actions: List of actions to perform.
            delay: Delay in milliseconds between steps (default: 500ms).
        """
        if self.animation_running or not self.window:
            return

        self.animation_running = True

        current_state = initial_state
        print("Initial State for Animation:", current_state) # Debugging
        self.update_map(problem.get_nodes_from_state(current_state))

        step_count = 0
        total_steps = len(solution_actions)

        def animate_step():
            nonlocal current_state, step_count

            if step_count < total_steps:
                action = solution_actions[step_count]
                print(f"Animating step {step_count + 1}: Action - {action}") # Debugging
                current_state = problem.result(current_state, action)
                print("New State:", current_state) # Debugging
                print("Updating map...") # Debugging
                self.update_map(problem.get_nodes_from_state(current_state))
                print("Map updated.") # Debugging

                step_count += 1
                self.window.after(delay, animate_step)
            else:
                self.animation_running = False
                messagebox.showinfo("Animation Complete", "The solution animation has finished!")

        # Start the animation
        if solution_actions: # Only start if there are actions
            self.window.after(delay, animate_step)
        else:
            self.animation_running = False
            messagebox.showinfo("Animation Info", "No solution actions to animate.")


class GameNode:
    def __init__(self, x, y, type, cost=1):
        self.x = x
        self.y = y
        self.type = type
        self.cost = cost

    def __eq__(self, other):
        return isinstance(other, GameNode) and self.x == other.x and self.y == other.y and self.type == other.type

    def __hash__(self):
        return hash((self.x, self.y, self.type))

    def __repr__(self):
        return f"({self.x}, {self.y}): {self.type.name}, Cost={self.cost}"

class NodeType(Enum):
    FREE = ' '
    WALL = '#'
    BOX = '$'
    TARGET = '.'
    PLAYER = '@'
    PLAYER_ON_TARGET = '!'
    BOX_ON_TARGET = '*'

def parse_map(file_path):
    """
    Parses a text file representing a 2D map into a list of GameNode objects.

    Args:
        file_path (str): The path to the text file.

    Returns:
        tuple: A tuple containing:
            - list[GameNode]: A list of GameNode objects representing the map.
            - int: The maximum number of columns in the map.
            - int: The maximum number of rows in the map.
    """
    nodes = []
    max_cols = 0
    max_rows = 0
    special_costs = {}
    player_pos = None
    box_positions = []
    target_positions = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

        # Parse the first line for special costs
        if lines:
            first_line = lines[0].strip().split()
            cost_values = [int(val) for val in first_line]
            special_costs = {'$': cost_values}  # Assuming '$' is the only special character with defined costs in the first line
            map_lines = [line.strip() for line in lines[1:]]
        else:
            map_lines = []

        # Invert the map (flip on the x-axis conceptually for easier parsing to bottom-left origin)
        inverted_map_lines = list(reversed(map_lines))

        box_counter = 0
        for y, row_str in enumerate(inverted_map_lines):
            max_rows = max(max_rows, y + 1)
            for x, char in enumerate(row_str):
                max_cols = max(max_cols, x + 1)
                node_type = None
                cost = 1

                if char == NodeType.FREE.value:
                    node_type = NodeType.FREE
                elif char == NodeType.WALL.value:
                    node_type = NodeType.WALL
                elif char == NodeType.BOX.value:
                    node_type = NodeType.BOX
                    if '$' in special_costs and box_counter < len(special_costs['$']):
                        cost = special_costs['$'][box_counter]
                    box_counter += 1
                    box_positions.append((x, y))
                elif char == NodeType.TARGET.value:
                    node_type = NodeType.TARGET
                    target_positions.append((x, y))
                elif char == NodeType.PLAYER.value:
                    node_type = NodeType.PLAYER
                    player_pos = (x, y)
                elif char == NodeType.PLAYER_ON_TARGET.value:
                    node_type = NodeType.PLAYER_ON_TARGET
                    player_pos = (x, y)
                    target_positions.append((x, y)) # Treat as target as well for goal test
                elif char == NodeType.BOX_ON_TARGET.value:
                    node_type = NodeType.BOX_ON_TARGET
                    if '$' in special_costs and box_counter < len(special_costs['$']):
                        cost = special_costs['$'][box_counter]
                    box_counter += 1
                    box_positions.append((x, y))
                    target_positions.append((x, y)) # Treat as target as well for goal test
                else:
                    # Handle unknown characters if necessary
                    continue

                if node_type:
                    nodes.append(GameNode(x, y, node_type, cost))

    return nodes, max_cols, max_rows, player_pos, tuple(sorted(box_positions)), tuple(sorted(target_positions))

class SokobanProblem(Problem):
    def __init__(self, initial_state, goal_state, max_cols, max_rows, initial_nodes):
        super().__init__(initial_state, goal_state)
        self.max_cols = max_cols
        self.max_rows = max_rows
        self.initial_nodes = initial_nodes
        self.walls = set([(node.x, node.y) for node in initial_nodes if node.type == NodeType.WALL])
        self.targets = set(goal_state)

    def get_nodes_from_state(self, state):
        player_pos, box_positions = state
        nodes = []
        for node in self.initial_nodes:
            if node.type == NodeType.WALL:
                nodes.append(GameNode(node.x, node.y, node.type))
            elif node.type == NodeType.TARGET:
                if (node.x, node.y) in box_positions:
                    nodes.append(GameNode(node.x, node.y, NodeType.BOX_ON_TARGET))
                else:
                    nodes.append(GameNode(node.x, node.y, node.type))
            elif (node.x, node.y) == player_pos:
                if (node.x, node.y) in self.targets:
                    nodes.append(GameNode(node.x, node.y, NodeType.PLAYER_ON_TARGET))
                else:
                    nodes.append(GameNode(node.x, node.y, NodeType.PLAYER))
            elif (node.x, node.y) in box_positions:
                original_cost_node = next((n for n in self.initial_nodes if n.x == node.x and n.y == node.y and n.type == NodeType.BOX), None)
                cost = original_cost_node.cost if original_cost_node else 1
                if (node.x, node.y) in self.targets:
                    nodes.append(GameNode(node.x, node.y, NodeType.BOX_ON_TARGET, cost))
                else:
                    nodes.append(GameNode(node.x, node.y, NodeType.BOX, cost))
            elif node.type == NodeType.FREE:
                nodes.append(GameNode(node.x, node.y, node.type))
        return nodes

    def actions(self, state):
        player_pos, box_positions = state
        possible_actions = []
        moves = [(0, 1, 'up'), (0, -1, 'down'), (1, 0, 'right'), (-1, 0, 'left')]

        for dx, dy, action in moves:
            new_player_x, new_player_y = player_pos[0] + dx, player_pos[1] + dy

            if (new_player_x, new_player_y) not in self.walls:
                # Check for a box push
                if (new_player_x, new_player_y) in box_positions:
                    new_box_x, new_box_y = new_player_x + dx, new_player_y + dy
                    if (new_box_x, new_box_y) not in self.walls and (new_box_x, new_box_y) not in box_positions:
                        possible_actions.append(action)
                else:
                    possible_actions.append(action)

        return possible_actions

    def result(self, state, action):
        player_pos, box_positions = state
        player_x, player_y = player_pos
        new_player_x, new_player_y = player_x, player_y
        new_box_positions = list(box_positions)

        if action == 'up':
            new_player_y += 1
            dx, dy = 0, 1
        elif action == 'down':
            new_player_y -= 1
            dx, dy = 0, -1
        elif action == 'right':
            new_player_x += 1
            dx, dy = 1, 0
        elif action == 'left':
            new_player_x -= 1
            dx, dy = -1, 0
        else:
            raise ValueError(f"Invalid action: {action}")

        new_player_pos = (new_player_x, new_player_y)

        # Check if a box was pushed
        if new_player_pos in box_positions:
            box_index = box_positions.index(new_player_pos)
            new_box_x = new_player_x + dx
            new_box_y = new_player_y + dy
            new_box_positions[box_index] = (new_box_x, new_box_y)

        return (new_player_pos, tuple(sorted(new_box_positions)))

    def goal_test(self, state):
        _, box_positions = state
        return set(box_positions) == self.targets
    def path_cost(self, cost_so_far, state1, action, state2):
        # Cost of moving a box is the cost associated with that box type in the map
        _, box_positions1 = state1
        _, box_positions2 = state2

        if len(box_positions2) > len(box_positions1):
            raise ValueError("More boxes in the next state than the current state")

        if box_positions1 != box_positions2: # A box was moved
            moved_box = None
            for box1 in box_positions1:
                if box1 not in box_positions2:
                    moved_box = box1
                    break
            if moved_box is None:
                for box2 in box_positions2:
                    if box2 not in box_positions1:
                        moved_box = box2
                        break
            if moved_box:
                original_box_node = next((n for n in self.initial_nodes if n.x == moved_box[0] and n.y == moved_box[1] and n.type in [NodeType.BOX, NodeType.BOX_ON_TARGET]), None)
                if original_box_node:
                    return cost_so_far + original_box_node.cost
                else:
                    return cost_so_far + 1 # Default cost if box info not found
        return cost_so_far + 1 # Cost of player movement
    def h(self, node_or_state):
        # Manhattan distance heuristic: sum of distances of each box to the nearest target
        # Handle both Node objects and state tuples
        if hasattr(node_or_state, 'state'):
            state = node_or_state.state
        else:
            state = node_or_state

        _, box_positions = state
        total_heuristic = 0
        for box_x, box_y in box_positions:
            min_distance = float('inf')
            for target_x, target_y in self.targets:
                distance = abs(box_x - target_x) + abs(box_y - target_y)
                min_distance = min(min_distance, distance)
            total_heuristic += min_distance
        return total_heuristic

if __name__ == "__main__":
    # Example usage with the provided input file content:

    # Parse the map file
    file_path = "/home/hecke/Github/sem1-2025files/cab320/Assignments/CAB320 Se125 Assigment 1-1/warehouses/warehouse_01_a.txt"
    nodes, max_cols, max_rows, player_pos, initial_box_positions, target_positions = parse_map(file_path)

    # Print map information
    print(f"Maximum Columns: {max_cols}")
    print(f"Maximum Rows: {max_rows}")
    print(f"Initial Player Position: {player_pos}")
    print(f"Initial Box Positions: {initial_box_positions}")
    print(f"Target Positions: {target_positions}")

    initial_state = (player_pos, initial_box_positions)
    goal_state = target_positions

    problem = SokobanProblem(initial_state, goal_state, max_cols, max_rows, nodes)

    # Solve the problem
    print("\nSolving the problem using A* search...")
    solution_node = astar_graph_search(problem, problem.h)

    if solution_node:
        solution_actions = solution_node.solution()
        print(f"\nSolution found! ({len(solution_actions)} steps)")

        # Print the list of steps
        print("Steps to solve:")
        for i, action in enumerate(solution_actions, start=1):
            print(f"Step {i}: {action}")

        # Create viewer and store problem and solution for animation
        viewer = MapViewer(nodes, max_cols, max_rows)
        viewer.problem = problem
        viewer.initial_state = initial_state
        viewer.solution_actions = solution_actions
        viewer.animation_delay = 1000 # Adjust delay if needed
        viewer.show()

    else:
        print("\nNo solution found.")