import time
from typing import List, Tuple, Dict, Optional
from helper_01 import HashiwokakeroGame


class AStarSolver:
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
    def heuristic(self, state) -> float:
        return 0
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        start_time = time.time()
        self.states_explored = 0
        solution = None
        time_taken = time.time() - start_time
        return solution, time_taken


class BacktrackingSolver:
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
    def is_valid(self, state) -> bool:
        return True
    
    def solve_recursive(self, state, depth: int) -> Optional[List[List[str]]]:
        self.states_explored += 1
        return None
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        start_time = time.time()
        self.states_explored = 0
        initial_state = None
        solution = self.solve_recursive(initial_state, 0)
        time_taken = time.time() - start_time
        return solution, time_taken


class BruteForceSolver:
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
        if len(game.islands) > 8:
            print(f"⚠ WARNING: Puzzle có {len(game.islands)} đảo.")
            print(f"   Brute force có thể mất rất lâu!")
            print(f"   Số combinations ước tính: ~2^n với n >> 20")
    
    def generate_all_combinations(self):
        yield None
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        start_time = time.time()
        self.states_explored = 0
        solution = None
        time_taken = time.time() - start_time
        return solution, time_taken


def create_empty_board(rows: int, cols: int) -> List[List[str]]:
    return [["0" for _ in range(cols)] for _ in range(rows)]


def can_place_bridge(board: List[List[str]], r1: int, c1: int,
                     r2: int, c2: int, num_bridges: int) -> bool:
    return True


def place_bridge(board: List[List[str]], r1: int, c1: int,
                 r2: int, c2: int, num_bridges: int) -> List[List[str]]:
    return board


def count_bridges_at_island(board: List[List[str]], r: int, c: int) -> int:
    return 0


def is_goal_state(board: List[List[str]], game: HashiwokakeroGame) -> bool:
    return False


if __name__ == "__main__":
    test_input = "Source/Inputs/input-01.txt"
    
    try:
        from helper_01 import HashiwokakeroGame
        
        game = HashiwokakeroGame(test_input)
        print(f"Loaded puzzle: {game.rows}x{game.cols}, {len(game.islands)} islands")
        
        print("\nTesting A* Solver...")
        try:
            solver = AStarSolver(game)
            solution, time_taken = solver.solve()
            print(f"Solution found: {solution is not None}")
            print(f"Time: {time_taken:.4f}s")
            print(f"States explored: {solver.states_explored}")
        except NotImplementedError:
            print("A* Solver chưa được implement")
        
        print("\nTesting Backtracking Solver...")
        try:
            solver = BacktrackingSolver(game)
            solution, time_taken = solver.solve()
            print(f"Solution found: {solution is not None}")
            print(f"Time: {time_taken:.4f}s")
            print(f"States explored: {solver.states_explored}")
        except NotImplementedError:
            print("Backtracking Solver chưa được implement")
        
        if len(game.islands) <= 8:
            print("\nTesting Brute Force Solver...")
            try:
                solver = BruteForceSolver(game)
                solution, time_taken = solver.solve()
                print(f"Solution found: {solution is not None}")
                print(f"Time: {time_taken:.4f}s")
                print(f"States explored: {solver.states_explored}")
            except NotImplementedError:
                print("Brute Force Solver chưa được implement")
        else:
            print("\nBrute Force skipped (puzzle too large)")
            
    except FileNotFoundError:
        print(f"File {test_input} không tồn tại")
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
