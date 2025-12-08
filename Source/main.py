import argparse
import os
import sys
import time
from pathlib import Path

# Import các modules
from helper_01 import HashiwokakeroGame
from helper_02 import PySATSolver


def solve_single(input_file: str, solver_type: str, output_file: str = None):
    """Giải một puzzle với solver được chỉ định"""
    print("="*80)
    print(f"SOLVING: {input_file}")
    print(f"SOLVER: {solver_type.upper()}")
    print("="*80)
    
    # Đọc game
    try:
        game = HashiwokakeroGame(input_file)
        print(f"Grid: {game.rows}x{game.cols}")
        print(f"Islands: {len(game.islands)}")
        print()
    except Exception as e:
        print(f"✗ Lỗi khi đọc file: {e}")
        return None
    
    # Xác định output file
    if not output_file:
        input_path = Path(input_file)
        output_filename = input_path.name.replace("input-", "output-")
        if output_filename == input_path.name:
            output_filename = f"output-{input_path.name}"
        output_file = os.path.join("Source/Outputs", output_filename)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Chọn solver
    solution = None
    time_taken = 0
    
    try:
        if solver_type == 'pysat':
            solver = PySATSolver(game)
            solution, time_taken = solver.solve()
        elif solver_type == 'astar':
            from astar_solver import AStarSolver
            solver = AStarSolver(game)
            solution, time_taken = solver.solve()
        elif solver_type == 'backtrack':
            from backtrack_solver import BacktrackingSolver
            solver = BacktrackingSolver(game)
            solution, time_taken = solver.solve()
        elif solver_type == 'bruteforce':
            from bruteforce_solver import OptimizedBruteForceSolver
            if len(game.islands) > 10:
                print("⚠ Puzzle quá lớn cho Brute Force (>10 đảo). Dùng PySAT...")
                solver = PySATSolver(game)
            else:
                solver = OptimizedBruteForceSolver(game)
            solution, time_taken = solver.solve()
        else:
            print(f"✗ Solver không hợp lệ: {solver_type}")
            return None
    except ImportError as e:
        print(f"⚠ Solver {solver_type} chưa import được: {e}")
        return None
    except Exception as e:
        print(f"✗ Lỗi khi giải: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # Xử lý kết quả
    if solution:
        print("\n" + "="*80)
        print("SOLUTION")
        print("="*80)
        game.display_solution(solution)
        
        is_valid, errors = game.validate_solution(solution)
        if is_valid:
            print("\n✓ Solution hợp lệ!")
        else:
            print("\n✗ Solution không hợp lệ:")
            for error in errors:
                print(f"  - {error}")
        
        try:
            game.save_solution(solution, output_file)
            print(f"\n✓ Đã lưu solution vào: {output_file}")
        except Exception as e:
            print(f"\n✗ Lỗi khi lưu output: {e}")
        
        print(f"\n⏱ Thời gian: {time_taken:.4f}s")
        if hasattr(solver, 'nodes_explored'):
            print(f"🔍 Nodes explored: {solver.nodes_explored:,}")
        
        return solution
    else:
        print("\n" + "!"*80)
        print("KẾT QUẢ: Map này KHÔNG CÓ LỜI GIẢI (UNSAT)")
        print("!"*80)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("NO SOLUTION\n")
                f.write("(Map này không có lời giải)")
            print(f"\n✓ Đã lưu thông báo 'NO SOLUTION' vào: {output_file}")
        except:
            pass
        print(f"\n⏱ Thời gian kiểm tra: {time_taken:.4f}s")
        return None


def benchmark_all():
    """Chạy benchmark trên TẤT CẢ test cases (FIXED - NO DUPLICATES)"""
    print("="*80)
    print("BENCHMARK - CHẠY TẤT CẢ TEST CASES")
    print("="*80)
    
    # TÌM FILE MỘT LẦN DUY NHẤT
    files = find_input_files()
    if not files:
        print("✗ Không tìm thấy file input nào!")
        return

    print(f"Tìm thấy {len(files)} test cases.\n")
    
    # Tạo output directory
    outputs_dir = Path("Source/Outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    results = []
    
    # CHẠY TỪNG FILE MỘT LẦN
    for idx, input_file in enumerate(files, 1):
        print(f"\n{'='*80}")
        print(f"Test {idx}/{len(files)}: {input_file.name}")
        print(f"{'='*80}")
        
        output_filename = input_file.name.replace("input-", "output-")
        output_file = outputs_dir / output_filename
        
        try:
            # Load game
            game = HashiwokakeroGame(str(input_file))
            print(f"Size: {game.rows}x{game.cols}, Islands: {len(game.islands)}")
            
            # Solve with PySAT
            solver = PySATSolver(game)
            solution, time_taken = solver.solve()
            
            # Store result
            result = {
                'file': input_file.name,
                'size': f"{game.rows}x{game.cols}",
                'islands': len(game.islands),
                'success': solution is not None,
                'time': time_taken
            }
            
            if solution:
                is_valid, errors = game.validate_solution(solution)
                result['valid'] = is_valid
                
                if not is_valid:
                    print(f"⚠️ WARNING: Solution không hợp lệ!")
                    for err in errors[:3]:  # In 3 lỗi đầu
                        print(f"   - {err}")
                
                game.save_solution(solution, str(output_file))
                print(f"✓ Đã lưu: {output_file}")
            else:
                result['valid'] = False
                print("➤ KHÔNG CÓ LỜI GIẢI.")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("NO SOLUTION\n")
                    f.write("(Map này không có lời giải)")
            
            results.append(result)
            
        except Exception as e:
            print(f"✗ Lỗi: {e}")
            import traceback
            traceback.print_exc()
            
            results.append({
                'file': input_file.name,
                'size': 'N/A',
                'islands': 0,
                'success': False,
                'time': 0,
                'valid': False
            })
    
    # In tổng kết
    print("\n" + "="*80)
    print("TỔNG KẾT BENCHMARK")
    print("="*80)
    print(f"{'File':<20} {'Size':<10} {'Islands':<10} {'Status':<12} {'Time (s)':<12} {'Valid':<8}")
    print("-"*80)
    
    for r in results:
        status = "✓ Pass" if r['success'] else "✗ No Sol"
        valid = "✓" if r.get('valid', False) else "-"
        time_str = f"{r['time']:.4f}" if r['time'] > 0 else "N/A"
        print(f"{r['file']:<20} {r['size']:<10} {r['islands']:<10} {status:<12} {time_str:<12} {valid:<8}")
    
    # Statistics
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    valid_count = sum(1 for r in results if r.get('valid', False))
    
    print("\n" + "="*80)
    print(f"Tổng: {total} tests")
    print(f"Có lời giải: {passed} ({passed/total*100:.1f}%)")
    print(f"Không có lời giải: {total - passed} ({(total-passed)/total*100:.1f}%)")
    print(f"Solution hợp lệ: {valid_count}/{passed}")
    
    # Tổng thời gian
    total_time = sum(r['time'] for r in results)
    print(f"Tổng thời gian: {total_time:.4f}s")
    print(f"Trung bình: {total_time/total:.4f}s/test")
    print("="*80)


def compare_solvers(input_file: str):
    """So sánh các solvers (Cập nhật: Dừng nếu PySAT UNSAT)"""
    print("="*80)
    print(f"SO SÁNH SOLVERS - {Path(input_file).name}")
    print("="*80)
    
    try:
        game = HashiwokakeroGame(input_file)
        print(f"Grid: {game.rows}x{game.cols}, Islands: {len(game.islands)}\n")
    except Exception as e:
        print(f"✗ Lỗi khi load game: {e}")
        return
    
    # Danh sách solvers
    # LƯU Ý: PySAT phải luôn nằm đầu tiên để kiểm tra tính khả thi
    solvers = [('pysat', PySATSolver)]
    
    try:
        from astar_solver import AStarSolver
        solvers.append(('astar', AStarSolver))
    except ImportError:
        print("⚠️ A* Solver không có")
    
    try:
        from backtrack_solver import BacktrackingSolver
        solvers.append(('backtrack', BacktrackingSolver))
    except ImportError:
        print("⚠️ Backtracking Solver không có")
    
    try:
        from bruteforce_solver import OptimizedBruteForceSolver
        if len(game.islands) <= 10:
            solvers.append(('bruteforce', OptimizedBruteForceSolver))
        else:
            print(f"⚠️ Brute Force bỏ qua (quá nhiều đảo: {len(game.islands)})")
    except ImportError:
        print("⚠️ Brute Force Solver không có")
    
    # Test từng solver
    results = {}
    pysat_unsat = False  # Cờ đánh dấu nếu PySAT không tìm thấy lời giải

    for name, SolverClass in solvers:
        # Nếu PySAT đã xác định UNSAT thì bỏ qua các thuật toán còn lại
        if pysat_unsat:
            print(f"\n➤ {name.upper()}: SKIPPED (Do PySAT xác định UNSAT)")
            results[name] = {
                'success': False,
                'time': 0,
                'valid': False,
                'nodes': 0
            }
            continue

        print(f"\n--- Testing {name.upper()} ---")
        try:
            solver = SolverClass(game)
            solution, time_taken = solver.solve()
            
            is_valid = False
            if solution:
                is_valid, errors = game.validate_solution(solution)
                if not is_valid:
                    print(f"⚠️ Solution không hợp lệ:")
                    for err in errors[:3]:
                        print(f"   - {err}")
            
            results[name] = {
                'success': solution is not None,
                'time': time_taken,
                'valid': is_valid,
                'nodes': getattr(solver, 'nodes_explored', 0)
            }
            
            if not solution:
                print(f"➤ {name.upper()}: KHÔNG CÓ LỜI GIẢI.")
                # Logic mới thêm vào ở đây:
                if name == 'pysat':
                    print("🛑 PySAT xác định map này VÔ NGHIỆM (UNSAT).")
                    print("   ➜ Dừng so sánh các thuật toán khác để tiết kiệm thời gian.")
                    pysat_unsat = True  # Bật cờ để skip các vòng lặp sau
                
        except Exception as e:
            print(f"✗ Lỗi: {e}")
            import traceback
            traceback.print_exc()
            results[name] = {
                'success': False,
                'time': 0,
                'valid': False,
                'nodes': 0
            }

    # In kết quả
    print("\n" + "="*80)
    print("KẾT QUẢ SO SÁNH")
    print("="*80)
    print(f"{'Solver':<15} {'Status':<12} {'Valid':<8} {'Time (s)':<12} {'Nodes':<15} {'Speedup':<10}")
    print("-"*80)
    
    base_time = results.get('pysat', {}).get('time', 1)
    if base_time == 0:
        base_time = 0.0001  # Tránh chia 0
    
    for name, res in results.items():
        if res.get('success'):
            status = "✓ Pass"
        else:
            # Phân biệt giữa không giải được và bị Skip
            if name != 'pysat' and pysat_unsat and res['time'] == 0:
                status = "⏹ Skipped"
            else:
                status = "✗ No Sol"

        valid = "✓" if res['valid'] else "-"
        time_str = f"{res['time']:.4f}" if res['time'] > 0 else "0.0000"
        nodes_str = f"{res['nodes']:,}" if res['nodes'] > 0 else "-"
        
        if res['time'] > 0:
            speedup = f"{base_time/res['time']:.2f}x"
        else:
            speedup = "-"
        
        print(f"{name.upper():<15} {status:<12} {valid:<8} {time_str:<12} {nodes_str:<15} {speedup:<10}")
    
    print("="*80)


# =============================================================================
# CÁC HÀM HỖ TRỢ MENU TƯƠNG TÁC
# =============================================================================

def find_input_files():
    """
    Tìm tất cả file input (KHÔNG TRÙNG LẶP)
    """
    # Ưu tiên thư mục theo thứ tự
    possible_dirs = [
        Path("Source/Inputs"),
        Path("Inputs"),
        Path(".")
    ]
    
    for d in possible_dirs:
        if d.exists():
            files = sorted(list(d.glob("input-*.txt")))
            if files:
                print(f"📁 Found {len(files)} input files in: {d}")
                return files
    
    print("✗ No input files found!")
    return []


def select_file_menu():
    """Menu chọn file"""
    files = find_input_files()
    if not files:
        print("✗ Không tìm thấy file input nào!")
        return None
    
    print("\n--- CHỌN FILE INPUT ---")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f.name}")
    print("  0. Quay lại")
    
    while True:
        try:
            choice = input(f"Chọn file [1-{len(files)}]: ").strip()
            if not choice:
                continue
            choice = int(choice)
            if choice == 0:
                return None
            if 1 <= choice <= len(files):
                return str(files[choice-1])
            print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Vui lòng nhập số.")
        except KeyboardInterrupt:
            print("\n")
            return None


def select_solver_menu():
    """Menu chọn solver"""
    solvers = [
        ('1', 'pysat', 'PySAT (Khuyên dùng)'),
        ('2', 'astar', 'A* Search'),
        ('3', 'backtrack', 'Backtracking'),
        ('4', 'bruteforce', 'Brute Force (Chỉ map nhỏ)')
    ]
    print("\n--- CHỌN THUẬT TOÁN ---")
    for k, v, desc in solvers:
        print(f"  {k}. {desc}")
    
    while True:
        choice = input("Chọn thuật toán [1]: ").strip()
        if not choice:
            return 'pysat'  # Default
        for k, v, _ in solvers:
            if choice == k:
                return v
        print("Lựa chọn không hợp lệ.")


def interactive_mode():
    """Chế độ tương tác dùng MENU Số"""
    while True:
        print("\n" + "="*50)
        print("   HASHIWOKAKERO SOLVER - MENU CHÍNH")
        print("="*50)
        print("  1. Giải Puzzle (Solve)")
        print("  2. Chạy Benchmark (Tất cả)")
        print("  3. So sánh Solvers (Compare)")
        print("  4. Thoát (Exit)")
        print("-" * 50)
        
        try:
            choice = input("Mời chọn chức năng [1-4]: ").strip()
            
            if choice == '1':  # Solve
                f = select_file_menu()
                if f:
                    s = select_solver_menu()
                    solve_single(f, s)
                    input("\nẤn Enter để tiếp tục...")
                    
            elif choice == '2':  # Benchmark
                benchmark_all()
                input("\nẤn Enter để tiếp tục...")
                
            elif choice == '3':  # Compare
                f = select_file_menu()
                if f:
                    compare_solvers(f)
                    input("\nẤn Enter để tiếp tục...")
                    
            elif choice == '4':  # Exit
                print("\nTạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ, vui lòng thử lại.")
        except KeyboardInterrupt:
            print("\n\nTạm biệt!")
            break
        except Exception as e:
            print(f"\n✗ Lỗi: {e}")
            import traceback
            traceback.print_exc()
            input("\nẤn Enter để tiếp tục...")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description='Hashiwokakero Solver - AI Project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode
  python main.py -i                                 # Interactive mode
  python main.py --benchmark                        # Run all tests
  python main.py --input input-01.txt               # Solve with PySAT
  python main.py --input input-01.txt --solver astar  # Solve with A*
  python main.py --compare --input input-01.txt     # Compare all solvers
        """
    )
    
    parser.add_argument('--solver', default='pysat',
                        choices=['pysat', 'astar', 'backtrack', 'bruteforce'],
                        help='Solver algorithm to use (default: pysat)')
    parser.add_argument('--input', type=str,
                        help='Input file path')
    parser.add_argument('--output', type=str,
                        help='Output file path (optional)')
    parser.add_argument('--benchmark', action='store_true',
                        help='Run benchmark on all test cases')
    parser.add_argument('--compare', action='store_true',
                        help='Compare all solvers on given input')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode with menu')
    
    args = parser.parse_args()
    
    # Tạo output directory
    os.makedirs("Source/Outputs", exist_ok=True)
    
    try:
        if args.interactive:
            interactive_mode()
        elif args.benchmark:
            benchmark_all()
        elif args.compare and args.input:
            compare_solvers(args.input)
        elif args.input:
            solve_single(args.input, args.solver, args.output)
        else:
            # Mặc định vào chế độ interactive nếu không có tham số
            print("💡 Tip: Dùng -h để xem các options")
            interactive_mode()
    except KeyboardInterrupt:
        print("\n\nĐã dừng chương trình.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Lỗi nghiêm trọng: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()