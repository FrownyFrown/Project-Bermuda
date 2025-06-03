import random
import os
import time

class BattleshipGame:
    def __init__(self):
        self.board_size = 10
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_view = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = {
            '항공모함': 5,
            '전함': 4,
            '구축함': 3,
            '잠수함': 3,
            '순양함': 2
        }
        self.player_ships = {}
        self.computer_ships = {}
        self.player_hits = 0
        self.computer_hits = 0
        self.total_ship_cells = sum(self.ships.values())

    def clear_screen(self):
        """화면을 지웁니다."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_boards(self):
        """플레이어와 컴퓨터의 게임 보드를 출력합니다."""
        self.clear_screen()
        print("\n" + "=" * 50)
        print("        당신의 보드                상대방의 보드")
        print("   A B C D E F G H I J         A B C D E F G H I J")

        for i in range(self.board_size):
            player_row = f"{i} |"
            for j in range(self.board_size):
                player_row += f"{self.player_board[i][j]}|"

            computer_row = f"{i} |"
            for j in range(self.board_size):
                computer_row += f"{self.computer_view[i][j]}|"

            print(f"{player_row}       {computer_row}")
        print("=" * 50 + "\n")

    def place_ship(self, board, ship_name, ship_size):
        """보드에 배를 배치합니다."""
        while True:
            # 가로 또는 세로 방향을 무작위로 선택
            is_horizontal = random.choice([True, False])

            # 배의 시작점 선택
            if is_horizontal:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - ship_size)
            else:
                row = random.randint(0, self.board_size - ship_size)
                col = random.randint(0, self.board_size - 1)

            # 배치 가능한지 확인
            can_place = True
            positions = []

            for i in range(ship_size):
                r = row if is_horizontal else row + i
                c = col + i if is_horizontal else col

                # 이미 다른 배가 있는지 확인
                if board[r][c] != ' ':
                    can_place = False
                    break

                positions.append((r, c))

            # 배치 가능하면 배를 배치
            if can_place:
                for r, c in positions:
                    board[r][c] = 'O'
                return positions

    def setup_game(self):
        """게임 설정을 초기화합니다."""
        # 플레이어 배 랜덤 배치
        for ship_name, ship_size in self.ships.items():
            positions = self.place_ship(self.player_board, ship_name, ship_size)
            self.player_ships[ship_name] = positions

        # 컴퓨터 배 랜덤 배치
        for ship_name, ship_size in self.ships.items():
            positions = self.place_ship(self.computer_board, ship_name, ship_size)
            self.computer_ships[ship_name] = positions

    def player_turn(self):
        """플레이어의 턴을 처리합니다."""
        while True:
            try:
                print("공격할 좌표를 입력하세요 (예: A3 또는 a3): ")
                coord = input().strip().upper()

                if len(coord) < 2 or len(coord) > 3:
                    print("잘못된 형식입니다. 다시 시도하세요.")
                    continue

                col = ord(coord[0]) - ord('A')
                row = int(coord[1:])

                if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
                    print(f"좌표는 A0-J9 사이여야 합니다.")
                    continue

                if self.computer_view[row][col] != ' ':
                    print("이미 공격한 위치입니다. 다시 시도하세요.")
                    continue

                break
            except ValueError:
                print("잘못된 형식입니다. 다시 시도하세요.")

        # 공격 처리
        if self.computer_board[row][col] == 'O':
            print("명중!")
            self.computer_view[row][col] = 'X'
            self.player_hits += 1

            # 배가 침몰했는지 확인
            ship_hit = None
            for ship_name, positions in self.computer_ships.items():
                if (row, col) in positions:
                    ship_hit = ship_name
                    positions.remove((row, col))
                    if not positions:
                        print(f"적의 {ship_hit}을(를) 침몰시켰습니다!")
                    break
        else:
            print("실패!")
            self.computer_view[row][col] = '.'

        time.sleep(2)

    def computer_turn(self):
        """컴퓨터의 턴을 처리합니다."""
        print("\n컴퓨터의 차례입니다...")
        time.sleep(1)

        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.player_board[row][col] not in ['X', '.']:
                break

        # 공격 처리
        col_letter = chr(col + ord('A'))
        print(f"컴퓨터가 {col_letter}{row}을(를) 공격합니다.")
        time.sleep(1)

        if self.player_board[row][col] == 'O':
            print("컴퓨터가 명중시켰습니다!")
            self.player_board[row][col] = 'X'
            self.computer_hits += 1

            # 배가 침몰했는지 확인
            ship_hit = None
            for ship_name, positions in self.player_ships.items():
                if (row, col) in positions:
                    ship_hit = ship_name
                    positions.remove((row, col))
                    if not positions:
                        print(f"당신의 {ship_hit}이(가) 침몰했습니다!")
                    break
        else:
            print("컴퓨터가 빗나갔습니다!")
            self.player_board[row][col] = '.'

        time.sleep(2)

    def check_game_over(self):
        """게임이 끝났는지 확인합니다."""
        if self.player_hits == self.total_ship_cells:
            self.print_boards()
            print("축하합니다! 당신이 승리했습니다!")
            return True

        if self.computer_hits == self.total_ship_cells:
            self.print_boards()
            print("아쉽습니다! 컴퓨터가 승리했습니다.")
            return True

        return False

    def play(self):
        """게임 메인 루프를 실행합니다."""
        print("배틀쉽 게임에 오신 것을 환영합니다!")
        print("당신과 컴퓨터는 각각 다음 배들을 가지고 있습니다:")
        for ship_name, ship_size in self.ships.items():
            print(f"{ship_name} (크기: {ship_size})")

        input("\n준비가 되셨으면 Enter 키를 눌러주세요...")

        self.setup_game()

        while True:
            self.print_boards()
            self.player_turn()

            if self.check_game_over():
                break

            self.computer_turn()

            if self.check_game_over():
                break

        print("\n게임이 종료되었습니다. 다시 플레이하려면 프로그램을 재시작하세요.")

if __name__ == "__main__":
    game = BattleshipGame()
    game.play()