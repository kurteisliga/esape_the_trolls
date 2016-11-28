import operator
import random
from player import Player
from troll import Troll

direction_key = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1)
}

maze = """#########################################################################
#   #               #               #           #                   #   #
#   #   #########   #   #####   #########   #####   #####   #####   #   #
#               #       #   #           #           #   #   #       #   #
#########   #   #########   #########   #####   #   #   #   #########   #
#       #   #               #           #   #   #   #   #           #   #
#   #   #############   #   #   #########   #####   #   #########   #   #
#   #               #   #   #       #           #           #       #   #
#   #############   #####   #####   #   #####   #########   #   #####   #
#           #       #   #       #   #       #           #   #           #
#   #####   #####   #   #####   #   #########   #   #   #   #############
#       #       #   #   #       #       #       #   #   #       #       #
#############   #   #   #   #########   #   #####   #   #####   #####   #
#           #   #           #       #   #       #   #       #           #
#   #####   #   #########   #####   #   #####   #####   #############   #
#   #       #           #           #       #   #   #               #   #
#   #   #########   #   #####   #########   #   #   #############   #   #
#   #           #   #   #   #   #           #               #   #       #
#   #########   #   #   #   #####   #########   #########   #   #########
#   #       #   #   #           #           #   #       #               #
#   #   #####   #####   #####   #########   #####   #   #########   #   #
#   #                   #           #               #               #   #
# X #####################################################################"""

class Maze():
    def __init__(self):
        self.create_maze()
        self.trolls = list()
        self.player = Player()
        self.set_initial_player_position()
        self.find_maze_exit()

    def create_maze(self):
        self.board = [list(line) for line in maze.split('\n')]

    def print_maze(self):
        for item in self.board:
            print( ''.join(item)  )

    def set_initial_player_position(self):
        row, column = self.generate_random_position()
        self.player.y_pos = row
        self.player.x_pos = column
        self.board[row][column] = self.player.direction

    def set_initial_troll_position(self, difficulty):
        for troll in range(difficulty):
            trolls = Troll()
            row, column = self.generate_random_position()
            trolls.y_pos = row
            trolls.x_pos = column
            self.board[row][column] = 'T'
            self.trolls.append(trolls)

    def generate_random_position(self):
        random.seed()

        while True:
            column = random.randrange(0, len(self.board[0])-1)
            row = random.randrange(0, len(self.board)-1)

            if self.board[row][column] == ' ':
                return (row, column)


    def find_maze_exit(self):
        y_pos = 0
        for row in self.board:
            if 'X' in row:
                self.exit = (y_pos, row.index('X'))
            y_pos += 1


    def is_won(self):
        if self.player.position() == self.exit:
            return True
        return False

    def move(self, dir):
        position = self.player.position()

        new_pos = tuple(map(operator.add, position, direction_key[dir]))

        if self.movement_valid(new_pos):
            if '#' not in self.board[new_pos[0]][new_pos[1]]:
                self.player.set_position(new_pos)
                self.player.set_direction(dir)
                self.board[position[0]][position[1]] = ' '
                self.board[new_pos[0]][new_pos[1]] = self.player.facing()
            else:
                block_new_pos = tuple(map(operator.add, new_pos, direction_key[dir]))
                if self.movement_valid(block_new_pos) and '#' not in self.board[block_new_pos[0]][block_new_pos[1]]:
                    self.player.set_position(new_pos)
                    self.player.set_direction(dir)
                    self.board[position[0]][position[1]] = ' '
                    self.board[new_pos[0]][new_pos[1]] = self.player.facing()
                    self.board[block_new_pos[0]][block_new_pos[1]] = '#'


    def movement_valid(self, position):
        if all( i > 0 for i in position):
            if position[0] < len(self.board) and position[1] < len(self.board[0]):
                return True
        return False



