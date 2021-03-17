from re import match
from random import choice


class Game:
    valid_symbols = 'XO_'

    def __init__(self):
        self.menu = Menu()
        self.grid = Grid()
        self.ai = AI()
        self.table_state = self.grid.table
        self.game_state = 'Game not finished'

    def start(self):
        player1, player2 = self.menu.start()
        while self.game_state == 'Game not finished':
            cells = ''.join(self.table_state.values())
            self.grid.draw_table(cells)
            if self.check_game_state(cells):
                break
            self.move(cells, player1, player2)

        print(self.game_state)

    def move(self, cells, player1, player2):
        sign = 'X' if cells.count('X') - cells.count('O') == 0 else 'O'
        if sign == 'X':
            cell = self.menu.make_move() if player1 == 'user' else self.ai.make_move(player1)
        else:
            cell = self.menu.make_move() if player2 == 'user' else self.ai.make_move(player2)

        if self.table_state[cell] != '_':
            if (sign == 'X' and player1 == 'user') or (sign == 'O' and player2 == 'user'):
                print('This cell is occupied! Choose another one!')
            self.move(cells, player1, player2)
        else:
            if sign == 'X' and player1 != 'user':
                print(f'Making move level "{player1}"')
            elif sign == 'O' and player2 != 'user':
                print(f'Making move level "{player2}"')
            self.table_state[cell] = sign

    def check_game_state(self, cells):
        x_pattern = r'(?:X..X..X..|.X..X..X.|..X..X..X|XXX......|...XXX...|......XXX|X...X...X|..X.X.X..)$'
        o_pattern = r'(?:O..O..O..|.O..O..O.|..O..O..O|OOO......|...OOO...|......OOO|O...O...O|..O.O.O..)$'
        # f_pattern = r'(?:_.._.._..|._.._.._.|.._.._.._|___......|...___...|......___|_..._..._|.._._._..)$'

        if match(x_pattern, cells):
            self.game_state = 'X wins'
            return True
        if match(o_pattern, cells):
            self.game_state = 'O wins'
            return True
        # if not match(f_pattern, cells):
        #     self.game_state = 'Draw'
        if cells.find('_') == -1:
            self.game_state = 'Draw'
            return True


class AI:
    @staticmethod
    def make_move(level):
        if level == 'easy':
            choices = [digit for digit in range(1, Grid.SIZE + 1)]
            coord_x = choice(choices)
            coord_y = choice(choices)
            return coord_x, coord_y


class Menu:
    def init_table_state(self):
        """
        Its not used anymore
        """
        cells_num = Grid.SIZE ** 2
        command = input('Enter the cells: ').strip()
        if len(command) != cells_num:
            print(f'Enter {cells_num} cells without whitespaces')
            command = self.init_table_state()
        if not all(c in Game.valid_symbols for c in command):
            print('X O _ only')
            command = self.init_table_state()
        return command

    def make_move(self):
        size = Grid.SIZE
        command = input('Enter the coordinates: ').strip()
        try:
            coord_x, coord_y = command.split()
            coord_x, coord_y = int(coord_x), int(coord_y)
        except ValueError:
            print('You should enter numbers!')
            coord_x, coord_y = self.make_move()
        if not (0 < coord_x < size + 1 and 0 < coord_y < size + 1):
            print(f'Coordinates should be from 1 to {size}!')
            coord_x, coord_y = self.make_move()
        return coord_x, coord_y

    def start(self):
        variants = ('user', 'easy')
        command = input('Input command: ').strip()
        if command == 'exit':
            self.exit()
        try:
            command, player1, player2 = command.split()
        except ValueError:
            print('Bad parameters!')
            player1, player2 = self.start()
        if command != 'start' or player1 not in variants or player2 not in variants:
            print('Bad parameters!')
            player1, player2 = self.start()
        return player1, player2

    @staticmethod
    def exit():
        exit()


class Grid:
    SIZE = 3

    def __init__(self):
        self.table = {(x, y): '_' for x in range(1, self.SIZE + 1) for y in range(1, self.SIZE + 1)}

    @staticmethod
    def draw_table(cells):
        cells = cells.replace('_', ' ')
        print("""
            ---------
            | {} {} {} |
            | {} {} {} |
            | {} {} {} |
            ---------
        """.format(*cells))


def main():
    Game().start()


if __name__ == '__main__':
    main()
