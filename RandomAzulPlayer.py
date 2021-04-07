import random
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
