# mac_engine.py

def compute_mac(pattern: list, filter_matrix: list) -> float:
    """
    2차원 패턴과 2차원 필터를 위치별로 곱해 모두 더하는 MAC 연산을 수행합니다.
    (NumPy 등 외부 라이브러리 없이 순수 반복문으로 직접 구현)
    """
    rows = len(pattern)
    cols = len(pattern[0])
    
    total_score = 0.0
    
    # 2중 반복문으로 위치별 곱셈 후 누적합 계산
    for r in range(rows):
        for c in range(cols):
            total_score += pattern[r][c] * filter_matrix[r][c]
            
    return total_score


def evaluate_decision(score_a: float, score_b: float, label_a: str = "Cross", label_b: str = "X", epsilon: float = 1e-9) -> str:
    """
    두 필터의 MAC 점수를 비교하여 판정 결과를 반환합니다.
    
    - 점수 차이가 epsilon(1e-9) 미만이면 동점 간주 -> 'UNDECIDED'
    - 점수가 더 높은 필터의 표준 라벨 반환
    """
    diff = abs(score_a - score_b)
    
    # 부동소수점 허용오차 기반 동점 처리
    if diff < epsilon:
        return "UNDECIDED"
    
    if score_a > score_b:
        return label_a
    else:
        return label_b


# --- 모듈 단독 테스트용 실행부 ---
if __name__ == "__main__":
    print("=== mac_engine.py 동작 검증 ===")
    
    # 3x3 테스트용 패턴 및 필터 데이터
    pattern_cross = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    
    filter_cross = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    
    filter_x = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    
    # 1. MAC 연산 계산
    score_a = compute_mac(pattern_cross, filter_cross)
    score_b = compute_mac(pattern_cross, filter_x)
    
    print(f"Cross 필터 점수: {score_a}")
    print(f"X 필터 점수    : {score_b}")
    
    # 2. 판정 검증
    decision = evaluate_decision(score_a, score_b, "Cross", "X")
    print(f"판정 결과      : {decision}")
    
    # 3. Epsilon 동점 처리 테스트
    print("\n--- 동점(UNDECIDED) 처리 테스트 ---")
    same_score_decision = evaluate_decision(0.9000000000000000, 0.8999999999999999, "Cross", "X")
    print(f"미세 오차 비교 결과: {same_score_decision}")