"""
Template cho các solver algorithms
Sử dụng template này để implement A*, Backtracking, và Brute Force
"""

import time
from typing import List, Tuple, Dict, Optional
from helper_01 import HashiwokakeroGame


class AStarSolver:
    """
    A* Search Algorithm để giải Hashiwokakero
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0  # QUAN TRỌNG: Đếm số states
        
    def heuristic(self, state) -> float:
        """
        Hàm heuristic để ước lượng chi phí từ state hiện tại đến goal
        """
        return 0
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng A* search
        """
        start_time = time.time()
        
        self.states_explored = 0  # Reset counter
        solution = None
        
        
        time_taken = time.time() - start_time
        return solution, time_taken


class BacktrackingSolver:
    """
    Backtracking Algorithm để giải Hashiwokakero
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
    def is_valid(self, state) -> bool:
        """
        Kiểm tra state có hợp lệ không (không vi phạm constraints)
        """
        return True
    
    def solve_recursive(self, state, depth: int) -> Optional[List[List[str]]]:
        """
        Hàm đệ quy backtracking
        """
        self.states_explored += 1
        
        return None
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng backtracking
        """
        start_time = time.time()
        
        self.states_explored = 0
        initial_state = None  #Tạo initial state
        
        solution = self.solve_recursive(initial_state, 0)
        
        time_taken = time.time() - start_time
        return solution, time_taken


class BruteForceSolver:
    """
    Brute Force Algorithm để giải Hashiwokakero
    
    CHÚ Ý: Chỉ dùng cho puzzle nhỏ (≤8 đảo)
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
        # Cảnh báo nếu puzzle quá lớn
        if len(game.islands) > 8:
            print(f"⚠ WARNING: Puzzle có {len(game.islands)} đảo.")
            print(f"   Brute force có thể mất rất lâu!")
            print(f"   Số combinations ước tính: ~2^n với n >> 20")
    
    def generate_all_combinations(self):
        """
        Sinh tất cả các cách nối cầu có thể
        """
        
        yield None  # Placeholder
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng brute force
        """
        start_time = time.time()
        
        self.states_explored = 0
        
        solution = None
        
        time_taken = time.time() - start_time
        return solution, time_taken


# =============================================================================
# HELPER FUNCTIONS (có thể dùng chung cho các solvers)
# =============================================================================

def create_empty_board(rows: int, cols: int) -> List[List[str]]:
    """Tạo board trống"""
    return [["0" for _ in range(cols)] for _ in range(rows)]


def can_place_bridge(board: List[List[str]], r1: int, c1: int, 
                     r2: int, c2: int, num_bridges: int) -> bool:
    """
    Kiểm tra có thể đặt cầu giữa (r1,c1) và (r2,c2) không
    """
    return True


def place_bridge(board: List[List[str]], r1: int, c1: int, 
                r2: int, c2: int, num_bridges: int) -> List[List[str]]:
    """
    Đặt cầu trên board
    """
    return board


def count_bridges_at_island(board: List[List[str]], r: int, c: int) -> int:
    """
    Đếm số cầu đã nối với đảo tại (r, c)
    """
    return 0


def is_goal_state(board: List[List[str]], game: HashiwokakeroGame) -> bool:
    """
    Kiểm tra board có phải goal state không
    """
    return False


# =============================================================================
# TEST CODE
# =============================================================================

if __name__ == "__main__":
    # Test với một puzzle nhỏ
    test_input = "Source/Inputs/input-01.txt"
    
    try:
        from helper_01 import HashiwokakeroGame
        
        game = HashiwokakeroGame(test_input)
        print(f"Loaded puzzle: {game.rows}x{game.cols}, {len(game.islands)} islands")
        
        # Test A*
        print("\nTesting A* Solver...")
        try:
            solver = AStarSolver(game)
            solution, time_taken = solver.solve()
            print(f"Solution found: {solution is not None}")
            print(f"Time: {time_taken:.4f}s")
            print(f"States explored: {solver.states_explored}")
        except NotImplementedError:
            print("A* Solver chưa được implement")
        
        # Test Backtracking
        print("\nTesting Backtracking Solver...")
        try:
            solver = BacktrackingSolver(game)
            solution, time_taken = solver.solve()
            print(f"Solution found: {solution is not None}")
            print(f"Time: {time_taken:.4f}s")
            print(f"States explored: {solver.states_explored}")
        except NotImplementedError:
            print("Backtracking Solver chưa được implement")
        
        # Test Brute Force (chỉ nếu puzzle nhỏ)
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