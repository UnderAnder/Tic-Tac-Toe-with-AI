from re import match


class Game:
    valid_symbols = 'XO_'

    def __init__(self):
        self.menu = Menu()
        self.grid = Grid()
        self.draw = Draw()
        self.table_state = dict(zip(self.grid.table, self.menu.init_table_state()))
        self.game_state = 'Game not finished'

    def start(self):
        self.draw.draw_table(self.table_state)
        while self.game_state == 'Game not finished':
            self.move()
            self.draw.draw_table(self.table_state)
            self.check_game_state()
            print(self.game_state)

    def move(self):
        cells = ''.join(self.table_state.values())
        cell = self.menu.make_move()

        if self.table_state[cell] != '_':
            print('This cell is occupied! Choose another one!')
            self.move()

        if cells.count("X") - cells.count("O") == 0:
            self.table_state[cell] = 'X'
        else:
            self.table_state[cell] = 'O'

    def check_game_state(self):
        x_pattern = r'(?:X..X..X..|.X..X..X.|..X..X..X|XXX......|...XXX...|......XXX|X...X...X|..X.X.X..)$'
        o_pattern = r'(?:O..O..O..|.O..O..O.|..O..O..O|OOO......|...OOO...|......OOO|O...O...O|..O.O.O..)$'
        f_pattern = r'(?:_.._.._..|._.._.._.|.._.._.._|___......|...___...|......___|_..._..._|.._._._..)$'
        cells = ''.join(self.table_state.values())

        if match(x_pattern, cells):
            self.game_state = 'X wins'
            return
        if match(o_pattern, cells):
            self.game_state = 'O wins'
            return
        # if not match(f_pattern, cells):
        #     self.game_state = 'Draw'
        if cells.find('_') == -1:
            self.game_state = 'Draw'
            return


class Grid:
    SIZE = 3

    def __init__(self):
        self.table = [(x, y) for x in range(1, self.SIZE + 1) for y in range(1, self.SIZE + 1)]


class Menu:
    def __init__(self):
        pass

    def init_table_state(self):
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
        except ValueError:
            print('You should enter numbers!')
            coord_x, coord_y = self.make_move()
        if not (str(coord_x).isdigit() or str(coord_y).isdigit()):
            print('You should enter numbers!')
            coord_x, coord_y = self.make_move()
        coord_x, coord_y = int(coord_x), int(coord_y)
        if not 0 < coord_x < size + 1 or not 0 < coord_y < size + 1:
            print(f'Coordinates should be from 1 to {size}!')
            coord_x, coord_y = self.make_move()
        return coord_x, coord_y


class Draw:
    @staticmethod
    def draw_table(table_state):
        values = ' '.join(table_state.values())
        size = Grid.SIZE
        horizontal_line = '---' * size

        print(horizontal_line)
        for group in chunker(values, size*2):
            print(group.replace('  ', ' ').replace('_', ' '))
        print(horizontal_line)


def chunker(seq, size):
    return (f'| {seq[pos:pos + size]} |' for pos in range(0, len(seq), size))


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
