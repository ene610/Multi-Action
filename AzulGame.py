import numpy as np
import pandas as pd


class Azul_game():

    def __init__(self):

        self.p1_score = 0
        self.p2_score = 0

        self.player_turn = "P1"
        self.initial_player = "P1"

        # refattorizza nome
        self.new_first_player = True

        self.board_p1 = np.zeros((5, 5), dtype=int)
        self.board_p2 = np.zeros((5, 5), dtype=int)

        self.rows_p1 = self.initialize_rows()
        self.rows_p2 = self.initialize_rows()

        self.penalty_row_p1 = [0, 0, 0, 0, 0, 0, 0]
        self.penalty_row_p2 = [0, 0, 0, 0, 0, 0, 0]

        self.create_random_drawing_pit()

        self.gameover = False
        self.is_done_phase = False

        self.inserted_tile_in_column_for_action = 0
        self.penality_for_action = 0

        self.player_played_turn = "P1"

        self.pit_choice = -1
        self.color_choice = -1
        self.row_choice = -1

    def initialize_rows(self):

        first_row = np.zeros(1, dtype=int)
        second_row = np.zeros(2, dtype=int)
        third_row = np.zeros(3, dtype=int)
        fourth_row = np.zeros(4, dtype=int)
        fifth_row = np.zeros(5, dtype=int)

        # return [first_row , second_row , third_row , fourth_row , fifth_row]
        return [[0], [0, 0], [0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0]]

    #TODO refactor
    def create_random_drawing_pit(self):
        pit_collection = []

        #
        self.new_first_player = True
        self.player_turn = self.initial_player
        self.is_done_phase = False

        for i in range(5):
            pit = [0, 0, 0, 0, 0]

            for j in range(4):
                generated_tile_type = np.random.randint(0, 5)
                pit[generated_tile_type] = pit[generated_tile_type] + 1

            pit_collection.append(pit)

        discard_pit = [0, 0, 0, 0, 0]
        pit_collection.append(discard_pit)

        self.penalty_row_p1 = [0, 0, 0, 0, 0, 0, 0]
        self.penalty_row_p2 = [0, 0, 0, 0, 0, 0, 0]
        self.drawing_pit = pit_collection

    def valid_move(self, player, pit_choice, tile_type, column_choice):

        drawed_tile = self.drawing_pit[pit_choice][tile_type]

        if (drawed_tile == 0):
            return False

        if (player == "P1"):
            rows = self.rows_p1
            scoreboard = self.board_p1
        else:
            rows = self.rows_p2
            scoreboard = self.board_p2
        if (column_choice != 5):
            position = ((tile_type + column_choice) % 5)
            if (scoreboard[column_choice][position] == 1):
                return False
            if (rows[column_choice][0] == 0 or rows[column_choice][0] == tile_type + 1):
                return True
            return False

        else:
            return True

    def create_custom_drawing_pit(self):

        pit_collection = []

        self.new_first_player = True
        self.player_turn = self.initial_player
        self.is_done_phase = False

        for i in range(5):

            end_pit = False
            while end_pit:
                pit = [0, 0, 0, 0, 0]
                j = 0
                cumulative_tile = 0

                while cumulative_tile < 4 and j < 5:
                    print(f"pit {i + 1}")
                    number_of_tile = input(f"quante tile di tipo {j+1}?")

                    pit[j] = number_of_tile

                j = 0
                if cumulative_tile == 4 :
                    print(pit)
                    response = input("sicuro del pit appena creato? 1 for yes 0, for no")
                    if response:
                        pit_collection.append(pit)
                        end_pit = 0
                else:
                    print("errore nella creazione del pit")

        discard_pit = [0, 0, 0, 0, 0]
        pit_collection.append(discard_pit)

        self.penalty_row_p1 = [0, 0, 0, 0, 0, 0, 0]
        self.penalty_row_p2 = [0, 0, 0, 0, 0, 0, 0]
        self.drawing_pit = pit_collection

    def play_turn(self, player, pit_choice, tile_type, column_choice):

        def insert_tiles_in_penalty_column( number_of_tiles, player):

            if player == "P1":
                penality_row = self.penalty_row_p1
            else:
                penality_row = self.penalty_row_p2

            self.penality_for_action = 0

            # se si riempie la penality column allora vanno scartate le tessere
            for i in range(7):
                if penality_row[i] == 0 and number_of_tiles > 0:
                    penality_row[i] = 1

                    if (i < 2):
                        self.penality_for_action = self.penality_for_action + 1
                    elif (i < 5):
                        self.penality_for_action = self.penality_for_action + 2
                    else:
                        self.penality_for_action = self.penality_for_action + 3

                    number_of_tiles = number_of_tiles - 1

        def take_tile_from_pit( pit_choice, tile_type, player):

            drawed_tiles = self.drawing_pit[pit_choice][tile_type]
            self.drawing_pit[pit_choice][tile_type] = 0

            if not self.new_first_player:
                self.new_first_player = False
                self.initial_player = player

            if (pit_choice != 5):
                for i in range(5):
                    discarded_tile = self.drawing_pit[pit_choice][i]
                    self.drawing_pit[pit_choice][i] = 0
                    self.drawing_pit[5][i] = self.drawing_pit[5][i] + discarded_tile

            return drawed_tiles

        def insert_tiles_in_column( tile_type, drawed_tiles, column_choice, player):

            number_of_drawed_tile = drawed_tiles

            if player == "P1":
                rows = self.rows_p1
                scoreboard = self.board_p1
            else:
                rows = self.rows_p2
                scoreboard = self.board_p2

            if column_choice == 5:
                insert_tiles_in_penalty_column(number_of_drawed_tile, player)
                return

            self.inserted_tile_in_column_for_action = 0

            for i in range(column_choice + 1):

                if (rows[column_choice][i] == 0 and number_of_drawed_tile > 0):
                    rows[column_choice][i] = tile_type + 1
                    self.inserted_tile_in_column_for_action = self.inserted_tile_in_column_for_action + 1
                    number_of_drawed_tile = number_of_drawed_tile - 1

            # mette le rimanenti nella penality column
            insert_tiles_in_penalty_column(number_of_drawed_tile, player)

        self.penality_for_action = 0
        self.player_played_turn = player

        # controlla se è una mossa valida
        if self.valid_move(player, pit_choice, tile_type, column_choice):

            self.pit_choice = pit_choice
            self.color_choice = tile_type
            self.row_choice = column_choice

            drawed_tiles = take_tile_from_pit(pit_choice, tile_type, player)

            if pit_choice == 5 and self.new_first_player:
                self.initial_player = player
                self.new_first_player = False
                # aggiunge 1 penalità
                insert_tiles_in_penalty_column(1, player)

            # inserisci tile nella colonna specificata del player

            if (column_choice != 5):
                insert_tiles_in_column(tile_type, drawed_tiles, column_choice, player)
            else:
                # se 5 allora inserisci direttamente nella colonna penalità
                insert_tiles_in_penalty_column(drawed_tiles, player)

            if self.player_turn == "P1":
                self.player_turn = "P2"
            else:
                self.player_turn = "P1"

            self.action_analisys()

            return True

        return False

    def calculate_score(self, player):

        def clear_row(index_row, player):

            if (player == "P1"):
                rows = self.rows_p1
            else:
                rows = self.rows_p2

            for i in range(index_row + 1):
                rows[index_row][i] = 0

        def add_tile_to_scoreboard(tile, player, index_row):

            if (player == "P1"):
                scoreboard = self.board_p1
            else:
                scoreboard = self.board_p2

            index_column = ((tile - 1 + index_row) % 5)
            scoreboard[index_row][index_column] = 1

            # cambia nome metodi in adiacent
            score_row = compute_row_point(index_row, index_column, player)
            score_column = compute_column_point(index_row, index_column, player)

            # 1 sta per l'inserimento della piastrella
            return 1 + score_row + score_column

        def compute_row_point(index_row, index_column, player):

            if (player == "P1"):
                scoreboard = self.board_p1
            else:
                scoreboard = self.board_p2
            score = 0
            i = 0
            for elem in scoreboard[index_row]:
                if (i < index_column):
                    if (elem):
                        score = score + 1
                    else:
                        score = 0
                else:
                    if (elem):
                        score = score + 1
                    else:
                        break
                i = i + 1
            return score - 1

        def compute_column_point(index_row, index_column, player):

            if (player == "P1"):
                scoreboard = self.board_p1
            else:
                scoreboard = self.board_p2
            point = 0
            i = 0
            for row in scoreboard:

                if (i < index_row):
                    if (row[index_column]):
                        point = point + 1
                    else:
                        point = 0
                else:
                    if (row[index_column]):
                        point = point + 1
                    else:
                        break

                i = i + 1
            return point - 1

        def update_score(player, points):

            if player == "P1":
                self.p1_score = self.p1_score + points
            else:
                self.p2_score = self.p2_score + points

        def calculate_penality(player):

            if (player == "P1"):
                penality_row = self.penalty_row_p1
            else:
                penality_row = self.penalty_row_p2

            penality = 0

            for i in range(7):
                if penality_row[i]:
                    if i < 2:
                        penality = penality - 1
                    elif i < 5:
                        penality = penality - 2
                    else:
                        penality = penality - 3

            return penality

        # calcolo dello score
        if player == "P1":
            rows = self.rows_p1

        else:
            rows = self.rows_p2

        index_row = 0
        partial_score = 0

        for row in rows:
            first_elem_row = row[0]
            completed_row = True

            for elem in row:
                if elem != first_elem_row or elem == 0:
                    completed_row = False
                    break

            if completed_row:
                clear_row(index_row, player)
                partial_score += add_tile_to_scoreboard(first_elem_row, player, index_row)

            index_row = index_row + 1

        # calculate penality e aggiorna lo score finale
        penality = calculate_penality(player)
        round_end_score = partial_score + penality

        if round_end_score > 0:
            update_score(player, round_end_score)

    def valid_actions(self, player):
        valid_actions = []
        for i in range(6):
            for j in range(5):
                for k in range(6):
                    if (self.valid_move(player, i, j, k)):
                        valid_actions.append([i, j, k])
        return valid_actions

    def is_turn_done(self):
        for pit in self.drawing_pit:
            for tile_type in pit:
                if (tile_type != 0):
                    self.is_done_phase = False
                    return

        self.is_done_phase = True
        return

    def is_game_done(self):
        # controlla la board p1
        self.is_turn_done()
        if self.is_done_phase:
            for row in self.board_p1:
                completed_tiles_in_a_row = 0
                for tile in row:
                    completed_tiles_in_a_row = completed_tiles_in_a_row + tile
                if (completed_tiles_in_a_row == 5):
                    self.gameover = True
                    return

            # controlla la board p2
            for row in self.board_p2:
                completed_tiles_in_a_row = 0
                for tile in row:
                    completed_tiles_in_a_row = completed_tiles_in_a_row + tile
                if (completed_tiles_in_a_row == 5):
                    self.gameover = True
                    return

            self.gameover = False
            return
        else:
            return False

    def compute_final_points(self):

        def row_completed_score(scoreboard):

            row_completed = 0
            for row in scoreboard:
                n_tile_in_a_row = 0

                for tile in row:
                    if (tile == 1):
                        n_tile_in_a_row = n_tile_in_a_row + 1
                if (n_tile_in_a_row == 5):
                    row_completed = row_completed + 1
            return row_completed * 2

        def column_completed_score(scoreboard):

            column_completed = 0
            cumulative = [0, 0, 0, 0, 0]

            for row in scoreboard:
                cumulative = cumulative + row

            for elem in cumulative:
                if (elem == 5):
                    column_completed = column_completed + 1

            return column_completed * 5

        def tile_completed_score(scoreboard):

            tile_completed = 0
            tile_array = [0, 0, 0, 0, 0]

            for i in range(5):
                for j in range(5):
                    if (scoreboard[i][j] == 1):
                        tile_array[(i + j) % 5] = tile_array[(i + j) % 5] + 1

            for elem in tile_array:
                if (elem == 5):
                    tile_completed = tile_completed + 1

            return tile_completed * 7

        # calcola per P1
        scoreboard = self.board_p1
        self.p1_score = self.p1_score + row_completed_score(scoreboard) + column_completed_score(
            scoreboard) + tile_completed_score(scoreboard)
        # calcola per P2
        scoreboard = self.board_p2
        self.p2_score = self.p2_score + row_completed_score(scoreboard) + column_completed_score(
            scoreboard) + tile_completed_score(scoreboard)

    def action_analisys(self):

        def compute_expected_row_points(row_array, column_choice, tile_type, board):

            expected_row_points = 0

            row_choice = board[column_choice]
            index_of_inserted_element = (tile_type + column_choice) % 5
            flag = False

            for i in range(5):
                if i == index_of_inserted_element:
                    expected_row_points = expected_row_points + 1
                else:
                    if row_choice[i] == 1:
                        expected_row_points = expected_row_points + 1
                    else:
                        if flag:
                            expected_row_points = 0
                        else:
                            expected_row_points

            return expected_row_points

        def compute_expected_column_points(row_array, column_choice, tile_type, board):

            flag = False
            expected_column_points_for_action = 0

            for i in range(5):
                if i == column_choice:
                    expected_column_points_for_action = expected_column_points_for_action + 1
                    flag = True
                else:
                    if board[i][tile_type] != 0:
                        expected_column_points_for_action = expected_column_points_for_action + 1
                    else:
                        # controlla che se la row  è piena e che quindi verrà considerata successivamente come piazzata
                        for tile in row_array[i]:
                            if tile == 0:
                                if not flag:
                                    expected_column_points_for_action = 0
                                else:
                                    return expected_column_points_for_action
                            else:
                                expected_column_points_for_action = expected_column_points_for_action + 1
            return expected_column_points_for_action

        def action_analisys_row(board, column_choice):
            count_tiles_in_row = 0

            for tile in board[column_choice]:
                if tile != 0:
                    count_tiles_in_row = count_tiles_in_row + 1

            return count_tiles_in_row

        def action_analisys_column(board, tile_type):

            cumulative = np.array([0, 0, 0, 0, 0])

            for row in board:
                np.array(row)
                cumulative = np.add(cumulative, row)


            return cumulative[tile_type]

        def action_analisys_color(board, tile_type):

            tile_completed = 0
            tile_array = [0, 0, 0, 0, 0]
            i = 1

            for i in range(5):
                for j in range(5):
                    if (board[i][j] == 1):
                        tile_array[(i + j) % 5] = tile_array[(i + j) % 5] + 1 * i
                i = i + 1

            return tile_array[tile_type]

        row, column, color, expected_row_points, expected_column_point = 0, 0, 0, 0, 0

        player, tile_type, column_choice = self.player_played_turn, self.color_choice, self.row_choice

        if player == "P1":

            board = self.board_p1
            row_array = self.rows_p1

        else:

            board = self.board_p2
            row_array = self.rows_p2

        if column_choice == 5:
            return row, column, color, expected_row_points, expected_column_point

        count_tiles_in_column = 0

        for tile in row_array[column_choice]:
            if tile == (tile_type + 1):
                count_tiles_in_column = count_tiles_in_column + 1

        if count_tiles_in_column == (column_choice + 1):
            expected_row_points = compute_expected_row_points(row_array, column_choice, tile_type, board)
            expected_column_point = compute_expected_column_points(row_array, column_choice, tile_type, board)

        row = count_tiles_in_column + action_analisys_row(board, column_choice)
        column = count_tiles_in_column + action_analisys_column(board, tile_type)
        color = count_tiles_in_column + action_analisys_color(board, tile_type)

        self.analisys_row, self.analisys_column, self.analisys_color, self.analisys_expected_row_points, \
        self.analisys_column_points = row, column, color, expected_row_points, expected_column_point

        return row, column, color, expected_row_points, expected_column_point

    def from_action_to_tuple_action(self, action):

        action_pit_choice = 0
        action_tile_type = 0
        action_column_choice = 0

        if action < 6:
            action_pit_choice = action
            return action_pit_choice, action_tile_type, action_column_choice

        if action < 30:
            action_pit_choice = action % 6
            action_tile_type = int(action / 6)
            return action_pit_choice, action_tile_type, action_column_choice

        action_pit_choice = action % 6
        action_tile_type = int((action % (6 * 5)) / 6)
        action_column_choice = int(action / (6 * 5))

        return action_pit_choice, action_tile_type, action_column_choice

    def from_tuple_action_to_action(self, action_pit_choice, action_tile_type, action_column_choice):

        a = action_pit_choice
        b = action_tile_type
        c = action_column_choice

        return action_pit_choice + action_tile_type * 6 + action_column_choice * 6 * 5

    def print_table(self):

        print(f"P1:{self.p1_score}")
        print(self.board_p1)
        print(f"row_p1:{self.rows_p1}")
        print(f"penality:{self.penalty_row_p1}")
        print("=" * 20)
        print(f"P2:{self.p2_score}")
        print(self.board_p2)
        print(f"row_p2:{self.rows_p2}")
        print(f"penality:{self.penalty_row_p2}")
        print("=" * 20)
        print(self.drawing_pit)
        print("=" * 20)

    def game_to_string(self):

        board_str = ""
        board_str += f"P1:{self.p1_score}" + "\n"
        board_str += f"{self.board_p1}" + "\n"
        board_str += f"row_p1:{self.rows_p1}" + "\n"
        board_str += f"penality:{self.penalty_row_p1}" + "\n"
        board_str += "=" * 20 + "\n"
        board_str += f"P2:{self.p2_score}" + "\n"
        board_str += f"{self.board_p2}" + "\n"
        board_str += f"row_p2:{self.rows_p2}" + "\n"
        board_str += f"penality:{self.penalty_row_p2}" + "\n"
        board_str += "=" * 20 + "\n"
        board_str += f"{self.drawing_pit}" + "\n"
        board_str += "=" * 20 + "\n"

        return board_str

    def observe_board(self):

        # TODO board p1
        pd_board_p1 = pd.DataFrame(self.board_p1)
        pd_rows_p1 = pd.DataFrame(self.rows_p1).fillna(0).astype(int)
        total_board_p1 = pd.concat([pd_board_p1, pd_rows_p1], axis=1)

        # TODO board p2
        pd_board_p2 = pd.DataFrame(self.board_p2)
        pd_rows_p2 = pd.DataFrame(self.rows_p2).fillna(0).astype(int)
        total_board_p2 = pd.concat([pd_board_p2, pd_rows_p2], axis=1)

        # TODO penality and pits
        reshaped_penality_p1 = [self.penalty_row_p1[:5], self.penalty_row_p1[5:]]
        reshaped_penality_p2 = [self.penalty_row_p2[:5], self.penalty_row_p2[5:]]

        pd_penality_p1 = pd.DataFrame(reshaped_penality_p1).fillna(0).astype(int)
        pd_penality_p2 = pd.DataFrame(reshaped_penality_p2).fillna(0).astype(int)
        pd_pits = pd.DataFrame(self.drawing_pit)

        pd_penalities_and_pits = pd.concat([pd_penality_p1, pd_penality_p2, pd_pits], axis=0)

        #TODO concatena le due board dei player
        pd_both_player_board = pd.concat([total_board_p1, total_board_p2], axis=0)

        #TODO concatena la final board con pits e penality
        pd_both_player_board.reset_index(drop=True, inplace=True)
        pd_penalities_and_pits.reset_index(drop=True, inplace=True)
        final_board = pd.concat([pd_both_player_board, pd_penalities_and_pits], axis=1)


        #shape(15,10)
        return final_board.values.tolist()
