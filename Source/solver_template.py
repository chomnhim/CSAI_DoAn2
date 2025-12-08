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
    
    TODO: Implement
    - __init__: Khởi tạo solver
    - heuristic: Hàm heuristic để ước lượng khoảng cách đến goal
    - solve: Giải puzzle bằng A*
    
    Yêu cầu:
    - Phải có thuộc tính self.states_explored để đếm số states đã explore
    - Trả về (solution, time_taken)
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0  # QUAN TRỌNG: Đếm số states
        
    def heuristic(self, state) -> float:
        """
        Hàm heuristic để ước lượng chi phí từ state hiện tại đến goal
        
        Gợi ý:
        - Đếm số đảo chưa đủ cầu
        - Tổng số cầu còn thiếu
        - Khoảng cách giữa các đảo chưa nối
        
        Returns:
            float: Chi phí ước lượng (càng nhỏ càng gần goal)
        """
        # TODO: Implement heuristic function
        return 0
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng A* search
        
        Returns:
            (solution, time_taken): Solution matrix và thời gian chạy
        """
        start_time = time.time()
        
        # TODO: Implement A* algorithm
        # Pseudo-code:
        # 1. Khởi tạo open_set với state ban đầu
        # 2. Trong khi open_set không rỗng:
        #    a. Lấy state có f(n) = g(n) + h(n) nhỏ nhất
        #    b. Nếu là goal state, return solution
        #    c. Tạo các successor states
        #    d. Thêm vào open_set
        # 3. Nếu không tìm thấy, return None
        
        self.states_explored = 0  # Reset counter
        solution = None
        
        # IMPLEMENT CODE HERE
        
        time_taken = time.time() - start_time
        return solution, time_taken


class BacktrackingSolver:
    """
    Backtracking Algorithm để giải Hashiwokakero
    
    TODO: Implement
    - __init__: Khởi tạo solver
    - is_valid: Kiểm tra state có hợp lệ không
    - solve_recursive: Hàm đệ quy backtracking
    - solve: Entry point
    
    Yêu cầu:
    - Phải có thuộc tính self.states_explored
    - Trả về (solution, time_taken)
    """
    
    def __init__(self, game: HashiwokakeroGame):
        self.game = game
        self.states_explored = 0
        
    def is_valid(self, state) -> bool:
        """
        Kiểm tra state có hợp lệ không (không vi phạm constraints)
        
        Returns:
            bool: True nếu state hợp lệ
        """
        # TODO: Implement validation
        return True
    
    def solve_recursive(self, state, depth: int) -> Optional[List[List[str]]]:
        """
        Hàm đệ quy backtracking
        
        Args:
            state: State hiện tại
            depth: Độ sâu hiện tại
            
        Returns:
            Solution hoặc None
        """
        self.states_explored += 1
        
        # TODO: Implement backtracking
        # Pseudo-code:
        # 1. Nếu state là goal, return state
        # 2. Nếu state không hợp lệ, return None
        # 3. Thử từng lựa chọn:
        #    a. Đặt cầu giữa 2 đảo
        #    b. Gọi đệ quy
        #    c. Nếu tìm thấy solution, return
        #    d. Nếu không, backtrack (bỏ cầu)
        # 4. Return None nếu không có lựa chọn nào thành công
        
        return None
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng backtracking
        
        Returns:
            (solution, time_taken)
        """
        start_time = time.time()
        
        self.states_explored = 0
        initial_state = None  # TODO: Tạo initial state
        
        solution = self.solve_recursive(initial_state, 0)
        
        time_taken = time.time() - start_time
        return solution, time_taken


class BruteForceSolver:
    """
    Brute Force Algorithm để giải Hashiwokakero
    
    CHÚ Ý: Chỉ dùng cho puzzle nhỏ (≤8 đảo)
    
    TODO: Implement
    - __init__: Khởi tạo
    - generate_all_combinations: Sinh tất cả các cách nối cầu có thể
    - solve: Thử từng combination
    
    Yêu cầu:
    - Phải có thuộc tính self.states_explored
    - Trả về (solution, time_taken)
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
        
        Yields:
            state: Mỗi combination
        """
        # TODO: Implement combination generator
        # Gợi ý:
        # - Với mỗi cặp đảo có thể nối, thử 0, 1, hoặc 2 cầu
        # - Sử dụng itertools.product hoặc đệ quy
        
        yield None  # Placeholder
    
    def solve(self) -> Tuple[Optional[List[List[str]]], float]:
        """
        Giải puzzle bằng brute force
        
        Returns:
            (solution, time_taken)
        """
        start_time = time.time()
        
        self.states_explored = 0
        
        # TODO: Implement brute force
        # Pseudo-code:
        # 1. Sinh tất cả combinations
        # 2. Với mỗi combination:
        #    a. Kiểm tra có hợp lệ không
        #    b. Nếu hợp lệ, return
        # 3. Return None nếu không tìm thấy
        
        solution = None
        
        # IMPLEMENT CODE HERE
        
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
    
    Args:
        board: Board hiện tại
        r1, c1: Tọa độ đảo 1
        r2, c2: Tọa độ đảo 2
        num_bridges: Số cầu (1 hoặc 2)
        
    Returns:
        bool: True nếu có thể đặt cầu
    """
    # TODO: Implement
    # Kiểm tra:
    # - Cầu phải ngang hoặc dọc (không chéo)
    # - Không cắt qua đảo khác
    # - Không cắt qua cầu khác
    return True


def place_bridge(board: List[List[str]], r1: int, c1: int, 
                r2: int, c2: int, num_bridges: int) -> List[List[str]]:
    """
    Đặt cầu trên board
    
    Args:
        board: Board hiện tại
        r1, c1: Tọa độ đảo 1
        r2, c2: Tọa độ đảo 2
        num_bridges: Số cầu (1 hoặc 2)
        
    Returns:
        Board mới với cầu đã đặt
    """
    # TODO: Implement
    # - Copy board
    # - Đặt cầu (-, =, |, $) tùy hướng và số lượng
    return board


def count_bridges_at_island(board: List[List[str]], r: int, c: int) -> int:
    """
    Đếm số cầu đã nối với đảo tại (r, c)
    
    Returns:
        int: Số cầu
    """
    # TODO: Implement
    return 0


def is_goal_state(board: List[List[str]], game: HashiwokakeroGame) -> bool:
    """
    Kiểm tra board có phải goal state không
    
    Kiểm tra:
    - Mỗi đảo có đúng số cầu
    - Tất cả đảo connected
    
    Returns:
        bool: True nếu là goal state
    """
    # TODO: Implement
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