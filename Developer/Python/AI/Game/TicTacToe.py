import pygame
import random
import tflearn
import time
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Tic Tac Toe')
window.fill((255, 255, 255))
font = pygame.font.SysFont('monospace', 100)

# Computer is X
# X in training Data is 1, O is -1, and empty is 0

game_won = False
is_computer_move = True
should_use_data = False
training_data = []
data = []
moves = []


class Game(object):
    def __init__(self):
        self.board = [0, 0, 0,
                      0, 0, 0,
                      0, 0, 0]
        self.boards = []
        self.moves = []
        self.board_check = []  # Stores the current pieces on the board with col + row [12, 23, 32]
        self.xs = []  # Stores the x pieces like board_check
        self.os = []  # Stores the o pieces like the board_check
        self.currentMove = 'X'  # Stores the current move as a 'X' or an 'O'

    def create_board(self):
        pygame.draw.line(window, (0, 0, 0), (200, 600), (200, 0), 5)
        pygame.draw.line(window, (0, 0, 0), (400, 600), (400, 0), 5)
        # Horizontal Lines
        pygame.draw.line(window, (0, 0, 0), (600, 200), (0, 200), 5)
        pygame.draw.line(window, (0, 0, 0), (600, 400), (0, 400), 5)
        pygame.display.update()

    def check_for_game_over(self):
        cols = []
        rows = []
        global game_won
        global should_use_data
        # Check X's first

        for number in self.xs:
            string_number = str(number)
            number_list = []
            for char in string_number:
                number_list.append(int(char))
            cols.append(number_list[0])
            rows.append(number_list[1])

        if cols.count(1) == 3 or cols.count(2) == 3 or cols.count(3) == 3 or rows.count(1) == 3 or rows.count(2) == 3 or rows.count(3) == 3:
            label = font.render('X Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True
            should_use_data = True

        if self.board[0] == 1 and self.board[4] == 1 and self.board[8] == 1:
            label = font.render('X Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True
            should_use_data = True

        if self.board[2] == 1 and self.board[4] == 1 and self.board[6] == 1:
            label = font.render('X Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True
            should_use_data = True

        # Check O's second
        cols = []
        rows = []

        for number in self.os:
            string_number = str(number)
            number_list = []
            for char in string_number:
                number_list.append(int(char))
            cols.append(number_list[0])
            rows.append(number_list[1])

        if cols.count(1) == 3 or cols.count(2) == 3 or cols.count(3) == 3 or rows.count(1) == 3 or rows.count(2) == 3 or rows.count(3) == 3:
            label = font.render('O Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True

        if self.board[0] == -1 and self.board[4] == -1 and self.board[8] == -1:
            label = font.render('O Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True

        if self.board[2] == -1 and self.board[4] == -1 and self.board[6] == -1:
            label = font.render('O Wins!', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True

        # Check for a tie
        if len(self.board_check) == 9 and not game_won:
            label = font.render('Tie', True, (0, 0, 0))
            label_rect = label.get_rect(center=(300, 300))
            window.blit(label, label_rect)
            game_won = True
            should_use_data = True

    def place_piece(self, position):
        current_number_string = ''

        if position[0] <= 200:
            x = 100
            current_number_string += '1'
        elif position[0] <= 400:
            x = 300
            current_number_string += '2'
        else:
            x = 500
            current_number_string += '3'

        if position[1] <= 200:
            y = 100
            current_number_string += '1'
        elif position[1] <= 400:
            y = 300
            current_number_string += '2'
        else:
            y = 500
            current_number_string += '3'

        current_number = int(current_number_string)
        if current_number not in self.board_check:
            self.board_check.append(current_number)
            if self.currentMove == 'O':
                pygame.draw.circle(window, (0, 0, 0), (x, y), 50, 5)
                self.currentMove = 'X'
                self.os.append(current_number)
                index_to_change = 0
                number_array = []
                # Separates the column from the row
                for char in current_number_string:
                    number_array.append(int(char))
                # Adds the number for each row
                if number_array[0] == 2:
                    index_to_change = 3
                elif number_array[0] == 3:
                    index_to_change = 6
                index_to_change += number_array[1]
                self.board[index_to_change - 1] = -1
            else:
                pygame.draw.line(window, (0, 0, 0), (x - 50, y - 50), (x + 50, y + 50), 5)
                pygame.draw.line(window, (0, 0, 0), (x - 50, y + 50), (x + 50, y - 50), 5)
                self.currentMove = 'O'
                self.xs.append(current_number)
                index_to_change = 0
                number_array = []
                for char in current_number_string:
                    number_array.append(int(char))
                if number_array[0] == 2:
                    index_to_change = 3
                elif number_array[0] == 3:
                    index_to_change = 6
                index_to_change += number_array[1]
                self.boards += self.board
                self.board[index_to_change - 1] = 1
                self.moves.append(index_to_change)

            self.check_for_game_over()

    def get_pos_to_play(self, events):
        global is_computer_move
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                is_computer_move = True
                self.place_piece(position)

    def not_random_move(self, block):
        if block == 0:
            self.place_piece((100, 100))
        elif block == 1:
            self.place_piece((100, 300))
        elif block == 2:
            self.place_piece((100, 500))
        elif block == 3:
            self.place_piece((300, 100))
        elif block == 4:
            self.place_piece((300, 300))
        elif block == 5:
            self.place_piece((300, 500))
        elif block == 6:
            self.place_piece((500, 100))
        elif block == 7:
            self.place_piece((500, 300))
        elif block == 8:
            self.place_piece((500, 500))

    def random_move(self):
        zeros = []
        counter = 0
        for piece in self.board:
            if piece == 0:
                zeros.append(counter)
            counter += 1

        if len(zeros) != 0:
            block = random.choice(zeros)

            if block == 0:
                self.place_piece((100, 100))
            elif block == 1:
                self.place_piece((100, 300))
            elif block == 2:
                self.place_piece((100, 500))
            elif block == 3:
                self.place_piece((300, 100))
            elif block == 4:
                self.place_piece((300, 300))
            elif block == 5:
                self.place_piece((300, 500))
            elif block == 6:
                self.place_piece((500, 100))
            elif block == 7:
                self.place_piece((500, 300))
            elif block == 8:
                self.place_piece((500, 500))

        # block += 1
        # return block

    def clean_up_data(self):
        new_array = self.boards
        global data

        while len(new_array) > 0:
            appender = new_array[:9]
            data.append(appender)
            del new_array[0:9]

# Creating the Neural Network


def create_model():
    network = input_data(shape=(None, 9), name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 1, activation='linear')
    network = regression(network, optimizer='adam', learning_rate=0.01, loss='mean_square', name='targets')

    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


def train_model(x, y):

    x = np.reshape(x, (-1, 9))
    y = np.reshape(y, (-1, 1))

    model = create_model()
    model.fit({'input': x}, {'targets': y}, n_epoch=50, snapshot_step=500, show_metric=True, run_id='openai_learning')

    return model


def gather_training_data(games):
    global data
    global game_won
    global moves
    global should_use_data
    for each_game in range(games):
        game = Game()
        while True:
            pygame.event.get()
            game.create_board()
            if not game_won:
                game.random_move()
            else:
                break
        if should_use_data:
            game.clean_up_data()
            moves += game.moves
            game_won = False
            should_use_data = False
        window.fill((255, 255, 255))

    return data, moves

x, y = gather_training_data(1000)

model = train_model(x, y)

print 'Len', len(x)
newData = x[5]
newData = np.reshape(newData, (-1, 9))

data_to_edit = model.predict(newData)[0]
data_to_edit = round(data_to_edit[0])

print data_to_edit
print y[5]

game = Game()

game_won = False

while True:
    events = pygame.event.get()
    game.create_board()
    if not game_won:
        if is_computer_move:
            # game.random_move()
            move = model.predict(np.reshape(game.board, (-1, 9)))
            move = move[0]
            move = move[0]
            print int(round(move))
            game.not_random_move(int(round(move)))
            is_computer_move = False
        else:
            game.get_pos_to_play(events)
    pygame.display.update()

pygame.quit()
quit()
