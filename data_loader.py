# data_loader.py
import json
from normalizer import normalize_label

def get_user_matrix(name: str, rows: int = 3, cols: int = 3) -> list:
    """
    모드 1용: 사용자로부터 N*N 크기의 행렬을 입력받습니다.
    잘못된 입력(숫자 파싱 실패, 개수 불일치 등) 발생 시 안내 문구를 출력하고 재입력을 유도합니다.
    """
    print(f"\n{name} ({rows}줄 입력, 공백 구분)")
    
    while True:
        matrix = []
        is_valid = True
        
        for i in range(rows):
            try:
                line = input().strip()
                tokens = line.split()
                
                # 열 개수 검증
                if len(tokens) != cols:
                    print(f"입력 형식 오류: 각 줄에 {cols}개의 숫자를 공백으로 구분해 입력하세요.")
                    is_valid = False
                    break
                
                # 숫자(float/int) 변환 검증
                row_values = [float(x) for x in tokens]
                matrix.append(row_values)
                
            except ValueError:
                print("입력 형식 오류: 숫자만 입력 가능합니다. 다시 입력해주세요.")
                is_valid = False
                break
                
        if is_valid and len(matrix) == rows:
            return matrix
        
        print(f"\n[{name}] 입력을 처음부터 다시 시도합니다.")


def load_json_data(filepath: str = "data.json") -> dict:
    """
    모드 2용: data.json 파일을 로드하여 라벨 정규화를 적용하고 반환합니다.
    파일 읽기 실패 시 에러 안내와 함께 빈 객체를 반환하여 프로그램 비정상 종료를 방지합니다.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"오류: {filepath} 파일을 찾을 수 없습니다.")
        return {}
    except json.JSONDecodeError:
        print(f"오류: {filepath} 파일의 JSON 형식이 올바르지 않습니다.")
        return {}


# --- 모듈 단독 테스트용 실행부 ---
if __name__ == "__main__":
    print("=== data_loader.py 모드 1 입력 검증 테스트 ===")
    print("(올바른 입력 예시: 0 1 0 입력 후 엔터)")
    # 테스트용으로 2x2 입력 받기 예시
    # test_matrix = get_user_matrix("테스트 필터", rows=2, cols=2)
    # print("입력받은 행렬:", test_matrix)