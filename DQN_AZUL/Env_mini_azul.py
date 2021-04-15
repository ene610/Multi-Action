import gym
from gym import spaces
import random

from Multi_Action.Azul_Interface import Azul_interface


class CustomEnv(gym.Env):

    def __init__(self):

        self.pygame = Azul_interface()
        self.action_space = spaces.Discrete(180)

        self.action_space_column = spaces.Discrete(6)
        self.action_space_color = spaces.Discrete(5)
        self.action_space_pit = spaces.Discrete(6)

        rows_player_obs = [5] * 15
        penality_player_obs = [1] * 7
        board_player_obs = [1] * 25
        normal_pit_obs = [4] * 5 * 5
        column_choice_obs = [6]
        color_choice_obs = [5]
        n_free_tile_in_column = [7]

        # al massimo ci possono essere 3*5 tessere nel discard pit per una singola tessera
        discard_pit_obs = [3 * 5] * 5
        one_player_obs = rows_player_obs + penality_player_obs + board_player_obs + \
                         normal_pit_obs + discard_pit_obs

        observation_array_column = rows_player_obs + penality_player_obs + board_player_obs + normal_pit_obs + discard_pit_obs
        # TODO sistema 10 con i veri numeri
        observation_array_color = normal_pit_obs + discard_pit_obs + board_player_obs + column_choice_obs
        observation_array_pit = normal_pit_obs + discard_pit_obs + n_free_tile_in_column + color_choice_obs

        self.observation_space_column = spaces.MultiDiscrete(observation_array_column)
        self.observation_space_color = spaces.MultiDiscrete(observation_array_color)
        self.observation_space_pit = spaces.MultiDiscrete(observation_array_pit)

        self.observation_space = spaces.MultiDiscrete(one_player_obs)

    def is_done(self):
        return self.pygame.is_done()

    def reset(self):

        del self.pygame
        self.pygame = Azul_interface()
        obs = self.pygame.observe()
        return obs

    def step(self, action):

        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluete()
        done = self.pygame.is_done()

        return obs, reward, done, {}

    def render(self, mode='human'):
        print(self.pygame.view())

    def obs_for_column_choice(self):

        obs = []

        for elem in self.pygame.game.rows_p1:
            obs = obs + elem

        for elem in self.pygame.game.penalty_row_p1:
            obs.append(elem)

        for row in self.pygame.game.board_p1:
            for elem in row:
                obs.append(elem)

        for pit in self.pygame.game.drawing_pit:
            for elem in pit:
                obs.append(elem)

        return obs

    def obs_for_color_choice(self):

        obs = []

        for pit in self.pygame.game.drawing_pit:
            for elem in pit:
                obs.append(elem)

        for row in self.pygame.game.board_p1:
            for elem in row:
                obs.append(elem)

        return obs

    def obs_for_pit_choice(self):

        obs = []

        for pit in self.pygame.game.drawing_pit:
            for elem in pit:
                obs.append(elem)

        return obs

    def count_free_tiles(self, column_choice):
        column_to_count = []
        a = 0

        if column_choice == 5:
            column_to_count = self.pygame.game.penalty_row_p1
        else:
            column_to_count = self.pygame.game.rows_p1

        for elem in column_to_count:
            if elem != 0:
                a = a + 1

        return a