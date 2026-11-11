# mac_flat.py
import time
from mac_engine import compute_mac

def flatten_matrix(matrix_2d: list) -> list:
    """2차원 배열을 1차원 리스트(길이 N^2)로 변환(Flatten)합니다."""
    flat_list = []
    for row in matrix_2d:
        for val in row:
            flat_list.append(val)
    return flat_list


def compute_mac_flat(pattern_flat: list, filter_flat: list) -> float:
    """1차원 배열 단일 반복문 기반 MAC 연산을 수행합니다."""
    total_score = 0.0
    for i in range(len(pattern_flat)):
        total_score += pattern_flat[i] * filter_flat[i]
    return total_score


def compare_2d_and_1d_performance(pattern_2d: list, filter_2d: list, repeat_count: int = 100) -> dict:
    """2차원 연산과 1차원 최적화 연산의 실행 속도(ms)를 비교합니다."""
    # 1. 2차원 MAC 연산 시간 측정
    start_2d = time.perf_counter()
    for _ in range(repeat_count):
        _ = compute_mac(pattern_2d, filter_2d)
    time_2d_ms = ((time.perf_counter() - start_2d) * 1000) / repeat_count

    # 2. 1차원 변환 및 1차원 MAC 연산 시간 측정
    flat_pattern = flatten_matrix(pattern_2d)
    flat_filter = flatten_matrix(filter_2d)

    start_1d = time.perf_counter()
    for _ in range(repeat_count):
        _ = compute_mac_flat(flat_pattern, flat_filter)
    time_1d_ms = ((time.perf_counter() - start_1d) * 1000) / repeat_count

    # 개선율 계산
    improvement = ((time_2d_ms - time_1d_ms) / time_2d_ms) * 100 if time_2d_ms > 0 else 0.0

    return {
        "time_2d_ms": time_2d_ms,
        "time_1d_ms": time_1d_ms,
        "improvement_percent": improvement
    }