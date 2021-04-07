import random
import AzulGame
import RandomAzulPlayerPlus

class RandomAzulPlayer():

    def __init__(self,player):
        self.player = player

    def set_board(self,board):
        self.azul_board = board

    def set_player(self,player):
        self.player = player

    def random_action(self):
        actions = []
        actions = self.azul_board.valid_actions(self.player)
        random.shuffle(actions)
        action = actions.pop()
        return action

class RandomVsRandom():

    def __init__(self):
        self.board = AzulGame.Azul_game()
        self.player_1 = RandomAzulPlayerPlus.RandomAzulPlayerPlus("P1")
        self.player_2 = RandomAzulPlayer("P2")

    def play(self):
        gameover = False

        while not self.board.gameover:
            if not self.board.is_done_phase:

                pit_choice, tile_type, column_choice = self.player_action()
                #player, pit_choice, tile_type, column_choice
                print(f"action:{self.board.player_turn},{pit_choice},{tile_type},{column_choice}")
                self.board.play_turn(self.board.player_turn,pit_choice, tile_type, column_choice)
                self.board.print_table()
                print(self.board.is_done_phase)
                self.board.is_turn_done()

            else:
                print("done_phase")
                self.board.calculate_score("P1")
                self.board.calculate_score("P2")

                self.board.print_table()
                self.board.is_game_done()
                if not self.board.gameover:
                    self.board.create_random_drawing_pit()

        self.board.compute_final_points()
        #self.board.final_points("P2")
        self.board.print_table()

    def player_action(self):

        if self.board.player_turn == "P1":
            self.player_1.set_board(self.board)
            return self.player_1.random_action()
        else:
            self.player_2.set_board(self.board)
            return self.player_2.random_action()

if __name__ == '__main__':
    a = RandomVsRandom()
    a.play()
