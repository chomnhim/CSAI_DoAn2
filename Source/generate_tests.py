import os
import random
from typing import List, Tuple, Set, Dict

OUTPUT_DIR = 'Source/Inputs'

# Input-01 gốc từ đề bài (giữ nguyên để so sánh)
MANUAL_TESTS = {
    'input-01.txt': [
        [0,2,0,5,0,0,2],
        [0,0,0,0,0,0,0],
        [4,0,2,0,2,0,4],
        [0,0,0,0,0,0,0],
        [0,1,0,5,0,2,0],
        [0,0,0,0,0,0,0],
        [4,0,0,0,0,0,3]
    ]
}

def generate_hard_puzzle(rows: int, cols: int, density: float = 0.6, cycle_ratio: float = 0.4) -> List[List[int]]:
    """
    Tạo puzzle KHÓ bằng cách:
    1. Tạo lưới các đảo dày đặc.
    2. Tạo cây khung ngẫu nhiên (Spanning Tree) để đảm bảo liên thông.
    3. Thêm cạnh ngẫu nhiên (Cycles) để phá vỡ cấu trúc cây -> Khó suy luận.
    4. Random cầu đôi (Double bridges) để tăng độ khó.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # 1. Xác định các vị trí có thể đặt đảo (lưới 2x2)
    possible_nodes = []
    for r in range(0, rows, 2):
        for c in range(0, cols, 2):
            possible_nodes.append((r, c))
            
    if not possible_nodes:
        return grid

    # 2. Chọn ngẫu nhiên các đảo dựa trên mật độ (Density)
    # Với map khó, ta muốn mật độ cao
    num_islands = int(len(possible_nodes) * density)
    islands = set(random.sample(possible_nodes, num_islands))
    
    # Đảm bảo các đảo đã chọn nằm trong lưới
    # (Bước này chuẩn bị cho thuật toán nối dây)
    
    # 3. Tạo Spanning Tree (để đảm bảo tính liên thông - Connected)
    # Sử dụng thuật toán Prim ngẫu nhiên hoặc Kruskal
    active_islands = list(islands)
    if not active_islands:
        return grid
        
    connected = {active_islands[0]}
    edges = set() # Lưu trữ các cạnh ((r1,c1), (r2,c2))
    
    # Hàm lấy láng giềng hợp lệ
    def get_neighbors(node):
        r, c = node
        nbs = []
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in islands:
                nbs.append((nr, nc))
        return nbs

    # Xây dựng cây khung (kết nối tất cả đảo thành 1 nhóm)
    while len(connected) < len(islands):
        # Tìm tất cả các cạnh nối từ nhóm đã connected ra nhóm chưa connected
        potential_edges = []
        for node in connected:
            nbs = get_neighbors(node)
            for nb in nbs:
                if nb not in connected:
                    potential_edges.append((node, nb))
        
        if not potential_edges:
            # Trường hợp đảo bị cô lập, xóa nó khỏi danh sách islands
            unconnected = islands - connected
            islands = connected
            break
            
        # Chọn ngẫu nhiên 1 cạnh để nối
        u, v = random.choice(potential_edges)
        connected.add(v)
        # Chuẩn hóa cạnh (nhỏ trước lớn sau) để tránh trùng lặp
        edge = tuple(sorted((u, v)))
        edges.add(edge)

    # 4. Thêm Cycles (Tạo vòng lặp để tăng độ khó)
    # Duyệt qua tất cả các cặp láng giềng chưa nối
    all_possible_edges = []
    for node in islands:
        nbs = get_neighbors(node)
        for nb in nbs:
            edge = tuple(sorted((node, nb)))
            if edge not in edges:
                all_possible_edges.append(edge)
    
    # Loại bỏ trùng lặp trong all_possible_edges
    all_possible_edges = list(set(all_possible_edges))
    
    # Thêm số lượng cạnh dựa trên cycle_ratio
    num_extra_edges = int(len(all_possible_edges) * cycle_ratio)
    if num_extra_edges > 0:
        extra_edges = random.sample(all_possible_edges, num_extra_edges)
        for edge in extra_edges:
            edges.add(edge)

    # 5. Gán cầu đôi (Double Bridges) ngẫu nhiên
    # Map khó sẽ có nhiều cầu đôi
    final_connections = {} # Map edge -> weight (1 or 2)
    for edge in edges:
        # 60% cơ hội là cầu đôi
        weight = 2 if random.random() < 0.6 else 1
        final_connections[edge] = weight

    # 6. Tính giá trị số trên đảo
    # Reset grid và điền số
    for r, c in islands:
        value = 0
        # Tìm tất cả các cạnh nối với đảo này
        for (u, v), w in final_connections.items():
            if (r, c) == u or (r, c) == v:
                value += w
        
        # Hashi rule: Max value is 8
        if value > 8:
            # Nếu > 8, cần giảm bớt cầu (cắt bớt cạnh)
            # Với thuật toán này, hiếm khi > 8 vì chỉ có 4 hướng, max là 4*2=8
            # Tuy nhiên vẫn nên gán vào grid
            pass
            
        grid[r][c] = value

    return grid

def save_grid(filename: str, grid: List[List[int]]):
    """Lưu grid vào file và hiển thị thông tin"""
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        for row in grid:
            f.write(','.join(map(str, row)) + '\n')
    
    # Calculate statistics
    island_count = sum(1 for row in grid for cell in row if cell > 0)
    # Count value 8 islands (hardest)
    eights = sum(1 for row in grid for cell in row if cell == 8)
    # Count value 7 islands
    sevens = sum(1 for row in grid for cell in row if cell == 7)
    
    print(f"✓ {filename:15s} | Size: {len(grid):2d}x{len(grid[0]):2d} | Islands: {island_count:3d} | '8's: {eights} | '7's: {sevens}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 90)
    print("HARD PUZZLE GENERATOR (High Density, Cycles, Double Bridges)")
    print("=" * 90)
    
    # 1. Input mẫu
    for name, grid in MANUAL_TESTS.items():
        save_grid(name, grid)

    print("\n--- Small & Dense ---")
    save_grid('input-02.txt', generate_hard_puzzle(7, 7, density=0.9, cycle_ratio=0.5))
    save_grid('input-03.txt', generate_hard_puzzle(9, 9, density=0.7, cycle_ratio=0.4))
    save_grid('input-04.txt', generate_hard_puzzle(9, 9, density=0.8, cycle_ratio=0.6))
    save_grid('input-05.txt', generate_hard_puzzle(11, 11, density=0.6, cycle_ratio=0.5))
    save_grid('input-06.txt', generate_hard_puzzle(13, 13, density=0.65, cycle_ratio=0.5))
    save_grid('input-07.txt', generate_hard_puzzle(15, 15, density=0.6, cycle_ratio=0.6))
    save_grid('input-08.txt', generate_hard_puzzle(17, 17, density=0.6, cycle_ratio=0.7))
    save_grid('input-09.txt', generate_hard_puzzle(21, 21, density=0.55, cycle_ratio=0.7))
    save_grid('input-10.txt', generate_hard_puzzle(25, 25, density=0.5, cycle_ratio=0.8)) # 
if __name__ == "__main__":
    main()