import heapq
import time
import math
from typing import Dict, List, Tuple
from helper_01 import HashiwokakeroGame

class AStarNode:
    def __init__(self, state: Dict, g: float, h: float):
        self.state = state 
        self.g = g
        self.h = h
        self.f = g + h
    
    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        return self.h < other.h

class AStarSolver:
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.islands_map = {(r,c): v for r,c,v in game.islands}
        self.neighbors_map = {pos: game.get_neighbors(*pos) for pos in self.islands_map}
        self.nodes_explored = 0

    def solve(self):
        print("Solving with A*...")
        start = time.perf_counter()
        
        initial = AStarNode({}, 0, self._heuristic({}))
        pq = [initial]
        visited = set()
        
        while pq:
            node = heapq.heappop(pq)
            self.nodes_explored += 1
            
            if self.nodes_explored % 5000 == 0:
                if self._detect_unsat_early(node.state):
                    elapsed = time.perf_counter() - start
                    print(f"   Detected UNSAT early at {self.nodes_explored:,} nodes")
                    print(f" No solution (UNSAT detected). Nodes: {self.nodes_explored:,}")
                    return None, elapsed
            
            # Progress
            if self.nodes_explored % 10000 == 0:
                print(f"  Nodes: {self.nodes_explored:,}, f={node.f:.1f}")
            
            # Limit
            if self.nodes_explored > 200000:
                break
            
            # Check complete FIRST, then connectivity
            if self._is_complete(node.state):
                if self._is_connected(node.state):
                    elapsed = time.perf_counter() - start
                    print(f"✓ Solution found! Nodes: {self.nodes_explored:,}")
                    return node.state, elapsed
                # Complete but not connected - skip
                continue
            
            # Visited check
            state_key = tuple(sorted(node.state.items()))
            if state_key in visited:
                continue
            visited.add(state_key)
            
            # Early pruning
            if not self._is_valid_partial(node.state):
                continue
            
            # Select island (MRV)
            target = self._select_island(node.state)
            if not target:
                continue
            
            r, c = target
            
            # Try connecting to neighbors
            for nr, nc in self.neighbors_map[(r,c)]:
                key = tuple(sorted(((r,c), (nr,nc))))
                flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                
                curr_b = node.state.get(flat_key, 0)
                
                if curr_b >= 2:
                    continue
                
                n_needed = self.islands_map[(nr,nc)] - self._current_bridges(nr, nc, node.state)
                if n_needed <= 0:
                    continue
                
                if curr_b == 0 and self._is_crossing(flat_key, node.state):
                    continue
                
                new_state = node.state.copy()
                new_state[flat_key] = curr_b + 1
                
                h = self._heuristic(new_state)
                if h < float('inf'):
                    heapq.heappush(pq, AStarNode(new_state, node.g + 1, h))
        
        elapsed = time.perf_counter() - start
        print(f" No solution. Nodes: {self.nodes_explored:,}")
        return None, elapsed

    def _is_complete(self, state):
        for (r,c), val in self.islands_map.items():
            if self._current_bridges(r, c, state) != val:
                return False
        return True

    def _is_valid_partial(self, state):
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, state)
            if curr > val:
                return False
            
            needed = val - curr
            if needed > 0:
                max_possible = 0
                for nr, nc in self.neighbors_map[(r,c)]:
                    key = tuple(sorted(((r,c), (nr,nc))))
                    flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                    curr_b = state.get(flat_key, 0)
                    can_add = 2 - curr_b
                    
                    neighbor_curr = self._current_bridges(nr, nc, state)
                    neighbor_can = self.islands_map[(nr,nc)] - neighbor_curr
                    
                    max_possible += min(can_add, neighbor_can)
                
                if max_possible < needed:
                    return False
        return True

    def _select_island(self, state):
        best = None
        best_score = -1
        
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, state)
            needed = val - curr
            
            if needed <= 0:
                continue
            
            available = 0
            for nr, nc in self.neighbors_map[(r,c)]:
                key = tuple(sorted(((r,c), (nr,nc))))
                flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                curr_b = state.get(flat_key, 0)
                
                if curr_b < 2:
                    n_needed = self.islands_map[(nr,nc)] - self._current_bridges(nr, nc, state)
                    if n_needed > 0:
                        if curr_b == 0:
                            if not self._is_crossing(flat_key, state):
                                available += 1
                        else:
                            available += 1
            
            if available > 0:
                score = needed / available
                if score > best_score:
                    best_score = score
                    best = (r,c)
        
        return best

    def _current_bridges(self, r, c, state):
        count = 0
        for (r1,c1,r2,c2), k in state.items():
            if (r1==r and c1==c) or (r2==r and c2==c):
                count += k
        return count

    def _heuristic(self, state):
        total_deficit = 0
        isolated_count = 0
        
        # Phase 1: Basic deficit
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, state)
            deficit = val - curr
            
            if curr > val:
                return float('inf')
            
            total_deficit += deficit
            
            if curr == 0 and deficit > 0:
                isolated_count += 1
        
        h = math.ceil(total_deficit / 2)
        
        # Phase 2: Component analysis
        if len(state) > 0:
            num_components = self._count_components(state)
            if num_components > 1:
                h += (num_components - 1) * 2
        
        # Phase 3: Isolated penalty
        if isolated_count > 1:
            h += isolated_count - 1
        
        # Phase 4: Hard islands
        hard_islands = 0
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, state)
            remaining = val - curr
            
            if remaining > 0:
                available = 0
                for nr, nc in self.neighbors_map[(r,c)]:
                    key = tuple(sorted(((r,c), (nr,nc))))
                    flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                    curr_b = state.get(flat_key, 0)
                    
                    if curr_b < 2:
                        neighbor_curr = self._current_bridges(nr, nc, state)
                        neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
                        
                        if neighbor_remaining > 0:
                            if curr_b == 0:
                                if not self._is_crossing(flat_key, state):
                                    available += 1
                            else:
                                available += 1
                
                if available > 0:
                    ratio = remaining / available
                    if ratio > 1.5:
                        hard_islands += 1
        
        if hard_islands > 0:
            h += math.ceil(hard_islands / 2)
        
        return h

    def _count_components(self, state):
        if not state:
            return len(self.islands_map)
        
        graph = {(r, c): [] for r, c, _ in self.game.islands}
        
        for (r1, c1, r2, c2), num_bridges in state.items():
            if num_bridges > 0:
                graph[(r1, c1)].append((r2, c2))
                graph[(r2, c2)].append((r1, c1))
        
        visited = set()
        components = 0
        
        for island in graph.keys():
            if island not in visited:
                components += 1
                stack = [island]
                
                while stack:
                    node = stack.pop()
                    if node in visited:
                        continue
                    visited.add(node)
                    
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
        
        return components

    def _detect_unsat_early(self, state):
        # Check 1: Impossible capacity
        for (r,c), val in self.islands_map.items():
            curr = self._current_bridges(r, c, state)
            remaining = val - curr
            
            if remaining > 0:
                max_possible = 0
                for nr, nc in self.neighbors_map[(r,c)]:
                    key = tuple(sorted(((r,c), (nr,nc))))
                    flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                    curr_b = state.get(flat_key, 0)
                    can_add = 2 - curr_b
                    
                    neighbor_curr = self._current_bridges(nr, nc, state)
                    neighbor_remaining = self.islands_map[(nr,nc)] - neighbor_curr
                    
                    max_possible += min(can_add, neighbor_remaining)
                
                if max_possible < remaining:
                    return True
        
        # Check 2: Too many isolated islands
        unconnected = self._count_unconnected_islands(state)
        if unconnected > len(self.islands_map) * 0.7:
            possible_new = 0
            for (r,c) in self.islands_map.keys():
                curr = self._current_bridges(r, c, state)
                if curr == 0:
                    for nr, nc in self.neighbors_map[(r,c)]:
                        key = tuple(sorted(((r,c), (nr,nc))))
                        flat_key = (key[0][0], key[0][1], key[1][0], key[1][1])
                        if flat_key not in state:
                            if not self._is_crossing(flat_key, state):
                                possible_new += 1
                                break
            
            if possible_new < unconnected * 0.5:
                return True
        
        return False

    def _count_unconnected_islands(self, state):
        count = 0
        for (r,c) in self.islands_map.keys():
            if self._current_bridges(r, c, state) == 0:
                count += 1
        return count

    def _is_crossing(self, new_link, state):
        r1a, c1a, r2a, c2a = new_link
        h1 = r1a == r2a
        for (r1b, c1b, r2b, c2b), _ in state.items():
            h2 = r1b == r2b
            if h1 == h2:
                continue
            if h1:
                if min(c1a,c2a) < c1b < max(c1a,c2a) and min(r1b,r2b) < r1a < max(r1b,r2b):
                    return True
            else:
                if min(c1b,c2b) < c1a < max(c1b,c2b) and min(r1a,r2a) < r1b < max(r1a,r2a):
                    return True
        return False

    def _is_connected(self, state):
        if not self.game.islands:
            return True
        
        graph = {(r, c): [] for r, c, _ in self.game.islands}
        
        for (r1, c1, r2, c2), num_bridges in state.items():
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