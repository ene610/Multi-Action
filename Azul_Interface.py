
from AzulGame import Azul_game
import RandomAzulPlayer as RandomAzulPlayer
import gym
from gym import spaces
import random
import numpy as np



class Azul_interface():

    def __init__(self):
        self.game = Azul_game()
        self.penality_for_action = 0
        self.penality_row_prev_action = [0, 0, 0, 0, 0, 0, 0]
        self.opponent_turn = "P2"
        self.opponent = RandomAzulPlayer.RandomAzulPlayer("P2")
        # self.opponent_turn = "P2"
        self.valid_move = True
        self.player_AI = "P1"

        #  pit_choice, tile_type, column_choice
        self.action_pit_choice = -1
        self.action_tile_type = -1
        self.action_column_choice = -1

    def action(self, action):
        self.action_pit_choice, self.action_tile_type, self.action_column_choice = self.game.from_action_to_tuple_action(
            action)

        self.valid_move = self.game.valid_move(self.player_AI, self.action_pit_choice, self.action_tile_type,
                                               self.action_column_choice)

        # se player è P1

        self.game.play_turn(self.player_AI, self.action_pit_choice, self.action_tile_type, self.action_column_choice)

        penality_row_after_action = self.game.penalty_row_p1

        # print(self.penality_row_prev_action,penality_row_after_action)
        penality = 0

        for i in range(len(penality_row_after_action)):
            if penality_row_after_action[i] != self.penality_row_prev_action[i]:
                penality = penality + 1
                # print("PENALITA" * 1000)

        self.penality_row_prev_action = penality_row_after_action

        self.penality_for_action = penality

        self.game.is_turn_done()
        self.game.is_game_done()

    def is_done(self):
        if (self.game.gameover):
            self.game.compute_final_points()
            return True
        return False

    def observe(self):

        self.game.is_turn_done()

        if (self.game.is_done_phase):
            self.game.calculate_score("P1")
            self.game.calculate_score("P2")
            self.game.create_random_drawing_pit()

        while self.game.player_turn != self.player_AI:
            # richiama l'azione del opponent
            self.opponent.set_board(self.game)
            pit_choice, tile_type, column_choice = self.opponent.random_action()
            self.game.play_turn(self.opponent, pit_choice, tile_type, column_choice)

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

        return obs

    def evaluete(self):
        # print(self.penality_for_action)
        if self.valid_move:
            return +1 - (self.penality_for_action * 0.2)
        else:
            return -1

    def view(self):
        return self.game.print_table()