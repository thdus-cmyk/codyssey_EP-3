# benchmark.py
import time
from mac_engine import compute_mac

def measure_mac_performance(pattern: list, filter_matrix: list, repeat_count: int = 10) -> dict:
    """
    I/O 시간은 제외하고 pure MAC 연산 함수 호출 시간만 ms 단위로 측정합니다.
    repeat_count(기본 10회) 만큼 반복 후 평균 시간을 반환합니다.
    """
    n = len(pattern)
    total_ops = n * n  # N x N 연산 횟수 (N^2)

    # 연산 시작 전 시간 기록
    start_time = time.perf_counter()
    
    for _ in range(repeat_count):
        _ = compute_mac(pattern, filter_matrix)
        
    end_time = time.perf_counter()

    # (초 단위 소요시간 -> ms 단위 변환) 후 10회 평균 계산
    total_duration_ms = (end_time - start_time) * 1000
    avg_time_ms = total_duration_ms / repeat_count

    return {
        "size_str": f"{n}×{n}",
        "avg_time_ms": avg_time_ms,
        "ops_count": total_ops
    }


def print_performance_table(benchmark_results: list):
    """
    성능 분석 결과를 예시 양식에 맞춰 콘솔 표 형태로 출력합니다.
    """
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수':<10}")
    print("-" * 40)
    
    for res in benchmark_results:
        print(f"{res['size_str']:<10} {res['avg_time_ms']:<15.3f} {res['ops_count']:<10}")


# --- 모듈 단독 테스트용 실행부 ---
if __name__ == "__main__":
    print("=== benchmark.py 동작 검증 ===")
    
    # 임의의 3x3 데이터로 측정 테스트
    dummy_pattern = [[1]*3 for _ in range(3)]
    dummy_filter = [[1]*3 for _ in range(3)]
    
    result = measure_mac_performance(dummy_pattern, dummy_filter, repeat_count=10)
    print_performance_table([result])