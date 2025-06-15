import json
from typing import Tuple, List

class Ship:
    def __init__(self, 
                 name: str,
                 size: Tuple[int, int],
                 hp: int,
                 attack: int,
                 mobility: int,
                 ability: str = None,
                 ship_type: str = "기본형",
                 power: int = 0):
        self.name = name
        self.size = size  # (width, height)
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.mobility = mobility
        self.ability = ability
        self.ship_type = ship_type
        self.power = power
        self.position = None  # 시작 좌표 (x, y)
        self.orientation = "H"  # "H" 수평 / "V" 수직
        self.cooldowns = {"attack": 0, "ability": 0}

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """함선이 차지하는 좌표 리스트 반환"""
        coords = []
        width, height = self.size
        x, y = self.position
        if self.orientation == "H":
            for dx in range(width):
                for dy in range(height):
                    coords.append((x + dx, y + dy))
        else:
            for dx in range(height):
                for dy in range(width):
                    coords.append((x + dy, y + dx))
        return coords

    def rotate(self):
        """90도 회전"""
        self.orientation = "V" if self.orientation == "H" else "H"

    def is_destroyed(self) -> bool:
        return self.current_hp <= 0

    def apply_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def reset_cooldowns(self):
        self.cooldowns = {"attack": 0, "ability": 0}


def load_ships_from_json(filepath: str) -> List[Ship]:
    ships = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            ship = Ship(
                name=item["name"],
                size=tuple(item["size"]),
                hp=item["hp"],
                attack=item["attack"],
                mobility=item["mobility"],
                ability=item.get("ability"),
                ship_type=item.get("type", "기본형"),
                power=item.get("power", 0)
            )
            ships.append(ship)
    return ships
