
import AzulGame
import RandomAzulPlayer
import numpy as np


class Azul_interface():

    def __init__(self):

        self.game = AzulGame.Azul_game()
        self.penality_for_action = 0
        self.penality_row_prev_action = [0, 0, 0, 0, 0, 0, 0]
        self.opponent_turn = "P2"
        self.opponent = RandomAzulPlayer.RandomAzulPlayer("P2")

        # self.opponent_turn = "P2"
        self.valid_move = True
        self.player_dqn = "P1"

        # pit_choice, tile_type, column_choice
        self.action_pit_choice = -1
        self.action_tile_type = -1
        self.action_column_choice = -1

    def action(self, action):

        self.action_pit_choice, self.action_tile_type, self.action_column_choice = self.game.from_action_to_tuple_action(
            action)
        self.valid_move = self.game.valid_move(self.player_dqn, self.action_pit_choice, self.action_tile_type,
                                               self.action_column_choice)

        # se player è P1
        self.game.play_turn(self.player_dqn, self.action_pit_choice, self.action_tile_type, self.action_column_choice)

        penality_row_after_action = self.game.penalty_row_p1

        # print(self.penality_row_prev_action,penality_row_after_action)
        penality = 0

        self.penality_row_prev_action = penality_row_after_action

        self.penality_for_action = self.game.penality_for_action

        self.game.is_turn_done()
        self.game.is_game_done()

        if self.game.is_done_phase:
            self.game.calculate_score("P1")
            self.game.calculate_score("P2")
            # attiva quando fai partire tutto il gioco
            # self.game.create_random_drawing_pit()

    def is_done(self):
        self.game.is_turn_done()
        if self.game.is_done_phase:
            self.game.calculate_score("P1")
            self.game.calculate_score("P2")
            return True

        # per tutto il game
        # if(self.game.gameover):
        #
        #    self.game.compute_final_points()
        #    return True

        return False

    def opponent_action(self):

        while self.game.player_turn != self.player_dqn and not self.game.is_done_phase:

            # richiama l'azione del opponent
            self.opponent.set_board(self.game)
            pit_choice, tile_type, column_choice = self.opponent.random_action()
            self.game.play_turn(self.opponent, pit_choice, tile_type, column_choice)

            self.game.is_turn_done()
            self.game.is_game_done()

            if self.game.is_done_phase:
                self.game.calculate_score("P1")
                self.game.calculate_score("P2")

                # attiva quando fai partire tutto il gioco
                # self.game.create_random_drawing_pit()

    def observe(self):

        self.opponent_action()

        # self.game.p1_score
        obs = []

        for elem in self.game.rows_p1:
            obs = obs + elem

        for elem in self.game.penalty_row_p1:
            obs.append(elem)

        for row in self.game.board_p1:
            for elem in row:
                obs.append(elem)

        for pit in self.game.drawing_pit:
            for elem in pit:
                obs.append(elem)

        return np.array(obs)

    def evaluete(self):

        row, column, color, expected_row_points, expected_column_points = self.game.action_analisys()
        reward = self.game.inserted_tile_in_column_for_action * 0.1 + expected_row_points + expected_column_points - self.game.penality_for_action

        if self.valid_move:
            return reward
        else:
            return -100

    def view(self):
        return self.game.print_table()
