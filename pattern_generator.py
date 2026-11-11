# pattern_generator.py

def generate_cross_pattern(n: int) -> list:
    """크기 N을 입력받아 N x N Cross(십자가) 패턴 2차원 배열을 생성합니다."""
    mid = n // 2
    matrix = []
    for r in range(n):
        row = []
        for c in range(n):
            if r == mid or c == mid:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)
    return matrix


def generate_x_pattern(n: int) -> list:
    """크기 N을 입력받아 N x N X 패턴 2차원 배열을 생성합니다."""
    matrix = []
    for r in range(n):
        row = []
        for c in range(n):
            if r == c or r + c == n - 1:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)
    return matrix