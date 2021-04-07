import random
class RandomAzulPlayerPlus():

    def __init__(self, player):
        self.player = player

    def set_board(self, board):
        self.azul_board = board

    def set_player(self, player):
        self.player = player

    def random_action(self):
        actions = []
        actions = self.azul_board.valid_actions(self.player)
        actions_not_in_penality = []

        for action in actions:

            if action[2] != 5:
                actions_not_in_penality.append(action)

        if actions_not_in_penality:
            actions = actions_not_in_penality

        random.shuffle(actions)
        action = actions.pop()
        return action


