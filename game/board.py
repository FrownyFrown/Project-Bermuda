from typing import List, Tuple, Optional
from game.ship import Ship

class Board:
    def __init__(self, size: int):
        self.size = size  # 정사각형 맵 (5~8)
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.mines: List[Tuple[int, int]] = []

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def can_place_ship(self, ship: Ship, pos: Tuple[int, int], orientation: str) -> bool:
        ship.position = pos
        ship.orientation = orientation
        for x, y in ship.get_coordinates():
            if not self.is_within_bounds(x, y):
                return False
            if self.grid[y][x] is not None:
                return False
        return True

    def place_ship(self, ship: Ship, pos: Tuple[int, int], orientation: str) -> bool:
        if not self.can_place_ship(ship, pos, orientation):
            return False
        for x, y in ship.get_coordinates():
            self.grid[y][x] = ship
        self.ships.append(ship)
        return True

    def receive_attack(self, x: int, y: int) -> Optional[Ship]:
        if not self.is_within_bounds(x, y):
            return None
        target = self.grid[y][x]
        if isinstance(target, Ship):
            target.apply_damage(1)
            if target.is_destroyed():
                self.remove_ship(target)
            return target
        return None

    def place_mine(self, x: int, y: int) -> bool:
        if not self.is_within_bounds(x, y):
            return False
        if (x, y) in self.mines:
            return False
        self.mines.append((x, y))
        return True

    def check_mine_trigger(self, x: int, y: int) -> bool:
        return (x, y) in self.mines

    def remove_ship(self, ship: Ship):
        for x, y in ship.get_coordinates():
            if self.is_within_bounds(x, y) and self.grid[y][x] == ship:
                self.grid[y][x] = None
        self.ships.remove(ship)

    def print_board(self, reveal: bool = True):
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                cell = self.grid[y][x]
                if isinstance(cell, Ship):
                    row += cell.name[0] if reveal else "■"
                elif (x, y) in self.mines:
                    row += "M"
                else:
                    row += "."
            print(row)