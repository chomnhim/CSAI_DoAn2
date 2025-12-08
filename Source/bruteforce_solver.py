"""
BRUTE FORCE SOLVER - SỬA LẠI ĐÚNG ĐỀ BÀI
Giải trực tiếp puzzle (KHÔNG dùng CNF)
Thử tất cả cách đặt cầu có thể
"""

import time
from itertools import product
from typing import Dict, List, Tuple, Set
from helper_01 import HashiwokakeroGame


class BruteForceSolver:
    """
    Brute Force: Thử TẤT CẢ các cách đặt cầu có thể
    Chỉ dùng cho puzzle nhỏ (≤8 đảo)
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.nodes_explored = 0
        
        # Tạo danh sách TẤT CẢ kết nối có thể
        self.all_possible_connections = []
        for r, c, _ in game.islands:
            neighbors = game.get_neighbors(r, c)
            for nr, nc in neighbors:
                if (r, c) < (nr, nc):  # Tránh trùng lặp
                    self.all_possible_connections.append((r, c, nr, nc))
        
        self.num_connections = len(self.all_possible_connections)
        
        # Tính số combinations (mỗi kết nối có 3 khả năng: 0, 1, 2 cầu)
        self.total_combinations = 3 ** self.num_connections
        
        print(f"Brute Force Setup:")
        print(f"  - Số kết nối có thể: {self.num_connections}")
        print(f"  - Tổng combinations: {self.total_combinations:,}")
        
        if self.total_combinations > 10_000_000:
            print(f"  ⚠️  CẢNH BÁO: Quá nhiều combinations!")
            print(f"  ⚠️  Thời gian ước tính: rất lâu...")
    
    def solve(self) -> Tuple[Dict, float]:
        """
        Giải puzzle bằng Brute Force
        
        Returns:
            (solution, time_taken)
        """
        print("\nSolving with Brute Force...")
        start = time.perf_counter()
        
        # Thử TẤT CẢ các combinations
        # Mỗi connection có 3 giá trị: 0, 1, 2 cầu
        for combination in product([0, 1, 2], repeat=self.num_connections):
            self.nodes_explored += 1
            
            # Tạo solution từ combination
            solution = {}
            for idx, num_bridges in enumerate(combination):
                if num_bridges > 0:
                    conn = self.all_possible_connections[idx]
                    solution[conn] = num_bridges
            
            # Kiểm tra solution có hợp lệ không
            if self._is_valid_solution(solution):
                elapsed = time.perf_counter() - start
                print(f"✓ Found solution!")
                print(f"  - Combinations tried: {self.nodes_explored:,}")
                print(f"  - Percentage: {self.nodes_explored/self.total_combinations*100:.4f}%")
                return solution, elapsed
            
            # Progress report
            if self.nodes_explored % 100_000 == 0:
                elapsed = time.perf_counter() - start
                pct = self.nodes_explored / self.total_combinations * 100
                print(f"  Progress: {self.nodes_explored:,}/{self.total_combinations:,} ({pct:.2f}%) - {elapsed:.1f}s")
            
            # Safety limit (tránh chạy quá lâu)
            if self.nodes_explored > 50_000_000:
                print("  ⚠️  Exceeded safety limit, stopping...")
                break
        
        elapsed = time.perf_counter() - start
        print(f"✗ No solution found")
        print(f"  - Tried {self.nodes_explored:,} combinations")
        return None, elapsed
    
    def _is_valid_solution(self, solution: Dict) -> bool:
        """
        Kiểm tra solution có hợp lệ không
        
        Checks:
        1. Mỗi đảo có đúng số cầu
        2. Không có cầu cắt nhau
        3. Tất cả đảo connected (1 connected component)
        """
        # Check 1: Số cầu mỗi đảo
        bridges_count = {}
        for r, c, val in self.game.islands:
            bridges_count[(r, c)] = 0
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            bridges_count[(r1, c1)] = bridges_count.get((r1, c1), 0) + num_bridges
            bridges_count[(r2, c2)] = bridges_count.get((r2, c2), 0) + num_bridges
        
        for r, c, required in self.game.islands:
            if bridges_count.get((r, c), 0) != required:
                return False
        
        # Check 2: Không có cầu cắt nhau
        bridges_list = list(solution.keys())
        for i in range(len(bridges_list)):
            for j in range(i + 1, len(bridges_list)):
                if self._bridges_cross(bridges_list[i], bridges_list[j]):
                    return False
        
        # Check 3: Connectivity (dùng DFS/BFS)
        if not self._is_connected(solution):
            return False
        
        return True
    
    def _bridges_cross(self, bridge1: tuple, bridge2: tuple) -> bool:
        """Kiểm tra 2 cầu có cắt nhau không"""
        r1a, c1a, r2a, c2a = bridge1
        r1b, c1b, r2b, c2b = bridge2
        
        # Ngang vs Dọc
        is_h1 = (r1a == r2a)
        is_h2 = (r1b == r2b)
        
        if is_h1 == is_h2:
            return False
        
        if is_h1:  # Bridge1 ngang, Bridge2 dọc
            return (min(c1a, c2a) < c1b < max(c1a, c2a) and
                    min(r1b, r2b) < r1a < max(r1b, r2b))
        else:  # Bridge1 dọc, Bridge2 ngang
            return (min(c1b, c2b) < c1a < max(c1b, c2b) and
                    min(r1a, r2a) < r1b < max(r1a, r2a))
    
    def _is_connected(self, solution: Dict) -> bool:
        """
        Kiểm tra tất cả đảo có connected không (DFS)
        """
        if not self.game.islands:
            return True
        
        # Build adjacency list
        graph = {(r, c): [] for r, c, _ in self.game.islands}
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            if num_bridges > 0:
                graph[(r1, c1)].append((r2, c2))
                graph[(r2, c2)].append((r1, c1))
        
        # DFS từ đảo đầu tiên
        start = (self.game.islands[0][0], self.game.islands[0][1])
        visited = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
        
        # Tất cả đảo phải được visit
        return len(visited) == len(self.game.islands)


class OptimizedBruteForceSolver:
    """
    Brute Force với Early Pruning
    Dừng sớm khi phát hiện vi phạm constraint
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.nodes_explored = 0
        
        # Tạo danh sách connections
        self.connections = []
        for r, c, _ in game.islands:
            neighbors = game.get_neighbors(r, c)
            for nr, nc in neighbors:
                if (r, c) < (nr, nc):
                    self.connections.append((r, c, nr, nc))
    
    def solve(self) -> Tuple[Dict, float]:
        """Giải với recursive + pruning"""
        print("\nSolving with Optimized Brute Force...")
        start = time.perf_counter()
        
        solution = {}
        result = self._backtrack_with_pruning(0, solution)
        
        elapsed = time.perf_counter() - start
        if result:
            print(f"✓ Found solution!")
            print(f"  - Nodes explored: {self.nodes_explored:,}")
            return result, elapsed
        else:
            print(f"✗ No solution")
            print(f"  - Nodes explored: {self.nodes_explored:,}")
            return None, elapsed
    
    def _backtrack_with_pruning(self, idx: int, solution: Dict) -> Dict:
        """Recursive backtracking với early pruning"""
        self.nodes_explored += 1
        
        # Limit
        if self.nodes_explored > 10_000_000:
            return None
        
        # Early pruning: Kiểm tra có đảo nào bị quá tải không
        if not self._is_valid_partial(solution):
            return None
        
        # Base case: Đã thử hết connections
        if idx == len(self.connections):
            if self._is_complete_solution(solution):
                return solution
            return None
        
        # Recursive: Thử 0, 1, 2 cầu
        conn = self.connections[idx]
        
        # Kiểm tra crossing trước khi thử
        if self._would_cross(conn, solution):
            # Nếu cross, chỉ có thể skip (0 cầu)
            return self._backtrack_with_pruning(idx + 1, solution)
        
        # Try 0 cầu (skip)
        result = self._backtrack_with_pruning(idx + 1, solution)
        if result:
            return result
        
        # Try 1 cầu
        solution[conn] = 1
        result = self._backtrack_with_pruning(idx + 1, solution)
        if result:
            return result
        del solution[conn]
        
        # Try 2 cầu
        solution[conn] = 2
        result = self._backtrack_with_pruning(idx + 1, solution)
        if result:
            return result
        del solution[conn]
        
        return None
    
    def _is_valid_partial(self, solution: Dict) -> bool:
        """Kiểm tra có đảo nào bị quá tải không"""
        bridges_count = {}
        for r, c, val in self.game.islands:
            bridges_count[(r, c)] = 0
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            bridges_count[(r1, c1)] += num_bridges
            bridges_count[(r2, c2)] += num_bridges
        
        for r, c, required in self.game.islands:
            if bridges_count.get((r, c), 0) > required:
                return False
        
        return True
    
    def _is_complete_solution(self, solution: Dict) -> bool:
        """Kiểm tra solution đầy đủ"""
        # Check số cầu
        bridges_count = {}
        for r, c, val in self.game.islands:
            bridges_count[(r, c)] = 0
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            bridges_count[(r1, c1)] += num_bridges
            bridges_count[(r2, c2)] += num_bridges
        
        for r, c, required in self.game.islands:
            if bridges_count.get((r, c), 0) != required:
                return False
        
        # Check connectivity
        return self._is_connected(solution)
    
    def _would_cross(self, new_conn: tuple, solution: Dict) -> bool:
        """Kiểm tra connection mới có cross với cầu đã có không"""
        r1a, c1a, r2a, c2a = new_conn
        is_h1 = (r1a == r2a)
        
        for (r1b, c1b, r2b, c2b) in solution.keys():
            is_h2 = (r1b == r2b)
            
            if is_h1 == is_h2:
                continue
            
            if is_h1:  # New ngang, old dọc
                if (min(c1a, c2a) < c1b < max(c1a, c2a) and
                    min(r1b, r2b) < r1a < max(r1b, r2b)):
                    return True
            else:  # New dọc, old ngang
                if (min(c1b, c2b) < c1a < max(c1b, c2b) and
                    min(r1a, r2a) < r1b < max(r1a, r2a)):
                    return True
        
        return False
    
    def _is_connected(self, solution: Dict) -> bool:
        """Check connectivity"""
        if not self.game.islands:
            return True
        
        graph = {(r, c): [] for r, c, _ in self.game.islands}
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            if num_bridges > 0:
                graph[(r1, c1)].append((r2, c2))
                graph[(r2, c2)].append((r1, c1))
        
        start = (self.game.islands[0][0], self.game.islands[0][1])
        visited = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return len(visited) == len(self.game.islands)