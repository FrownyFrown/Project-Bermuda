from game.player import Player
from game.constants import ACTIONS
from game.actions import move_ship, rotate_ship, attack, use_ability

class GameEngine:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.turn = 0  # 0 or 1

    def get_current_player(self) -> Player:
        return self.players[self.turn % 2]

    def get_opponent_player(self) -> Player:
        return self.players[(self.turn + 1) % 2]

    def next_turn(self):
        self.turn += 1
        for player in self.players:
            player.reduce_cooldowns()

    def perform_action(self, player: Player, action: str, ship_index: int, **kwargs):
        if action not in ACTIONS:
            return "알 수 없는 명령입니다."

        ship = player.choose_ship(ship_index)
        if not ship:
            return "유효하지 않은 함선 선택입니다."

        if action == "MOVE":
            new_pos = kwargs.get("pos")
            return "이동 성공" if move_ship(ship, player.board, new_pos) else "이동 실패"

        elif action == "ROTATE":
            return "회전 성공" if rotate_ship(ship, player.board) else "회전 실패"

        elif action == "ATTACK":
            if not player.can_act("attack"):
                return "공격은 쿨타임 중입니다."
            x, y = kwargs.get("x"), kwargs.get("y")
            result = attack(self.get_opponent_player().board, x, y)
            player.apply_cooldowns()
            return "공격 성공" if result else "공격 실패"

        elif action == "ABILITY":
            if not player.can_act("ability"):
                return "스킬은 쿨타임 중입니다."
            result = use_ability(ship, self.get_opponent_player().board, **kwargs)
            player.apply_cooldowns()
            return result

        elif action == "SKIP":
            return "턴을 넘깁니다."

        return "명령 실행 실패"

    def is_game_over(self) -> bool:
        return any(player.is_defeated() for player in self.players)

    def get_winner(self) -> str:
        if self.players[0].is_defeated():
            return self.players[1].name
        elif self.players[1].is_defeated():
            return self.players[0].name
        return "무승부 또는 진행 중"
