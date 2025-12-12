import numpy as np
from typing import List, Tuple, Set

BRIDGE_SYMBOLS = {
    'h1': '-',
    'h2': '=',
    'v1': '|',
    'v2': '$',
    'empty': '0'
}

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class HashiwokakeroGame:
    def __init__(self, filename=None, grid=None):
        if filename:
            self.grid = self.read_input(filename)
        elif grid is not None:
            self.grid = np.array(grid)
        else:
            raise ValueError("Cần cung cấp filename hoặc grid")
        
        self.rows, self.cols = self.grid.shape
        self.islands = self.find_islands()
        self.bridges = {}
        
    def read_input(self, filename: str) -> np.ndarray:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        grid = []
        for line in lines:
            line = line.strip()
            if line:
                row = [int(x.strip()) for x in line.split(',')]
                grid.append(row)
        
        return np.array(grid)
    
    def find_islands(self) -> List[Tuple[int, int, int]]:
        islands = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] > 0:
                    islands.append((i, j, self.grid[i][j]))
        return islands
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors = []
        
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            
            while 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] > 0:
                    neighbors.append((r, c))
                    break
                r += dr
                c += dc
        
        return neighbors
    
    def is_valid_bridge(self, i1: int, j1: int, i2: int, j2: int, 
                       current_state: dict) -> bool:
        for (r1, c1, r2, c2), _ in current_state.items():
            if self._bridges_cross((i1, j1, i2, j2), (r1, c1, r2, c2)):
                return False
        return True
    
    def _bridges_cross(self, bridge1: tuple, bridge2: tuple) -> bool:
        i1a, j1a, i2a, j2a = bridge1
        i1b, j1b, i2b, j2b = bridge2
        
        if i1a == i2a and j1b == j2b:
            if (min(j1a, j2a) < j1b < max(j1a, j2a) and
                min(i1b, i2b) < i1a < max(i1b, i2b)):
                return True
                
        elif j1a == j2a and i1b == i2b:
            if (min(i1a, i2a) < i1b < max(i1a, i2a) and
                min(j1b, j2b) < j1a < max(j1b, j2b)):
                return True
        
        return False
    
    def display(self, solution=None):
        if solution is None:
            print("Grid:")
            print(self.grid)
        else:
            self.display_solution(solution)
    
    def display_solution(self, solution: dict) -> List[List[str]]:
        result = [[BRIDGE_SYMBOLS['empty'] for _ in range(self.cols)] 
                  for _ in range(self.rows)]
        
        for i, j, val in self.islands:
            result[i][j] = str(val)
        
        for key, num_bridges in solution.items():
            i1, j1, i2, j2 = key
            
            if i1 == i2:
                start_col = min(j1, j2) + 1
                end_col = max(j1, j2)
                for c in range(start_col, end_col):
                    result[i1][c] = BRIDGE_SYMBOLS['h1'] if num_bridges == 1 else BRIDGE_SYMBOLS['h2']
                        
            else:
                start_row = min(i1, i2) + 1
                end_row = max(i1, i2)
                for r in range(start_row, end_row):
                    result[r][j1] = BRIDGE_SYMBOLS['v1'] if num_bridges == 1 else BRIDGE_SYMBOLS['v2']
        
        for row in result:
            print(row)
        
        return result
    
    def save_solution(self, solution: dict, filename: str):
        result = [[BRIDGE_SYMBOLS['empty'] for _ in range(self.cols)] 
                  for _ in range(self.rows)]
        
        for i, j, val in self.islands:
            result[i][j] = str(val)
        
        for key, num_bridges in solution.items():
            i1, j1, i2, j2 = key
            
            if i1 == i2:
                start_col = min(j1, j2) + 1
                end_col = max(j1, j2)
                for c in range(start_col, end_col):
                    result[i1][c] = BRIDGE_SYMBOLS['h2'] if num_bridges == 2 else BRIDGE_SYMBOLS['h1']
                    
            else:
                start_row = min(i1, i2) + 1
                end_row = max(i1, i2)
                for r in range(start_row, end_row):
                    result[r][j1] = BRIDGE_SYMBOLS['v2'] if num_bridges == 2 else BRIDGE_SYMBOLS['v1']
        
        with open(filename, 'w') as f:
            for row in result:
                f.write('[' + ', '.join(f'"{x}"' for x in row) + ']\n')
 
    def validate_solution(self, solution: dict) -> Tuple[bool, List[str]]:
        """
        Validates the solution against game rules.
        """
        errors = []
        
        # Check 1: Bridge count per island
        bridges_count = {}
        for island in self.islands:
            bridges_count[(island[0], island[1])] = 0
        
        for (i1, j1, i2, j2), num_bridges in solution.items():
            bridges_count[(i1, j1)] = bridges_count.get((i1, j1), 0) + num_bridges
            bridges_count[(i2, j2)] = bridges_count.get((i2, j2), 0) + num_bridges
        
        for i, j, required in self.islands:
            actual = bridges_count.get((i, j), 0)
            if actual != required:
                errors.append(f"Island ({i},{j}): needs {required} bridges, has {actual}")
        
        # Check 2: Crossing bridges
        bridges_list = list(solution.keys())
        for idx1 in range(len(bridges_list)):
            for idx2 in range(idx1 + 1, len(bridges_list)):
                if self._bridges_cross(bridges_list[idx1], bridges_list[idx2]):
                    errors.append(f"Bridge {bridges_list[idx1]} crosses {bridges_list[idx2]}")

        # Check 3: Connectivity
        # The bridges must connect the islands into a single connected group
        if not self._is_connected(solution):
             errors.append("Islands are not fully connected (Graph is disconnected)")
        return len(errors) == 0, errors

    def _is_connected(self, solution: dict) -> bool:
        if not self.islands:
            return True
            
        # Build adjacency list
        adj = {(r, c): [] for r, c, _ in self.islands}
        for (r1, c1, r2, c2), count in solution.items():
            if count > 0:
                adj[(r1, c1)].append((r2, c2))
                adj[(r2, c2)].append((r1, c1))
        
        # BFS
        start_node = (self.islands[0][0], self.islands[0][1])
        queue = [start_node]
        visited = {start_node}
        
        while queue:
            u = queue.pop(0)
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return len(visited) == len(self.islands)
    
    def __str__(self):
        return f"Hashiwokakero({self.rows}x{self.cols}, {len(self.islands)} islands)"
