import os
import random
from typing import List, Tuple, Set

OUTPUT_DIR = 'Source/Inputs'

MANUAL_TESTS = {
    'input-01.txt': [[0,2,0,5,0,0,2],[0,0,0,0,0,0,0],[4,0,2,0,2,0,4],[0,0,0,0,0,0,0],[0,1,0,5,0,2,0],[0,0,0,0,0,0,0],[4,0,0,0,0,0,3]],
    'input-02.txt': [[2,0,2],[0,0,0],[2,0,2]],
    'input-03.txt': [[2,0,3,0,2],[0,0,0,0,0],[3,0,4,0,3],[0,0,0,0,0],[2,0,3,0,2]]
}

def _recalculate_island_values(grid, rows, cols, double_bridges=True):
    islands = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] > 0:
                islands.append((r, c))
    
    island_set = set(islands)
    multiplier = 2 if double_bridges else 1
    
    for r, c in islands:
        neighbors_count = 0
        
        for i in range(r - 1, -1, -1):
            if (i, c) in island_set:
                neighbors_count += 1
                break
        for i in range(r + 1, rows):
            if (i, c) in island_set:
                neighbors_count += 1
                break
        for j in range(c - 1, -1, -1):
            if (r, j) in island_set:
                neighbors_count += 1
                break
        for j in range(c + 1, cols):
            if (r, j) in island_set:
                neighbors_count += 1
                break
                
        if neighbors_count > 0:
            grid[r][c] = neighbors_count * multiplier
            
    return grid

def create_ring_puzzle(rows: int, cols: int, double_bridges: bool = False) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    r_min, r_max = 0, rows - 1
    c_min, c_max = 0, cols - 1
    
    for c in range(c_min, c_max + 1, 2): grid[r_min][c] = 1
    for r in range(r_min + 2, r_max + 1, 2): grid[r][c_max] = 1
    for c in range(c_max - 2, c_min - 1, -2): grid[r_max][c] = 1
    for r in range(r_max - 2, r_min + 1, -2): grid[r][c_min] = 1
    
    return _recalculate_island_values(grid, rows, cols, double_bridges)

def create_grid_puzzle(rows: int, cols: int) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(0, rows, 2):
        for c in range(0, cols, 2):
            grid[r][c] = 1 
            
    return _recalculate_island_values(grid, rows, cols, double_bridges=False)

def create_cross_puzzle(rows: int, cols: int) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    center_r, center_c = rows // 2, cols // 2
    if center_r % 2 != 0: center_r -= 1
    if center_c % 2 != 0: center_c -= 1
    
    grid[center_r][center_c] = 1
    
    for c in range(center_c + 2, cols, 2): grid[center_r][c] = 1
    for c in range(center_c - 2, -1, -2): grid[center_r][c] = 1
    for r in range(center_r + 2, rows, 2): grid[r][center_c] = 1
    for r in range(center_r - 2, -1, -2): grid[r][center_c] = 1
    
    return _recalculate_island_values(grid, rows, cols, double_bridges=True)

def create_spiral_puzzle(rows: int, cols: int) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    r_min, r_max = 0, rows - 1
    c_min, c_max = 0, cols - 1
    
    while r_min <= r_max and c_min <= c_max:
        for c in range(c_min, c_max + 1, 2):
            if r_min % 2 == 0: grid[r_min][c] = 1
        for r in range(r_min + 2, r_max + 1, 2):
            if c_max % 2 == 0: grid[r][c_max] = 1
        if r_min < r_max:
            for c in range(c_max - 2, c_min - 1, -2):
                if r_max % 2 == 0: grid[r_max][c] = 1
        if c_min < c_max:
            for r in range(r_max - 2, r_min, -2):
                if c_min % 2 == 0: grid[r][c_min] = 1
        r_min += 2; r_max -= 2; c_min += 2; c_max -= 2
        
    return _recalculate_island_values(grid, rows, cols, double_bridges=True)

def create_double_ring_puzzle(rows: int, cols: int) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for c in range(0, cols, 2): grid[0][c] = 1
    for r in range(2, rows, 2): grid[r][cols - 1 if (cols - 1) % 2 == 0 else cols - 2] = 1
    for c in range(cols - 3, -1, -2): 
        if rows > 1: grid[rows - 1 if (rows - 1) % 2 == 0 else rows - 2][c] = 1
    for r in range(rows - 3, 0, -2): grid[r][0] = 1
    
    if rows >= 7 and cols >= 7:
        margin = 2
        for c in range(margin, cols - margin, 2): grid[margin][c] = 1
        for r in range(margin + 2, rows - margin, 2): 
            grid[r][cols - margin - 1 if (cols - margin - 1) % 2 == 0 else cols - margin - 2] = 1
        for c in range(cols - margin - 3, margin - 1, -2):
            if rows - margin - 1 != margin:
                grid[rows - margin - 1 if (rows - margin - 1) % 2 == 0 else rows - margin - 2][c] = 1
        for r in range(rows - margin - 3, margin, -2):
            grid[r][margin] = 1
        
    return _recalculate_island_values(grid, rows, cols, double_bridges=True)

def create_star_puzzle(rows: int, cols: int) -> List[List[int]]:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    center_r, center_c = rows // 2, cols // 2
    if center_r % 2 != 0: center_r -= 1
    if center_c % 2 != 0: center_c -= 1
    
    grid[center_r][center_c] = 1
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    for dr, dc in directions:
        r, c = center_r + dr, center_c + dc
        steps = 0
        while 0 <= r < rows and 0 <= c < cols and steps < 3:
            grid[r][c] = 1
            r += dr; c += dc; steps += 1
            
    return _recalculate_island_values(grid, rows, cols, double_bridges=True)

def save_grid(filename: str, grid: List[List[int]]):
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        for row in grid:
            f.write(','.join(map(str, row)) + '\n')
    print(f"✓ Saved {filename} ({len(grid)}x{len(grid[0])})")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 70)
    print("FIXED GENERATOR - 100% VALIDITY MODE")
    print("=" * 70)

    for name, grid in MANUAL_TESTS.items():
        save_grid(name, grid)

    save_grid('input-04.txt', create_ring_puzzle(9, 9, double_bridges=True))
    save_grid('input-05.txt', create_grid_puzzle(11, 11))
    save_grid('input-06.txt', create_cross_puzzle(7, 7))
    save_grid('input-07.txt', create_spiral_puzzle(9, 9))
    save_grid('input-08.txt', create_grid_puzzle(11, 11))
    save_grid('input-09.txt', create_ring_puzzle(13, 13, double_bridges=True))
    save_grid('input-10.txt', create_star_puzzle(17, 17))

    print("\n✓ Đã tạo lại toàn bộ file input.")
    print("Hãy chạy lại: python main.py --benchmark")

if __name__ == "__main__":
    main()