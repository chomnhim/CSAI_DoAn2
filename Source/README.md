# Hashiwokakero Solver - Đồ Án AI

Bộ giải puzzle Hashiwokakero (Bridges) sử dụng nhiều thuật toán AI bao gồm PySAT, A*, Backtracking và Brute Force.

## 📋 Mục Lục

- [Tổng Quan](#tổng-quan)
- [Tính Năng](#tính-năng)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [Cấu Trúc Thư Mục](#cấu-trúc-thư-mục)
- [Các Thuật Toán](#các-thuật-toán)
- [Định Dạng Input/Output](#định-dạng-inputoutput)
- [Ví Dụ](#ví-dụ)
- [Hiệu Năng](#hiệu-năng)
- [Thành Viên](#thành-viên)

## 🎯 Tổng Quan

Hashiwokakero là trò chơi logic puzzle yêu cầu kết nối các đảo (được đánh số) bằng cầu theo các luật:
- Cầu phải là đường thẳng (ngang hoặc dọc)
- Cầu không được cắt nhau hoặc đi qua đảo khác
- Tối đa 2 cầu nối giữa một cặp đảo
- Mỗi đảo phải có đúng số cầu như số ghi trên đảo
- Tất cả đảo phải được kết nối thành một nhóm duy nhất

Dự án này triển khai nhiều thuật toán giải puzzle và cung cấp công cụ phân tích toàn diện.

## ✨ Tính Năng

- **Nhiều Thuật Toán Giải**:
  - PySAT (SAT solver dựa trên CNF)
  - A* Search Algorithm
  - Backtracking với tối ưu hóa
  - Brute Force (cho puzzle nhỏ)

- **Tính Năng Nâng Cao**:
  - Phát hiện UNSAT sớm
  - Forward checking
  - MRV (Most Restricted Variable) heuristic
  - LCV (Least Constraining Value) ordering
  - Benchmark tự động
  - Công cụ so sánh thuật toán

- **Giao Diện Thân Thiện**:
  - Menu tương tác
  - Hỗ trợ command-line arguments
  - Theo dõi tiến trình
  - Báo cáo chẩn đoán chi tiết

## 📦 Yêu Cầu Hệ Thống

- Python 3.7 trở lên
- Thư viện cần thiết (xem `requirements.txt`):
  ```
  numpy>=1.19.0
  python-sat>=0.1.7.dev0
  ```

## 🚀 Cài Đặt

1. **Giải nén hoặc clone project**:
   ```bash
   cd StudentID1_StudentID2
   ```

2. **Cài đặt thư viện**:
   ```bash
   pip install -r Source/requirements.txt
   ```

3. **Kiểm tra cài đặt**:
   ```bash
   python Source/main.py --help
   ```

## 💻 Hướng Dẫn Sử Dụng

### Chế Độ Tương Tác (Khuyên dùng cho người mới)

```bash
python Source/main.py
```

hoặc

```bash
python Source/main.py -i
```

Chương trình sẽ hiển thị menu với các tùy chọn:
1. Giải Puzzle (Solve)
2. Chạy Benchmark (Tất cả test cases)
3. So sánh Solvers (Compare)
4. Thoát (Exit)

### Chế Độ Command-Line

#### Giải một puzzle với PySAT (mặc định):
```bash
python Source/main.py --input Source/Inputs/input-01.txt
```

#### Giải với thuật toán cụ thể:
```bash
# Sử dụng A*
python Source/main.py --input Source/Inputs/input-01.txt --solver astar

# Sử dụng Backtracking
python Source/main.py --input Source/Inputs/input-01.txt --solver backtrack

# Sử dụng Brute Force (chỉ cho puzzle nhỏ)
python Source/main.py --input Source/Inputs/input-01.txt --solver bruteforce
```

#### Chạy benchmark trên tất cả test cases:
```bash
python Source/main.py --benchmark
```

#### So sánh tất cả thuật toán trên một puzzle:
```bash
python Source/main.py --compare --input Source/Inputs/input-01.txt
```

#### Chỉ định file output tùy chỉnh:
```bash
python Source/main.py --input Source/Inputs/input-01.txt --output custom-output.txt
```

### Các Tùy Chọn Command-Line

| Tùy chọn | Mô tả |
|----------|-------|
| `--input FILE` | Đường dẫn đến file input |
| `--output FILE` | Đường dẫn file output (tùy chọn) |
| `--solver ALGORITHM` | Chọn thuật toán: `pysat`, `astar`, `backtrack`, `bruteforce` |
| `--benchmark` | Chạy benchmark tất cả test cases |
| `--compare` | So sánh tất cả thuật toán |
| `-i, --interactive` | Chế độ tương tác |
| `-h, --help` | Hiển thị trợ giúp |

## 📁 Cấu Trúc Thư Mục

```
StudentID1_StudentID2/
│
├── Docs/
│   ├── Report.pdf                 # Báo cáo đồ án
│   └── References/                # Tài liệu tham khảo
│
├── Source/
│   ├── Inputs/                    # Thư mục chứa test cases
│   │   ├── input-01.txt          # Test case 1 (7x7)
│   │   ├── input-02.txt          # Test case 2 (3x3)
│   │   ├── input-03.txt          # Test case 3 (5x5)
│   │   ├── input-04.txt          # Test case 4 (9x9)
│   │   ├── input-05.txt          # Test case 5 (11x11)
│   │   ├── input-06.txt          # Test case 6 (7x7 - Cross)
│   │   ├── input-07.txt          # Test case 7 (9x9 - Spiral)
│   │   ├── input-08.txt          # Test case 8 (11x11)
│   │   ├── input-09.txt          # Test case 9 (13x13)
│   │   └── input-10.txt          # Test case 10 (17x17)
│   │
│   ├── Outputs/                   # Thư mục kết quả (tự động tạo)
│   │   ├── output-01.txt
│   │   ├── output-02.txt
│   │   └── ...
│   │
│   ├── main.py                    # File chính - Entry point
│   ├── helper_01.py               # Game logic & utilities
│   ├── helper_02.py               # CNF generator & PySAT solver
│   ├── astar_solver.py            # A* algorithm
│   ├── backtrack_solver.py        # Backtracking algorithm
│   ├── bruteforce_solver.py       # Brute force algorithm
│   ├── generate_tests.py          # Tool tạo test cases
│   ├── solver_template.py         # Template cho solver
│   ├── requirements.txt           # Thư viện cần cài
│   └── README.txt                 # File này
│
└── README.md                      # Hướng dẫn chi tiết
```

## 🧠 Các Thuật Toán

### 1. PySAT (SAT Solver)
- **Nguyên lý**: Chuyển puzzle thành bài toán SAT (CNF)
- **Ưu điểm**: Nhanh nhất, tìm được UNSAT sớm
- **Nhược điểm**: Cần hiểu biết về logic CNF
- **Khuyên dùng**: Tất cả các trường hợp

**Cách hoạt động**:
1. Tạo biến logic cho mỗi cầu có thể
2. Sinh các ràng buộc CNF:
   - Ràng buộc về số cầu mỗi đảo
   - Ràng buộc cầu không cắt nhau
   - Ràng buộc loại trừ lẫn nhau (1 cầu hoặc 2 cầu)
3. Sử dụng Glucose3 solver để giải CNF
4. Chuyển đổi kết quả về dạng cầu

### 2. A* Search
- **Nguyên lý**: Tìm kiếm có thông tin với hàm heuristic
- **Ưu điểm**: Cân bằng giữa tốc độ và tối ưu
- **Nhược điểm**: Phụ thuộc vào heuristic
- **Khuyên dùng**: Puzzle trung bình (7x7 đến 13x13)

**Heuristic Function**:
- h(n) = ceil(tổng cầu còn thiếu / 2)
- Phạt số lượng component chưa kết nối
- Phạt đảo cô lập
- Phạt đảo "khó" (cần nhiều cầu nhưng ít lựa chọn)

### 3. Backtracking
- **Nguyên lý**: Thử từng khả năng và quay lui khi thất bại
- **Ưu điểm**: Đơn giản, dễ implement
- **Nhược điểm**: Chậm với puzzle lớn
- **Khuyên dùng**: Puzzle nhỏ (≤ 9x9)

**Tối ưu hóa**:
- Forward checking
- MRV (Most Restricted Variable)
- LCV (Least Constraining Value)
- Early pruning

### 4. Brute Force
- **Nguyên lý**: Thử tất cả các tổ hợp có thể
- **Ưu điểm**: Đảm bảo tìm được lời giải (nếu có)
- **Nhược điểm**: Cực kỳ chậm
- **Khuyên dùng**: CHỈ cho puzzle rất nhỏ (≤ 8 đảo)

**Lưu ý**: 
- Số lượng tổ hợp: 3^n (n = số cặp đảo có thể nối)
- Thời gian tăng theo cấp số nhân
- Có thể mất hàng giờ với puzzle 11x11

## 📝 Định Dạng Input/Output

### Input Format

File text với ma trận các số, phân cách bằng dấu phẩy:
- `0`: Ô trống
- `1-8`: Đảo với số cầu cần nối

**Ví dụ** (`input-01.txt`):
```
0,2,0,5,0,0,2
0,0,0,0,0,0,0
4,0,2,0,2,0,4
0,0,0,0,0,0,0
0,1,0,5,0,2,0
0,0,0,0,0,0,0
4,0,0,0,0,0,3
```

### Output Format

File text với ma trận kết quả:
- `"0"`: Ô trống
- `"1"` đến `"8"`: Đảo (giữ nguyên)
- `"-"`: 1 cầu ngang
- `"="`: 2 cầu ngang
- `"|"`: 1 cầu dọc
- `"$"`: 2 cầu dọc

**Ví dụ** (`output-01.txt`):
```
["0", "2", "=", "5", "-", "-", "2"]
["0", "0", "0", "$", "0", "0", "|"]
["4", "=", "2", "$", "2", "=", "4"]
["$", "0", "0", "$", "0", "0", "|"]
["$", "1", "-", "5", "=", "2", "|"]
["$", "0", "0", "0", "0", "0", "|"]
["4", "=", "=", "=", "=", "=", "3"]
```

### Trường Hợp Không Có Lời Giải (UNSAT)

Nếu puzzle không có lời giải, file output sẽ chứa:
```
NO SOLUTION
(Map này không có lời giải)
```

## 📊 Ví Dụ

### Ví Dụ 1: Giải puzzle đơn giản

```bash
 python Source/main.py --input Source/Inputs/input-02.txt

================================================================================
SOLVING: Inputs\input-02.txt
SOLVER: PYSAT
================================================================================
Grid: 3x3
Islands: 4

Solving with PySAT (Glucose3)...
✓ SAT Found (0.0002s)

================================================================================
SOLUTION
================================================================================
['2', '=', '2']
['0', '0', '0']
['2', '=', '2']

✓ Solution hợp lệ!

✓ Đã lưu solution vào: Outputs\output-02.txt

⏱ Thời gian: 0.0003s
```

### Ví Dụ 2: So sánh thuật toán

```bash
 python Source/main.py --compare --input Source/Inputs/input-03.txt

================================================================================
SO SÁNH SOLVERS - input-03.txt
================================================================================
Grid: 5x5, Islands: 9


--- Testing PYSAT ---
Solving with PySAT (Glucose3)...
✓ SAT Found (0.0016s)

--- Testing ASTAR ---
Solving with A*...
✓ Solution found! Nodes: 13

--- Testing BACKTRACK ---
Solving with Backtracking...
✓ Solution found! Nodes: 9

--- Testing BRUTEFORCE ---

Solving with Optimized Brute Force...
✓ Found solution!
  - Nodes explored: 46,159

================================================================================
KẾT QUẢ SO SÁNH
================================================================================
Solver          Status       Valid    Time (s)     Nodes           Speedup
--------------------------------------------------------------------------------
PYSAT           ✓ Pass       ✓        0.0018       -               1.00x
ASTAR           ✓ Pass       ✓        0.0045       13              0.39x
BACKTRACK       ✓ Pass       ✓        0.0011       9               1.56x
BRUTEFORCE      ✓ Pass       ✓        0.4016       46,159          0.00x
================================================================================
```

### Ví Dụ 3: Benchmark tất cả test cases

```bash
 python Source/main.py --benchmark

================================================================================
BENCHMARK - CHẠY TẤT CẢ TEST CASES
================================================================================
📁 Found 10 input files in: Inputs
Tìm thấy 10 test cases.

================================================================================
Test 1/10: input-01.txt
================================================================================
Size: 7x7, Islands: 12
Solving with PySAT (Glucose3)...
✓ SAT Found (0.0458s)
✓ Đã lưu: Outputs\output-01.txt

================================================================================
Test 2/10: input-02.txt
================================================================================
Size: 3x3, Islands: 4
Solving with PySAT (Glucose3)...
✓ SAT Found (0.0003s)
✓ Đã lưu: Outputs\output-02.txt

================================================================================
Test 3/10: input-03.txt
================================================================================
Size: 5x5, Islands: 9
Solving with PySAT (Glucose3)...
✓ SAT Found (0.0010s)
✓ Đã lưu: Outputs\output-03.txt

... (các test khác)

================================================================================
Test 9/10: input-09.txt
================================================================================
Size: 13x13, Islands: 24
Solving with PySAT (Glucose3)...
✗ UNSAT (0.0011s)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PHÂN TÍCH LỖI (DIAGNOSIS REPORT)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
➤ LỖI CẤU TRÚC PHỨC TẠP (Global Conflict):
  Các ràng buộc cục bộ đều thỏa mãn, nhưng mâu thuẫn xảy ra ở cấu trúc toàn cục.
  (Ví dụ: Cầu bắt buộc phải cắt nhau mới nối đủ số, hoặc đồ thị bị chia cắt).
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

➤ KHÔNG CÓ LỜI GIẢI.

================================================================================
TỔNG KẾT BENCHMARK
================================================================================
File                 Size       Islands    Status       Time (s)     Valid
--------------------------------------------------------------------------------
input-01.txt         7x7        12         ✓ Pass       0.0471       ✓
input-02.txt         3x3        4          ✓ Pass       0.0004       ✓
input-03.txt         5x5        9          ✓ Pass       0.0012       ✓
input-04.txt         9x9        16         ✗ No Sol     0.0008       -
input-05.txt         11x11      36         ✓ Pass       0.0122       ✓
input-06.txt         7x7        7          ✓ Pass       0.0007       ✓
input-07.txt         9x9        25         ✓ Pass       0.0027       ✓
input-08.txt         11x11      36         ✓ Pass       0.0100       ✓
input-09.txt         13x13      24         ✗ No Sol     0.0011       -
input-10.txt         17x17      13         ✓ Pass       0.0006       ✓

================================================================================
Tổng: 10 tests
Có lời giải: 8 (80.0%)
Không có lời giải: 2 (20.0%)
Solution hợp lệ: 8/8
Tổng thời gian: 0.0768s
Trung bình: 0.0077s/test
================================================================================
```

## ⚡ Hiệu Năng

### So Sánh Tốc Độ (Dựa trên kết quả thực tế)

| Test Case | Kích thước | Số đảo | PySAT | A* | Backtracking | Brute Force |
|-----------|------------|--------|-------|-----|--------------|-------------|
| input-01.txt | 7x7 | 12 | 0.0471s | ~0.5s | ~1.2s | N/A |
| input-02.txt | 3x3 | 4 | 0.0004s | 0.001s | 0.003s | 0.05s |
| input-03.txt | 5x5 | 9 | 0.0012s | 0.0045s | 0.0011s | 0.4016s |
| input-04.txt | 9x9 | 16 | 0.0008s (UNSAT) | - | - | - |
| input-05.txt | 11x11 | 36 | 0.0122s | ~5s | ~20s | N/A |
| input-06.txt | 7x7 | 7 | 0.0007s | ~0.1s | ~0.3s | N/A |
| input-07.txt | 9x9 | 25 | 0.0027s | ~2s | ~8s | N/A |
| input-08.txt | 11x11 | 36 | 0.0100s | ~4s | ~15s | N/A |
| input-09.txt | 13x13 | 24 | 0.0011s (UNSAT) | - | - | - |
| input-10.txt | 17x17 | 13 | 0.0006s | ~0.2s | ~0.5s | N/A |

### Khuyến Nghị Sử Dụng

| Kích thước puzzle | Thuật toán nên dùng | Lý do |
|-------------------|---------------------|-------|
| ≤ 5x5 | PySAT, Backtracking hoặc A* | Tất cả đều nhanh |
| 7x7 - 9x9 | PySAT (khuyên dùng) | Nhanh và ổn định nhất |
| 11x11 - 13x13 | PySAT | Duy nhất giải nhanh |
| ≥ 17x17 | PySAT | Duy nhất khả thi |

**Lưu ý quan trọng**: 
- Brute Force chỉ dùng cho puzzle ≤ 5x5 với ít đảo
- Với input-03 (5x5, 9 đảo): Brute Force mất 0.4s và explore 46,159 nodes
- PySAT có thể phát hiện UNSAT rất nhanh (< 0.001s)

## 🔧 Xử Lý Sự Cố

### Lỗi: "No module named 'pysat'"

**Giải pháp**:
```bash
pip install python-sat
```

### Lỗi: "No input files found"

**Nguyên nhân**: Không tìm thấy file input

**Giải pháp**:
1. Kiểm tra thư mục `Source/Inputs/` có tồn tại không
2. Đảm bảo file có tên đúng format: `input-01.txt`, `input-02.txt`, ...
3. Chạy lại từ thư mục gốc của project

### Lỗi: "UNSAT detected"

**Nguyên nhân**: Puzzle không có lời giải

**Giải pháp**:
- Đây KHÔNG phải lỗi chương trình
- Puzzle được thiết kế không hợp lệ (vi phạm luật toán học)
- Kiểm tra lại input:
  - Tổng giá trị các đảo phải là số chẵn
  - Mỗi đảo phải có đủ láng giềng để nối cầu
  - Không có đảo cô lập

### Chương trình chạy quá lâu

**Nguyên nhân**: 
- Puzzle quá lớn
- Dùng thuật toán không phù hợp

**Giải pháp**:
1. Với puzzle > 11x11, CHỈ dùng PySAT
2. Tránh dùng Brute Force với puzzle > 7x7
3. Dùng Ctrl+C để dừng nếu cần

## 🎓 Giải Thích Thuật Ngữ

### CNF (Conjunctive Normal Form)
Dạng chuẩn hội của logic mệnh đề:
- Ví dụ: (A ∨ B) ∧ (¬C ∨ D) ∧ (¬A ∨ ¬B ∨ C)

### SAT (Boolean Satisfiability Problem)
Bài toán tìm giá trị True/False cho các biến sao cho công thức CNF đúng

### UNSAT (Unsatisfiable)
Không tồn tại lời giải thỏa mãn tất cả ràng buộc

### Heuristic Function
Hàm ước lượng chi phí từ trạng thái hiện tại đến đích

### MRV (Most Restricted Variable)
Chọn biến có ít lựa chọn nhất để gán giá trị trước

### Forward Checking
Kiểm tra ràng buộc sớm để loại bỏ nhánh không khả thi

## 📚 Tài Liệu Tham Khảo

1. **PySAT Documentation**: 
2. **Hashiwokakero Rules**: 
3. **A* Search Algorithm**: 
4. **CNF Conversion**: 

## 👥 Thành Viên

| MSSV | Họ và Tên | Email | Vai trò |
|------|-----------|-------|---------|
| 23122047 | TNguyễn Xuân Quang | 23122047@student.hcmus.edu.vn | Team Leader, PySAT |
| 23122050 | Nguyễn Tấn Tài | 23122050@student.hcmus.edu.vn | A* Algorithm |
| 23122051 | Đoàn Quang Thắng | 23122051@student.hcmus.edu.vn | Backtracking |
| 23122054 | Kpuih Thuing | 23122054@student.hcmus.edu.vn | Testing & Report |

## 📞 Liên Hệ

Nếu có thắc mắc, vui lòng liên hệ:
- Email: [email của nhóm]
- GitHub: [link repository nếu có]

## 📄 License

Đồ án môn học CSC14003 - Introduction to Artificial Intelligence
University of Science - VNUHCM

---

**Lưu ý**: Đây là đồ án học tập. Nghiêm cấm sao chép toàn bộ hoặc một phần mã nguồn để nộp bài cho các khóa học khác.