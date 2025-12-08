import time
import sys
from typing import Dict, List, Tuple
from helper_01 import HashiwokakeroGame

sys.setrecursionlimit(10000)

class BacktrackingSolver:
    """
    Optimized Backtracking with:
    - Forward Checking
    - MRV (Most Constrained Variable)
    - LCV (Least Constraining Value)
    - Early Pruning
    - Early UNSAT Detection
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.islands_map = {(r,c): v for r,c,v in game.islands}
        self.neighbors_map = {(r,c): game.get_neighbors(r,c) for r,c,v in game.islands}
        self.nodes_explored = 0
        self.unsat_detected = False
        
        self.connections = []
        seen = set()
        for (r,c), neighbors in self.neighbors_map.items():
            for nr, nc in neighbors:
                key = self._normalize_key(r, c, nr, nc)
                if key not in seen:
                    self.connections.append(key)
                    seen.add(key)

    def solve(self) -> Tuple[Dict, float]:
        print("Solving with Backtracking...")
        start = time.perf_counter()
        
        solution = {}
        result = self._backtrack(solution, 0)
        
        elapsed = time.perf_counter() - start
        if result:
            print(f"✓ Solution found! Nodes: {self.nodes_explored:,}")
            return result, elapsed
        else:
            if self.unsat_detected:
                print(f"✗ No solution (UNSAT detected). Nodes: {self.nodes_explored:,}")
            else:
                print(f"✗ No solution. Nodes: {self.nodes_explored:,}")
            return None, elapsed

    def _backtrack(self, solution: Dict, depth: int) -> Dict:
        self.nodes_explored += 1
        
        # ✅ Early UNSAT Detection
        if self.nodes_explored % 5000 == 0:
            if self._detect_unsat_early(solution):
                if not self.unsat_detected:
                    print(f"  🔍 Detected UNSAT early at {self.nodes_explored:,} nodes")
                    self.unsat_detected = True
                return None
        
        # Progress
        if self.nodes_explored % 10000 == 0:
            print(f"  Nodes: {self.nodes_explored:,}, Depth: {depth}")
        
        # Limit
        if self.nodes_explored > 500000:
            return None
        
        # Forward checking
        if not self._is_consistent(solution):
            return None
        
        # Goal check - complete AND connected
        if self._is_complete(solution):
            if self._is_connected(solution):
                return solution
            else:
                return None
        
        # Select MRV island
        island = self._select_mrv_island(solution)
        if not island:
            return None
        
        r, c = island
        needed = self.islands_map[(r,c)] - self._current_bridges(r, c, solution)
        
        if needed <= 0:
            return self._backtrack(solution, depth + 1)
        
        # Order neighbors by LCV
        neighbors = self._order_neighbors_lcv(r, c, solution)
        
        # Try connecting to each neighbor
        for nr, nc in neighbors:
            key = self._normalize_key(r, c, nr, nc)
            curr_bridges = solution.get(key, 0)
            
            # Skip if crossing
            if curr_bridges == 0 and self._would_cross(key, solution):
                continue
            
            # Skip if max
            if curr_bridges >= 2:
                continue
            
            # Check neighbor capacity
            neighbor_needed = self.islands_map[(nr,nc)] - self._current_bridges(nr, nc, solution)
            if neighbor_needed <= 0:
                continue
            
            # Try 2 bridges first, then 1
            for num_bridges in [2, 1]:
                if curr_bridges + num_bridges > 2:
                    continue
                
                if num_bridges > min(needed, neighbor_needed):
                    continue
                
                # Add bridges
                old_value = curr_bridges
                solution[key] = curr_bridges + num_bridges
                
                # Recursive call
                result = self._backtrack(solution, depth + 1)
                if result:
                    return result
                
                # Backtrack
                if old_value == 0:
                    del solution[key]
                else:
                    solution[key] = old_value
        
        return None

    def _is_complete(self, solution):
        """Check if all islands have required bridges"""
        for (r,c), val in self.islands_map.items():
            if self._current_bridges(r, c, solution) != val:
                return False
        return True

    def _select_mrv_island(self, solution):
        """Select most constrained island"""
        best = None
        best_score = -1
        
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, solution)
            remaining = val - curr
            
            if remaining <= 0:
                continue
            
            available = 0
            for nr, nc in self.neighbors_map[(r,c)]:
                key = self._normalize_key(r, c, nr, nc)
                curr_b = solution.get(key, 0)
                
                if curr_b < 2:
                    neighbor_curr = self._current_bridges(nr, nc, solution)
                    neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
                    
                    if neighbor_remaining > 0:
                        if curr_b == 0 and not self._would_cross(key, solution):
                            available += 1
                        elif curr_b > 0:
                            available += 1
            
            if available > 0:
                score = remaining / available
                if score > best_score:
                    best_score = score
                    best = (r, c)
        
        return best

    def _order_neighbors_lcv(self, r, c, solution):
        """Order neighbors by LCV"""
        neighbors = self.neighbors_map[(r,c)]
        scores = []
        
        for nr, nc in neighbors:
            key = self._normalize_key(r, c, nr, nc)
            curr_b = solution.get(key, 0)
            
            if curr_b >= 2:
                continue
            
            neighbor_curr = self._current_bridges(nr, nc, solution)
            neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
            
            if neighbor_remaining <= 0:
                continue
            
            scores.append((neighbor_remaining, nr, nc))
        
        scores.sort(reverse=True)
        return [(nr, nc) for _, nr, nc in scores]

    def _is_consistent(self, solution):
        """Forward checking"""
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, solution)
            if curr > val:
                return False
            
            remaining = val - curr
            if remaining > 0:
                max_possible = 0
                for nr, nc in self.neighbors_map[(r,c)]:
                    key = self._normalize_key(r, c, nr, nc)
                    curr_b = solution.get(key, 0)
                    can_add = 2 - curr_b
                    
                    neighbor_curr = self._current_bridges(nr, nc, solution)
                    neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
                    
                    max_possible += min(can_add, neighbor_remaining)
                
                if max_possible < remaining:
                    return False
        return True

    def _detect_unsat_early(self, solution):
        """Early UNSAT detection"""
        # Check 1: Impossible capacity
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, solution)
            remaining = val - curr
            
            if remaining > 0:
                max_possible = 0
                for nr, nc in self.neighbors_map[(r,c)]:
                    key = self._normalize_key(r, c, nr, nc)
                    curr_b = solution.get(key, 0)
                    can_add = 2 - curr_b
                    
                    neighbor_curr = self._current_bridges(nr, nc, solution)
                    neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
                    
                    max_possible += min(can_add, neighbor_remaining)
                
                if max_possible < remaining:
                    return True
        
        # Check 2: Too many isolated islands
        unconnected = self._count_unconnected_islands(solution)
        if unconnected > len(self.islands_map) * 0.7:
            possible_new = 0
            for (r,c) in self.islands_map.keys():
                curr = self._current_bridges(r, c, solution)
                if curr == 0:
                    for nr, nc in self.neighbors_map[(r,c)]:
                        key = self._normalize_key(r, c, nr, nc)
                        if key not in solution:
                            if not self._would_cross(key, solution):
                                possible_new += 1
                                break
            
            if possible_new < unconnected * 0.5:
                return True
        
        return False

    def _count_unconnected_islands(self, solution):
        """Count islands with no bridges"""
        count = 0
        for (r,c) in self.islands_map.keys():
            if self._current_bridges(r, c, solution) == 0:
                count += 1
        return count

    def _current_bridges(self, r, c, solution):
        count = 0
        for (r1,c1,r2,c2), k in solution.items():
            if (r1==r and c1==c) or (r2==r and c2==c):
                count += k
        return count

    def _would_cross(self, new_key, solution):
        r1a, c1a, r2a, c2a = new_key
        is_h1 = (r1a == r2a)
        
        for (r1b, c1b, r2b, c2b) in solution.keys():
            is_h2 = (r1b == r2b)
            
            if is_h1 == is_h2:
                continue
            
            if is_h1:
                if (min(c1a, c2a) < c1b < max(c1a, c2a) and
                    min(r1b, r2b) < r1a < max(r1b, r2b)):
                    return True
            else:
                if (min(c1b, c2b) < c1a < max(c1b, c2b) and
                    min(r1a, r2a) < r1b < max(r1a, r2a)):
                    return True
        return False

    def _is_connected(self, solution):
        """Check connectivity via DFS"""
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

    def _normalize_key(self, r1, c1, r2, c2):
        if (r1, c1) > (r2, c2):
            return (r2, c2, r1, c1)
        return (r1, c1, r2, c2)