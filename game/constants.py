# 게임 전역 상수

# 좌표계 관련
ALPHABETS = ["A", "B", "C", "D", "E", "F", "G", "H"]  # 최대 8x8 대응

# 맵 크기별 설정 (함선 수, 전력치 총합 제한)
MAP_CONFIG = {
    5: {"ship_limit": 2, "power_limit": 6},
    6: {"ship_limit": 3, "power_limit": 9},
    7: {"ship_limit": 3, "power_limit": 10},
    8: {"ship_limit": 4, "power_limit": 12},
}

# 쿨타임 계산 방식
# 공격, 능력은 각각 1척당 1턴 쿨다운. 단, 남은 함선 1척일 때는 쿨타임 없음

def get_ability_cooldown(ships_remaining: int) -> int:
    return 0 if ships_remaining == 1 else ships_remaining

def get_attack_cooldown(ships_remaining: int) -> int:
    return 0 if ships_remaining == 1 else ships_remaining

# 기본 행동 종류
ACTIONS = ["MOVE", "ROTATE", "ATTACK", "ABILITY", "SKIP"]
