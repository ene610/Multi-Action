#
# AI that learns to play Tic Tac Toe using
#        reinforcement learning
#                (MCTS)
#

# packages
from copy import deepcopy
from MCTS import *
from AzulGame import *
import RandomAzulPlayerPlus

# Tic Tac Toe board class
class Board():

    # create constructor (init board class instance)
    def __init__(self, board=None):
        # define players
        if board:
            self.game = deepcopy(board.game)

    # make move
    def make_move(self, player, pit, color, row):
        # create new board instance that inherits from the current state
        board = Board(self)
        # make move
        board.game.play_turn(player, pit, color, row)

        board.game.is_turn_done()
        # return new board state
        return board

    # generate legal moves to play in the current position
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
        actions = []
        #action_array contains [pit , color , row]
        for action_array in self.game.valid_actions(self.game.player_turn):
            actions.append(self.make_move(self.game.player_turn, action_array[0], action_array[1], action_array[2]))

        # return the list of available actions (board class instances)

        return actions

    # main game loop
    def game_loop_vs_human(self):
        print('\n  Tic Tac Toe by Code Monkey King\n')
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')

        # print board
        print(self)

        # create MCTS instance
        mcts = MCTS()

        # game loop
        while True:

            player_to_play = self.game.player_turn
            if (player_to_play == "P1"):
                # get user input
                user_input = input('> ')

                # escape condition
                if user_input == 'exit': break

                # skip empty input
                if user_input == '': continue

                try:
                    # parse user input (move format [col, row]: 1,2)
                    pit = int(user_input.split(',')[0]) - 1
                    color = int(user_input.split(',')[1]) - 1
                    row = int(user_input.split(',')[2]) - 1

                    # check move legality
                    if self.game.valid_move(player_to_play,pit,color,row):
                        self = self.make_move(player_to_play, pit, color, row)
                        print(self)
                    else:
                        print(' Illegal move!')
                        continue
                except Exception as e:
                    print('  Error:', e)
                    print('  Illegal command!')
                    print('  Move format "pit,color,row"')

                # make move on board

                # search for the best move
            #else gioca MCTS

            else:
                best_move = mcts.search(self)
                # legal moves available
                try:
                # make AI move here
                    self = best_move.board
                    print("MCTS played:", self.game.pit_choice,self.game.color_choice,self.game.row_choice)
                # game over
                except:
                    pass
                print(self)

                # print board


                # check if the game is won
            if self.game.is_done_phase:
                    print("is done phase\n")
                    break


    def game_loop_vs_random_player(self):

        # print board
        print(self)

        # create MCTS instance
        mcts = MCTS()

        # game loop
        while True:

            player_to_play = self.game.player_turn
            random_player = RandomAzulPlayerPlus.RandomAzulPlayerPlus("P1")
            
            if player_to_play == "P1":
                random_player.set_board(self.game)
                pit_choice, tile_type, column_choice = random_player.random_action()
                self = self.make_move(player_to_play, pit_choice, tile_type, column_choice)
                print(self)
            #else gioca MCTS

            else:
                best_move = mcts.search(self)
                # legal moves available
                try:
                # make AI move here
                    self = best_move.board
                    print("MCTS played:", self.game.pit_choice, self.game.color_choice, self.game.row_choice)
                # game over
                except:
                    pass
                print(self)

                # print board


                # check if the game is won
            if self.game.is_done_phase:
                    print("is done phase\n")
                    break

    # print board state
    def __str__(self):
        return self.game.game_to_string()

# main driver
if __name__ == '__main__':

    # create board instance
    game = Azul_game()
    board = Board()
    board.game = game

    # start game loop
    board.game_loop_vs_random_player()
