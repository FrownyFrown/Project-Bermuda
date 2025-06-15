from typing import List, Optional
from game.ship import Ship
from game.board import Board
from game.constants import get_attack_cooldown, get_ability_cooldown

class Player:
    def __init__(self, name: str, board_size: int):
        self.name = name
        self.board = Board(board_size)
        self.ships: List[Ship] = []
        self.cooldowns = {"attack": 0, "ability": 0}

    def add_ship(self, ship: Ship, pos: tuple, orientation: str) -> bool:
        success = self.board.place_ship(ship, pos, orientation)
        if success:
            self.ships.append(ship)
        return success

    def get_alive_ships(self) -> List[Ship]:
        return [s for s in self.ships if not s.is_destroyed()]

    def can_act(self, action_type: str) -> bool:
        return self.cooldowns[action_type] == 0

    def apply_cooldowns(self):
        self.cooldowns["attack"] = get_attack_cooldown(len(self.get_alive_ships()))
        self.cooldowns["ability"] = get_ability_cooldown(len(self.get_alive_ships()))

    def reduce_cooldowns(self):
        for k in self.cooldowns:
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1

    def choose_ship(self, index: int) -> Optional[Ship]:
        alive = self.get_alive_ships()
        if 0 <= index < len(alive):
            return alive[index]
        return None

    def is_defeated(self) -> bool:
        return all(s.is_destroyed() for s in self.ships)

    def show_own_board(self):
        print(f"[내 보드] {self.name}")
        self.board.print_board(reveal=True)

    def show_enemy_board(self, enemy_board: Board):
        print(f"[적 보드] {self.name}")
        enemy_board.print_board(reveal=False)
