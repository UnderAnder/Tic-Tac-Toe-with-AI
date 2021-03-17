from re import match
from random import choice


class Game:
    valid_symbols = 'XO_'

    def __init__(self):
        self.menu = Menu()
        self.grid = Grid()
        self.ai = AI()
        self.table_state = self.grid.table
        self.cells = ''.join(self.table_state.values())
        self.game_state = 'Game not finished'

    def start(self):
        player1, player2 = self.menu.start()
        self.grid.draw_table(self.cells)
        while not self.check_game_state():
            self.move(player1, player2)
            self.cells = ''.join(self.table_state.values())
            self.grid.draw_table(self.cells)

        print(self.game_state)

    def move(self, player1, player2):
        table_state = self.table_state
        # Player choose
        sign = 'X' if self.cells.count('X') - self.cells.count('O') == 0 else 'O'
        if sign == 'X':
            cell = self.menu.make_move(table_state) if player1 == 'user' else self.ai.make_move(player1, table_state)
        else:
            cell = self.menu.make_move(table_state) if player2 == 'user' else self.ai.make_move(player2, table_state)

        self.table_state[cell] = sign

    def check_game_state(self, cells=None):
        x_pattern = r'(?:X..X..X..|.X..X..X.|..X..X..X|XXX......|...XXX...|......XXX|X...X...X|..X.X.X..)$'
        o_pattern = r'(?:O..O..O..|.O..O..O.|..O..O..O|OOO......|...OOO...|......OOO|O...O...O|..O.O.O..)$'
        # For copy board check
        cells = self.cells if cells is None else cells

        if match(x_pattern, cells):
            self.game_state = 'X wins'
            return True
        if match(o_pattern, cells):
            self.game_state = 'O wins'
            return True
        if cells.find('_') == -1:
            self.game_state = 'Draw'
            return True
        return False


class AI:
    def make_move(self, level, table_state):
        if level == 'easy':
            return self.easy(table_state)
        if level == 'medium':
            return self.medium(table_state)

    def easy(self, table_state):
        empty_cells = [coordinates for coordinates, state in table_state.items() if state == '_']
        coordinates = self.random_move(empty_cells)
        print('Making move level "easy"')
        return coordinates

    def medium(self, table_state):
        empty_cells = [coordinates for coordinates, state in table_state.items() if state == '_']
        # Sim game to check win/lose positions
        table_copy = table_state.copy()
        sim_game = Game()
        cells = ''.join(table_copy.values())
        sign = 'X' if cells.count('X') - cells.count('O') == 0 else 'O'
        # Win move search
        for cell in empty_cells:
            table_copy = table_state.copy()
            table_copy[cell] = sign
            cells = ''.join(table_copy.values())
            if sim_game.check_game_state(cells):
                print('Making move level "medium"')
                return cell
        # Not lose move search
        for cell in empty_cells:
            table_copy = table_state.copy()
            table_copy[cell] = 'O' if sign == 'X' else 'X'
            cells = ''.join(table_copy.values())
            if sim_game.check_game_state(cells):
                print('Making move level "medium"')
                return cell

        print('Making move level "medium"')
        return self.random_move(empty_cells)

    @staticmethod
    def random_move(empty_cells):
        return choice(empty_cells)


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

    def make_move(self, table_state):
        size = Grid.SIZE
        command = input('Enter the coordinates: ').strip()
        try:
            coord_x, coord_y = command.split()
            coord_x, coord_y = int(coord_x), int(coord_y)
        except ValueError:
            print('You should enter numbers!')
            coord_x, coord_y = self.make_move(table_state)
        if not (0 < coord_x < size + 1 and 0 < coord_y < size + 1):
            print(f'Coordinates should be from 1 to {size}!')
            coord_x, coord_y = self.make_move(table_state)
        if table_state[coord_x, coord_y] != '_':
            print('This cell is occupied! Choose another one!')
            coord_x, coord_y = self.make_move(table_state)

        return coord_x, coord_y

    def start(self):
        variants = ('user', 'easy', 'medium')
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
