
# MCTS algorithm implementation

# packages
import math
import random

# tree node class definition
class TreeNode():
    # class constructor (create tree node class instance)
    def __init__(self, board, parent):

        # init associated board state
        self.board = board

        # init is node terminal flag

        if self.board.game.is_done_phase:
            # we have a terminal node
            self.is_terminal = True

        # otherwise
        else:
            # we have a non-terminal node
            self.is_terminal = False

        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal

        # init parent node if available
        self.parent = parent

        # init the number of node visits
        self.visits = 0

        # init the total score of the node

        row, column, color, expected_row_points, expected_column_point = board.game.analisys_row, board.game.analisys_column,\
            board.game.analisys_color, board.game.analisys_expected_row_points,  board.game.analisys_column_point

        self.score = board.game.inserted_tile_in_column_for_action + expected_row_points + expected_column_point - board.game.penality_for_action

        # init current node's children
        self.children = {}

# MCTS class definition
class MCTS():
    
    # search for the best move in the current position
    def search(self, initial_state):
        # create root node
        self.root = TreeNode(initial_state, None)

        # walk through 1000 iterations
        for iteration in range(2000):

            # select a node (selection phase)
            node = self.select(self.root)

            # score current node (simulation phase)
            score = self.rollout(node.board)

            # backpropagate results
            self.backpropagate(node, score)

        # pick up the best move in the current position
        try:
            return self.get_best_move(self.root, 0)

        except:
            pass

    # select most promising node
    def select(self, node):
        # make sure that we're dealing with non-terminal nodes


        #node.board.game.is_turn_done()
        if node.board.game.is_done_phase :
            node.is_terminal = True

        while not node.is_terminal:

            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
                #print(node.__dict__)

            # case where the node is not fully expanded
            else:
                # otherwise expand the node
                a = self.expand(node)

                return a

        # return node

        return node

    # expand node
    def expand(self, node):
        # generate legal states (moves) for the given node
        states = node.board.generate_states()
        #print(states)
        # loop over generated states (moves)
        for state in states:
            # make sure that current state (move) is not present in child nodes
            state_board = state.game
            action = (state_board.pit_choice, state_board.color_choice, state_board.row_choice)

            if action not in node.children:
                # create a new node
                new_node = TreeNode(state, node)

                # add child node to parent's node children list (dict)
                node.children[action] = new_node

                # case when node is fully expanded
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                # return newly created node
                return new_node


        # debugging
        print('Should not get here!!!')

    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.game.is_done_phase:
            # try to make a move
            try:
                # make the on board
                board = random.choice(board.generate_states())

            # no moves available
            except:
                # return a draw score
                return 0

        # return score from the player "x" perspective
        board.game.calculate_score("P1")
        board.game.calculate_score("P2")

        return board.game.p2_score - board.game.p1_score

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1

            # update node's score
            node.score += score

            # set node to parent
            node = node.parent

    # select the best node basing on UCB1 formula
    def get_best_move(self, node, exploration_constant):
        # define best score & best moves
        best_score = float('-inf')
        best_moves = []

        # loop over child nodes
        for child_node in node.children.values():
            # define current player
            if child_node.board.game.player_played_turn == 'P2' : current_player = 1
            elif child_node.board.game.player_played_turn == 'P1' : current_player = -1

            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt \
                (math.log(node.visits / child_node.visits))

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)

        # return one of the best moves randomly
        return random.choice(best_moves)