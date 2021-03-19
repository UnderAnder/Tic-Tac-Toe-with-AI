from re import match
from random import choice

class Game:
    valid_symbols = 'XO_'

    def __init__(self, board=None):
        self.menu = Menu()
        self.grid = Grid()
        self.ai = AI()
        self.board = self.grid.table if board is None else board
        self.cells = ''.join(self.board.values())
        self.move_count = self.grid.SIZE ** 2 - self.cells.count('_')

    def start(self):
        player1, player2 = self.menu.start()
        self.grid.draw_table(self.cells)
        while not self.check_win():
            self.move(player1, player2)
            self.cells = ''.join(self.board.values())
            self.grid.draw_table(self.cells)

        print(self.check_win())

    def move(self, player1, player2):
        # Player choose
        sign = 'X' if self.move_count % 2 == 0 else 'O'
        if sign == 'X':
            cell = self.menu.make_move(self.board) if player1 == 'user' else self.ai.make_move(player1, self.board)
        else:
            cell = self.menu.make_move(self.board) if player2 == 'user' else self.ai.make_move(player2, self.board)
        self.move_count += 1
        self.board[cell] = sign

    def check_win(self, cells=None):
        x_pattern = r'(?:X..X..X..|.X..X..X.|..X..X..X|XXX......|...XXX...|......XXX|X...X...X|..X.X.X..)$'
        o_pattern = r'(?:O..O..O..|.O..O..O.|..O..O..O|OOO......|...OOO...|......OOO|O...O...O|..O.O.O..)$'
        # For copy board check
        cells = self.cells if cells is None else cells

        if match(x_pattern, cells):
            return 'X wins'
        if match(o_pattern, cells):
            return 'O wins'
        if cells.find('_') == -1:
            return 'Draw'
        return False


class AI:
    def make_move(self, level, board):
        empty_cells = [coordinates for coordinates, state in board.items() if state == '_']
        if level == 'easy':
            return self.easy(empty_cells)
        if level == 'medium':
            return self.medium(board, empty_cells)
        if level == 'hard':
            return self.hard(board)

    def easy(self, empty_cells):

        coordinates = self.random_move(empty_cells)
        print('Making move level "easy"')
        return coordinates

    def medium(self, board, empty_cells):
        # Sim game to check win/lose positions
        sim_game = Game(board.copy())
        signs = 'XO' if sim_game.move_count % 2 == 0 else 'OX'
        # Win/not lose move search
        for sign in signs:
            for cell in empty_cells:
                sim_game.board[cell] = sign
                cells = ''.join(sim_game.board.values())
                if sim_game.check_win(cells):
                    print('Making move level "medium"')
                    return cell
                else:
                    sim_game.board[cell] = '_'

        print('Making move level "medium"')
        return self.random_move(empty_cells)

    def hard(self, board):
        sim_game = Game(board.copy())
        signs = 'XO' if sim_game.move_count % 2 == 0 else 'OX'
        # Minimax move search
        best_move = self.minimax(sim_game, signs[0], signs)

        print('Making move level "hard"')
        print(best_move)
        return best_move[0]

    def minimax(self, game, player, signs):
        cur_player, opponent = signs[0], signs[1]
        empty_cells = [coordinates for coordinates, state in game.board.items() if state == '_']
        if game.check_win() == f'{opponent} wins':
            return (0, 0), -1
        elif game.check_win() == f'{cur_player} wins':
            return (0, 0), 1
        elif game.move_count == Grid.SIZE**2:
            return (0, 0), 0

        moves = {}
        for cell in empty_cells:
            move = {}
            game.board[cell] = player
            if cur_player == player:
                result = self.minimax(Game(game.board.copy()), opponent, signs)
                move[cell] = result[1]
            else:
                result = self.minimax(Game(game.board.copy()), cur_player, signs)
                move[cell] = result[1]

            game.board[cell] = '_'

            moves[cell] = move[cell]

        if cur_player == player:
            best_score = -100
            for coords, score in moves.items():
                if score > best_score:
                    best_score = score
                    best_move = (coords, score)
        else:
            best_score = 100
            for coords, score in moves.items():
                if score < best_score:
                    best_score = score
                    best_move = (coords, score)

        return best_move



    @staticmethod
    def random_move(empty_cells):
        return choice(empty_cells)


class Menu:
    def start(self):
        options = ('user', 'easy', 'medium', 'hard')
        command = input('Input command: ').strip()
        if command == 'exit':
            exit()
        try:
            command, player1, player2 = command.split()
        except ValueError:
            print('Bad parameters!')
            player1, player2 = self.start()
        if command != 'start' or player1 not in options or player2 not in options:
            print('Bad parameters!')
            player1, player2 = self.start()
        return player1, player2

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
