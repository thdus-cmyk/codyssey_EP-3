# main.py
import sys
from normalizer import normalize_label
from mac_engine import compute_mac, evaluate_decision
from benchmark import measure_mac_performance, print_performance_table
from data_loader import get_user_matrix, load_json_data
from pattern_generator import generate_cross_pattern, generate_x_pattern
from mac_flat import compare_2d_and_1d_performance

def run_mode_1():
    """모드 1: 사용자 직접 입력 (3x3)"""
    print("\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    filter_a = get_user_matrix("필터 A", rows=3, cols=3)
    filter_b = get_user_matrix("필터 B", rows=3, cols=3)

    print("\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    pattern = get_user_matrix("패턴", rows=3, cols=3)

    score_a = compute_mac(pattern, filter_a)
    score_b = compute_mac(pattern, filter_b)
    
    perf = measure_mac_performance(pattern, filter_a, repeat_count=10)
    decision = evaluate_decision(score_a, score_b, "A", "B")

    print("\n#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {perf['avg_time_ms']:.3f} ms")
    
    if decision == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print(f"판정: {decision}")


def run_mode_2():
    """모드 2: data.json 일괄 분석"""
    data = load_json_data("data.json")
    if not data:
        print("data.json 읽기에 실패하여 모드 2를 종료합니다.")
        return

    filters_dict = data.get("filters", {})
    patterns_dict = data.get("patterns", {})

    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    for key in filters_dict.keys():
        print(f"✓ {key:<7} 필터 로드 완료 (Cross, X)")

    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    
    total_count = 0
    pass_count = 0
    fail_cases = []
    benchmark_map = {}

    for pattern_key, p_info in patterns_dict.items():
        total_count += 1
        raw_input = p_info.get("input", [])
        expected_raw = p_info.get("expected", "")
        expected_norm = normalize_label(expected_raw)

        size_key = "_".join(pattern_key.split("_")[:2])
        print(f"\n--- {pattern_key} ---")
        
        if size_key not in filters_dict:
            print(f"FAIL (원인: {size_key} 필터 없음)")
            fail_cases.append((pattern_key, "필터 스키마 부재"))
            continue

        cross_filter = filters_dict[size_key].get("cross", [])
        x_filter = filters_dict[size_key].get("x", [])

        score_cross = compute_mac(raw_input, cross_filter)
        score_x = compute_mac(raw_input, x_filter)

        decision = evaluate_decision(score_cross, score_x, "Cross", "X")
        is_pass = (decision == expected_norm)
        result_str = "PASS" if is_pass else "FAIL"

        if is_pass:
            pass_count += 1
        else:
            if decision == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                reason = f"판정 불일치 (기대: {expected_norm}, 결과: {decision})"
            fail_cases.append((pattern_key, reason))

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {decision} | expected: {expected_norm} | {result_str}")

        if size_key not in benchmark_map:
            perf = measure_mac_performance(raw_input, cross_filter, repeat_count=10)
            benchmark_map[size_key] = perf

    benchmark_list = list(benchmark_map.values())
    print_performance_table(benchmark_list)

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {total_count - pass_count}개")

    if fail_cases:
        print("\n실패 케이스:")
        for key, reason in fail_cases:
            print(f"- {key}: {reason}")


def run_mode_3():
    """모드 3 (보너스): Cross/X 패턴 자동 생성기"""
    print("\n#---------------------------------------")
    print("# [보너스] N×N 패턴 자동 생성기")
    print("#---------------------------------------")
    try:
        n = int(input("생성할 패턴 크기 N 입력 (예: 5): ").strip())
        if n < 3:
            print("크기는 최소 3 이상이어야 합니다.")
            return

        print(f"\n[{n}×{n} Cross 패턴]")
        cross_p = generate_cross_pattern(n)
        for r in cross_p:
            print(" ".join(str(int(x)) for x in r))

        print(f"\n[{n}×{n} X 패턴]")
        x_p = generate_x_pattern(n)
        for r in x_p:
            print(" ".join(str(int(x)) for x in r))

    except ValueError:
        print("숫자만 입력해 주세요.")


def run_mode_4():
    """모드 4 (보너스): 1차원 배열 최적화 성능 비교"""
    print("\n#---------------------------------------")
    print("# [보너스] 1차원 배열 최적화 성능 비교")
    print("#---------------------------------------")
    sizes = [3, 5, 13, 25]
    print(f"{'크기':<10} {'2차원 연산(ms)':<15} {'1차원 연산(ms)':<15} {'속도 개선율':<10}")
    print("-" * 55)

    for n in sizes:
        p = generate_cross_pattern(n)
        f = generate_cross_pattern(n)
        res = compare_2d_and_1d_performance(p, f, repeat_count=100)
        print(f"{n:<2}×{n:<7} {res['time_2d_ms']:<15.5f} {res['time_1d_ms']:<15.5f} {res['improvement_percent']:.1f}%")


def main():
    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. (보너스) N×N 패턴 자동 생성")
    print("4. (보너스) 1차원 배열 최적화 성능 비교")
    
    choice = input("선택: ").strip()
    
    if choice == "1":
        run_mode_1()
    elif choice == "2":
        run_mode_2()
    elif choice == "3":
        run_mode_3()
    elif choice == "4":
        run_mode_4()
    else:
        print("잘못된 선택입니다. 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()