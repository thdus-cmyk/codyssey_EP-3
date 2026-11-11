# normalizer.py

def normalize_label(raw_label: str) -> str:
    """
    입력받은 다양한 형태의 라벨을 표준 라벨('Cross' 또는 'X')로 정규화합니다.
    
    - '+' 또는 'cross' (대소문자 구분 없음) -> 'Cross'
    - 'x' (대소문자 구분 없음) -> 'X'
    """
    if not isinstance(raw_label, str):
        return raw_label

    # 공백 제거 후 소문자로 통일
    cleaned = raw_label.strip().lower()

    if cleaned in ['+', 'cross']:
        return 'Cross'
    elif cleaned == 'x':
        return 'X'
    else:
        # 정규화 규칙에 없는 입력은 원본 그대로 반환
        return raw_label


# --- 모듈 단독 테스트용 실행부 ---
if __name__ == "__main__":
    test_cases = ['+', 'x', 'cross', 'Cross', 'X', '+ ', '  x  ']
    print("=== normalizer.py 동작 검증 ===")
    for item in test_cases:
        result = normalize_label(item)
        print(f"입력: {repr(item):10} -> 정규화: {result}")
        