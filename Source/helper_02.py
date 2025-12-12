import time
from collections import deque
from itertools import combinations
from pysat.solvers import Glucose3
from typing import Dict, List, Tuple, Set
from helper_01 import HashiwokakeroGame

class CNFGenerator:
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.variables = {}  # Maps (r1, c1, r2, c2, k) -> int ID
        self.var_counter = 1
        self.clauses = []
        self.neighbors_map = {}
        for r, c, _ in self.game.islands:
            self.neighbors_map[(r, c)] = self.game.get_neighbors(r, c)

    def _get_var_key(self, r1, c1, r2, c2, k):
        if (r1, c1) > (r2, c2):
            return (r2, c2, r1, c1, k)
        return (r1, c1, r2, c2, k)

    def create_variable(self, i1: int, j1: int, i2: int, j2: int, num_bridges: int) -> int:
        key = self._get_var_key(i1, j1, i2, j2, num_bridges)
        if key not in self.variables:
            self.variables[key] = self.var_counter
            self.var_counter += 1
        return self.variables[key]
    
    def generate_cnf(self) -> Tuple[List[List[int]], Dict]:
        self.clauses = []
        self._create_variables()
        self._add_crossing_constraints()
        self._add_mutex_constraints()
        
        if not self._add_island_capacity_constraints():
            return None, self.variables
            
        return self.clauses, self.variables
    
    def _create_variables(self):
        for (r, c), neighbors in self.neighbors_map.items():
            for nr, nc in neighbors:
                if (r, c) < (nr, nc):
                    self.create_variable(r, c, nr, nc, 1)
                    self.create_variable(r, c, nr, nc, 2)

    def _add_mutex_constraints(self):
        seen = set()
        for (r1, c1, r2, c2, k), _ in self.variables.items():
            pair = (r1, c1, r2, c2)
            if pair in seen: continue
            seen.add(pair)
            v1 = self.variables.get((r1, c1, r2, c2, 1))
            v2 = self.variables.get((r1, c1, r2, c2, 2))
            if v1 and v2: self.clauses.append([-v1, -v2])

    def _add_crossing_constraints(self):
        connections = []
        seen = set()
        for (r1, c1, r2, c2, k) in self.variables:
            pair = (r1, c1, r2, c2)
            if pair not in seen:
                connections.append(pair)
                seen.add(pair)
        
        for i in range(len(connections)):
            for j in range(i + 1, len(connections)):
                if self._bridges_cross(connections[i], connections[j]):
                    pair1 = connections[i]
                    pair2 = connections[j]
                    vars1 = [self.variables.get(pair1 + (k,)) for k in [1, 2]]
                    vars2 = [self.variables.get(pair2 + (k,)) for k in [1, 2]]
                    for v1 in vars1:
                        for v2 in vars2:
                            if v1 and v2: self.clauses.append([-v1, -v2])

    def _bridges_cross(self, b1, b2):
        r1a, c1a, r2a, c2a = b1
        r1b, c1b, r2b, c2b = b2
        is_h1 = (r1a == r2a)
        is_h2 = (r1b == r2b)
        if is_h1 == is_h2: return False
        if is_h1:
            return (min(c1a, c2a) < c1b < max(c1a, c2a)) and \
                   (min(r1b, r2b) < r1a < max(r1b, r2b))
        else:
            return (min(c1b, c2b) < c1a < max(c1b, c2b)) and \
                   (min(r1a, r2a) < r1b < max(r1a, r2a))

    def _add_island_capacity_constraints(self):
        for r, c, val in self.game.islands:
            neighbors = self.neighbors_map.get((r, c), [])
            # Quick check: if max capacity < required value -> impossible
            if len(neighbors) * 2 < val: return False
            
            valid_configs = self._generate_configs(neighbors, val)
            if not valid_configs: return False
            
            config_vars = []
            for config in valid_configs:
                c_var = self.var_counter; self.var_counter += 1
                config_vars.append(c_var)
                config_dict = {(nr, nc): count for nr, nc, count in config}
                for nr, nc in neighbors:
                    count = config_dict.get((nr, nc), 0)
                    if count > 0:
                        b_var = self.create_variable(r, c, nr, nc, count)
                        self.clauses.append([-c_var, b_var])
                    else:
                        v1 = self.variables.get(self._get_var_key(r, c, nr, nc, 1))
                        v2 = self.variables.get(self._get_var_key(r, c, nr, nc, 2))
                        if v1: self.clauses.append([-c_var, -v1])
                        if v2: self.clauses.append([-c_var, -v2])
            
            # Must choose exactly one config
            self.clauses.append(config_vars) # At least one
            # At most one
            for i in range(len(config_vars)):
                for j in range(i + 1, len(config_vars)):
                    self.clauses.append([-config_vars[i], -config_vars[j]])
        return True

    def _generate_configs(self, neighbors, target_sum):
        results = []
        def backtrack(idx, current_sum, current_config):
            if current_sum > target_sum: return
            if idx == len(neighbors):
                if current_sum == target_sum: results.append(list(current_config))
                return
            nr, nc = neighbors[idx]
            # Option 0 bridges
            backtrack(idx + 1, current_sum, current_config)
            # Option 1 bridge
            current_config.append((nr, nc, 1))
            backtrack(idx + 1, current_sum + 1, current_config)
            current_config.pop()
            # Option 2 bridges
            current_config.append((nr, nc, 2))
            backtrack(idx + 1, current_sum + 2, current_config)
            current_config.pop()
        backtrack(0, 0, [])
        return results


class PySATSolver:
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.cnf_gen = CNFGenerator(game)
        
    def solve(self) -> Tuple[dict, float]:
        print("Solving with PySAT (Glucose3)...")
        start_time = time.perf_counter()
        
        # 1. Generate CNF
        result = self.cnf_gen.generate_cnf()
        if result is None:
            solve_time = time.perf_counter() - start_time
            print(f"  UNSAT (Local Conflict Detected in Generator) ({solve_time:.4f}s)")
            self.diagnose_failure(connectivity_failed=False)
            return None, solve_time

        clauses, variables = result
        if not clauses:
            return None, time.perf_counter() - start_time
            
        solver = Glucose3()
        for c in clauses: 
            solver.add_clause(c)
        
        # 2. Iterative Solving (Connectivity Check Loop)
        max_attempts = 100
        attempt = 0
        bridge_var_ids = set(variables.values())
        
        while solver.solve() and attempt < max_attempts:
            attempt += 1
            model = solver.get_model()
            solution = self._extract_solution(model, variables)
            
            # Check Connectivity
            if self._is_connected(solution):
                solve_time = time.perf_counter() - start_time
                print(f"  SAT Found (Connected) - Attempt {attempt} ({solve_time:.4f}s)")
                return solution, solve_time
            
            # Blocking Clause
            blocking_clause = [-lit for lit in model if abs(lit) in bridge_var_ids]
            solver.add_clause(blocking_clause)
            
            if attempt <= 5 or attempt % 10 == 0:
                print(f"    Attempt {attempt}: Disconnected solution found. Retrying...")
        
        solve_time = time.perf_counter() - start_time
        
        if attempt == 0:
            print(f"  UNSAT (Basic Constraints Unsatisfiable) ({solve_time:.4f}s)")
            self.diagnose_failure(connectivity_failed=False) 
        else:
            print(f"  UNSAT (No connected solution found after {attempt} attempts) ({solve_time:.4f}s)")
            self.diagnose_failure(connectivity_failed=True)
            
        return None, solve_time

    def _is_connected(self, solution: dict) -> bool:
        if not self.game.islands:
            return True
        
        # Build graph from solution
        graph = {}
        for r, c, _ in self.game.islands:
            graph[(r, c)] = []
        
        for (r1, c1, r2, c2), num_bridges in solution.items():
            if num_bridges > 0:
                graph[(r1, c1)].append((r2, c2))
                graph[(r2, c2)].append((r1, c1))
        
        # BFS
        start_island = (self.game.islands[0][0], self.game.islands[0][1])
        visited = set()
        queue = deque([start_island])
        visited.add(start_island)
        
        while queue:
            current = queue.popleft()
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.game.islands)

    def _extract_solution(self, model, variables):
        solution = {}
        id_to_key = {v: k for k, v in variables.items()}
        for val in model:
            if val > 0:
                key = id_to_key.get(val)
                # Ensure it's a bridge variable (5 components)
                if key and len(key) == 5:
                    solution[(key[0], key[1], key[2], key[3])] = key[4]
        return solution

    def diagnose_failure(self, connectivity_failed=False):
        print("\n" + "!"*50)
        print("DIAGNOSIS REPORT")
        print("!"*50)
        
        if connectivity_failed:
            print("  CONNECTIVITY FAILURE:")
            print("  - Solutions satisfying local constraints were found.")
            print("  - HOWEVER, all found solutions were disconnected (split into groups).")
            print("  - No solution exists that connects ALL islands together.")
            print("  - The puzzle design might be invalid.")
            print("!"*50 + "\n")
            return
        
        islands = self.game.islands
        neighbors_map = self.cnf_gen.neighbors_map
        found_reason = False

        total_bridges = sum(val for r, c, val in islands)
        if total_bridges % 2 != 0:
            print(f" MATHEMATICAL ERROR: Total island value is {total_bridges} (Odd number).")
            print("  (Sum of bridges x 2 must be even -> Impossible to solve).")
            found_reason = True

        for r, c, val in islands:
            neighbors = neighbors_map.get((r, c), [])
            num_neighbors = len(neighbors)
            max_possible = num_neighbors * 2
            
            if val > max_possible:
                print(f" LOCAL ERROR at Island ({r},{c}) value {val}:")
                print(f"  - Only has {num_neighbors} neighbors.")
                print(f"  - Max possible bridges: {max_possible} (Deficit: {val - max_possible}).")
                found_reason = True
            
            if num_neighbors == 0:
                print(f" ISOLATION ERROR at Island ({r},{c}): Needs {val} bridges but has NO neighbors.")
                found_reason = True

        for r, c, val in islands:
            neighbors = neighbors_map.get((r, c), [])
            max_neighbors_can_take = 0
            
            for nr, nc in neighbors:
                n_val = next(v for nr_, nc_, v in islands if nr_ == nr and nc_ == nc)
                max_contribution = min(2, n_val)
                max_neighbors_can_take += max_contribution
            
            if val > max_neighbors_can_take:
                print(f" NEIGHBOR CAPACITY ERROR at Island ({r},{c}) value {val}:")
                print(f"  - Neighbors can only accept a total of {max_neighbors_can_take} bridges.")
                print(f"  - Not enough capacity to support {val} bridges.")
                found_reason = True

        if not found_reason:
            print(" GLOBAL CONFLICT:")
            print("  All local constraints seem valid, but a global contradiction exists.")
            print("  (e.g., Mandatory crossings, or isolated sub-graphs preventing a solution).")
        
        print("!"*50 + "\n")