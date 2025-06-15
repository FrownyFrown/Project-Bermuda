from typing import Tuple, Optional
from game.ship import Ship
from game.board import Board


def move_ship(ship: Ship, board: Board, new_pos: Tuple[int, int]) -> bool:
    """함선을 새 위치로 이동시킴"""
    # 기존 위치 제거
    for x, y in ship.get_coordinates():
        board.grid[y][x] = None

    old_pos = ship.position
    ship.position = new_pos
    if board.can_place_ship(ship, new_pos, ship.orientation):
        for x, y in ship.get_coordinates():
            board.grid[y][x] = ship
        return True
    else:
        ship.position = old_pos  # 복구
        for x, y in ship.get_coordinates():
            board.grid[y][x] = ship
        return False


def rotate_ship(ship: Ship, board: Board) -> bool:
    """함선을 회전시킴"""
    # 기존 위치 제거
    for x, y in ship.get_coordinates():
        board.grid[y][x] = None

    old_orientation = ship.orientation
    ship.rotate()
    if board.can_place_ship(ship, ship.position, ship.orientation):
        for x, y in ship.get_coordinates():
            board.grid[y][x] = ship
        return True
    else:
        ship.orientation = old_orientation  # 복구
        for x, y in ship.get_coordinates():
            board.grid[y][x] = ship
        return False


def attack(board: Board, x: int, y: int) -> Optional[Ship]:
    """해당 좌표에 공격"""
    return board.receive_attack(x, y)


def use_ability(ship: Ship, board: Board, **kwargs) -> str:
    """스킬 사용 - 능력마다 분기 처리 예정"""
    # 예시로 수뢰 설치만 구현
    if ship.ability == "수뢰 설치":
        x, y = kwargs.get("x"), kwargs.get("y")
        if board.place_mine(x, y):
            return "수뢰 설치 완료"
        else:
            return "수뢰 설치 실패"
    elif ship.ability == "속사포":
        targets = kwargs.get("targets", [])  # [(x1, y1), (x2, y2)]
        result = []
        for tx, ty in targets:
            hit = board.receive_attack(tx, ty)
            result.append((tx, ty, bool(hit)))
        return f"속사포 결과: {result}"
    else:
        return "능력 미구현 또는 없음"
