# Author: Carrie Barrett
# Date: 11/22/2020
# Description: a class named FocusGame for playing an abstract board
# game called Focus/Domination. You can see the rules here:
# https://en.wikipedia.org/wiki/Focus_%28board_game%29.


class FocusGame:
    """
    A class named FocusGame that will interact with the Player and
    Board classes in order to model an abstract board game called
    Focus/Domination.
    """

    def __init__(self, player_1, player_2):
        """
        Initializes the board with the pieces placed in the correct
        positions
        :param player_1: tuple containing player name and color of the
        piece one player is playing (ex: ('PlayerA', 'R'))
        :param player_2: same as above for second player
        """
        self._player_turn = ""
        self._game_state = "UNFINISHED"
        self._player_1 = Player(player_1[0], player_1[1])
        self._player_2 = Player(player_2[0], player_2[1])
        self._game_board = Board(player_1[1], player_2[1])

    def move_piece(self, player, move_from,  move_to, pieces):
        """
        Makes a move (after determining if the move is valid)
        :param player: name of the player making the move
        :param move_from: tuple representing coordinate from where the
        move is being made
        :param move_to: tuple representing location to where the move
        is being made
        :param pieces: integer number of pieces being moved
        :return: an error or a proper message
        """
        # get the selected player object if the player exists
        if self._player_1.get_name() == player:
            selected_player = self._player_1
        elif self._player_2.get_name() == player:
            selected_player = self._player_2
        else:
            return False

        # if it's the first move, set the player turn to given player
        if self._player_turn == "":
            self._player_turn = player

        # check if it is the given player's turn
        if self._player_turn != player:
            return False

        # make a move
        # check if locations are on the board
        if move_from[0] < 0 or move_from[0] > 5 or move_from[1] < 0 \
                or move_from[1] > 5 or move_to[0] < 0 or move_to[0] > 5 \
                or move_to[1] < 0 or move_to[1] > 5:
            return False

        # check if player controls that stack
        if self.show_pieces(move_from)[-1] != selected_player.get_color():
            return False

        # check if stack has required number of pieces
        if len(self.show_pieces(move_from)) < pieces:
            return False

        # make sure move is not diagonal
        if move_from[0] != move_to[0] and move_from[1] != move_to[1]:
            return False

        # make sure number of pieces equals spaces moved
        if move_from[0] == move_to[0]:          # if row is same
            if abs(move_to[1] - move_from[1]) != pieces:
                return False
        if move_from[1] == move_to[1]:          # if column is same
            if abs(move_to[0] - move_from[0]) != pieces:
                return False

        # move the stack
        return self.move_stack(selected_player, move_from, move_to, pieces)

    def move_stack(self, selected_player, move_from, move_to, pieces):
        """
        Helper function that moves a stack of pieces from one location
        to another
        :param selected_player: player object that is moving the stack
        :param move_from: tuple representing coordinate from where the
        move is being made
        :param move_to: tuple representing location to where the move
        is being made
        :param pieces: integer number of pieces being moved
        :return: 'successfully moved' message if the move was successful
        """
        starting_stack = self.show_pieces(move_from)

        # add the selected pieces to the moving_stack
        moving_stack = []
        for i in range(len(starting_stack)-pieces, len(starting_stack)):
            moving_stack.append(starting_stack[i])

        # add the remaining pieces to the new stack
        new_starting_stack = []
        for i in range(0, len(starting_stack)-pieces):
            new_starting_stack.append(starting_stack[i])

        # set the starting location stack to be new starting stack
        self._game_board.set_stack(new_starting_stack, move_from)

        # add the moving stack on to the stack at the new location
        self.add_to_stack(move_to, moving_stack, selected_player)

        # end turn
        return self.end_turn(selected_player)

    def add_to_stack(self, move_to, moving_stack, selected_player):
        """
        Adds a stack on top of a previous stack and handles reserved
        and captured pieces
        :param move_to: location stack is moving to
        :param moving_stack: list representing the stack to move
        :param selected_player: player making the move
        """
        ending_stack = self.show_pieces(move_to) + moving_stack
        if len(ending_stack) <= 5:
            self._game_board.set_stack(ending_stack, move_to)

        else:
            for i in range(0, len(ending_stack) - 5):
                if ending_stack[i] == selected_player.get_color():
                    selected_player.add_reserved()
                else:
                    selected_player.add_captured()

            # remove extra pieces from beginning of ending stack
            new_ending_stack = []
            for i in range(len(ending_stack) - 5, len(ending_stack)):
                new_ending_stack.append(ending_stack[i])

            # set the ending location to the new ending stack
            self._game_board.set_stack(new_ending_stack, move_to)

    def end_turn(self, selected_player):
        """
        Checks for win, if game is not won changes the player turn from
        selected player to the next player, update game state
        :param selected_player: the current player
        :return: '<player name> wins' if game is won, 'successfully
        moved' otherwise
        """
        # checks for win
        if self._player_1.get_captured() >= 6:
            self._game_state = "FINISHED"
            return self._player_1.get_name() + " Wins"
        elif self._player_2.get_captured() >= 6:
            self._game_state = "FINISHED"
            return self._player_2.get_name() + " Wins"

        # updates player turn
        else:
            if selected_player is self._player_1:
                self._player_turn = self._player_2.get_name()
            else:
                self._player_turn = self._player_1.get_name()
            return "successfully moved"

    def show_pieces(self, position):
        """
        Takes a position on the board and returns a list showing the
        pieces that are present at that location with the bottom-most
        pieces at the 0th index and other pieces on it in order
        :param position: tuple representing a position on the board
        :return: a list showing the pieces that are present at that
        location
        """
        return self._game_board.get_stack(position)

    def show_reserve(self, player):
        """
        Shows the count of pieces that are in reserve for a player
        :param player: player name
        :return: number of pieces the player has in reserve (0 if none)
        """
        if self._player_1.get_name() == player:
            return self._player_1.get_reserved()

        if self._player_2.get_name() == player:
            return self._player_2.get_reserved()

        else:
            return False

    def show_captured(self, player):
        """
        Shows the number of pieces captured by a player
        :param player: player name
        :return: number of pieces captured by that player (0 if none)
        """
        if self._player_1.get_name() == player:
            return self._player_1.get_captured()

        if self._player_2.get_name() == player:
            return self._player_2.get_captured()

        else:
            return False

    def reserved_move(self, player, move_to):
        """
        Places the piece from the reserve to the location
        :param player: player name
        :param move_to: tuple representing location to where the move
        is being made
        :return: If there are no pieces in reserve, return 'no pieces
        in reserve'
        """
        # get the selected player object if the player exists
        if self._player_1.get_name() == player:
            selected_player = self._player_1
        elif self._player_2.get_name() == player:
            selected_player = self._player_2
        else:
            return False

        # check if it is the given player's turn
        if self._player_turn != player:
            return False

        # check if locations are on the board
        if move_to[0] < 0 or move_to[0] > 5 or move_to[1] < 0 or move_to[1] > 5:
            return False

        # check if player has any pieces in reserve
        if selected_player.get_reserved() < 1:
            return False

        # make a one-piece moving stack from reserved piece
        moving_stack = [selected_player.get_color()]

        # add the moving stack on to the stack at the new location
        self.add_to_stack(move_to, moving_stack, selected_player)

        # update reserved pieces
        selected_player.decrease_reserved()

        # end turn
        return self.end_turn(selected_player)

    def print_game_board(self):
        """
        prints the board
        """
        self._game_board.print_board()


class Player:
    """
    A class named Player that will interact with the FocusGame and
    Board classes in order to model an abstract board game called
    Focus/Domination.
    """

    def __init__(self, player_name, player_color):
        """
        Initializes the player with 0 captured and 0 reserved pieces
        """
        self._name = player_name
        self._color = player_color
        self._captured = 0
        self._reserved = 0

    def get_name(self):
        """
        A getter function for the name of the player
        :return: name of player
        """
        return self._name

    def get_color(self):
        """
        A getter function for the color of the player
        :return: the player color
        """
        return self._color

    def get_captured(self):
        """
        A getter function for the number of pieces captured by player
        :return: number of pieces captured by the player
        """
        return self._captured

    def add_captured(self):
        """
        increases the number of captured pieces by 1
        """
        self._captured += 1

    def get_reserved(self):
        """
        A getter function for the number of pieces reserved by player
        :return: number of pieces reserved by the player
        """
        return self._reserved

    def add_reserved(self):
        """
        increases the number of reserved pieces by 1
        """
        self._reserved += 1

    def decrease_reserved(self):
        """
        decreases the number of reserved pieces by 1
        """
        self._reserved -= 1


class Board:
    """
    A class named Board that will interact with the FocusGame and
    Player classes in order to model an abstract board game called
    Focus/Domination.
    """

    def __init__(self, color_1, color_2):
        """
        Initializes the board with the pieces placed in the correct
        locations
        """
        self._layout = [[[color_1], [color_1], [color_2], [color_2], [color_1], [color_1]],
                        [[color_2], [color_2], [color_1], [color_1], [color_2], [color_2]],
                        [[color_1], [color_1], [color_2], [color_2], [color_1], [color_1]],
                        [[color_2], [color_2], [color_1], [color_1], [color_2], [color_2]],
                        [[color_1], [color_1], [color_2], [color_2], [color_1], [color_1]],
                        [[color_2], [color_2], [color_1], [color_1], [color_2], [color_2]]]

    def get_stack(self, coordinates):
        """
        A getter function for the stack at a location on the board
        :param coordinates: a tuple representing the coordinates of the
        space on the board where we want to know what is in the stack
        :return: a list of all the items in the stack at that position
        """
        return self._layout[coordinates[0]][coordinates[1]]

    def set_stack(self, stack_list, coordinates):
        """
        Sets the stack at a given location to a given list
        :param stack_list: list representing the new stack
        :param coordinates: tuple representing the coordinates of the
        space on the board where we want to put the new stack
        """
        self._layout[coordinates[0]][coordinates[1]] = stack_list

    def print_board(self):
        """
        prints the board
        """
        for i in range(0, 6):
            print(self._layout[i])
