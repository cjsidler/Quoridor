#  Quoridor by Collin Sidler
#  Quoridor board game for two players. Players take turns placing a fence or
#  moving their pawn. Each player starts with 10 fences. Each fence blocks two
#  tiles. Player wins by moving their pawn to the opponent's baseline.

class QuoridorGame:
    """
    Class that represents the board game Quoridor.
    """

    def __init__(self):
        """
        Initializes a new QuoridorGame with 9x9 board tiles and 10x10 vertices for fences.
        _board will be filled with Tile objects, _fences with Fence objects.
        _fences will start with fences placed around the 4 edges of the board.
        Each player starts with 10 placeable fences.
        _turn will store the player (1 or 2) whose turn it is.
        """
        self._p1_fences = 10
        self._p2_fences = 10
        self._turn = 1
        self._p1_loc = (0, 4)
        self._p2_loc = (8, 4)
        self._ortho_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self._diag_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self._jump_dirs = [(-2, 0), (2, 0), (0, 2), (0, -2)]
        self._selected = False

        self._board = []
        for x in range(9):
            board_row = []
            for y in range(9):
                new_tile = Tile(x, y)
                if x == 0 and y == 4:
                    new_tile.set_piece(1)
                elif x == 8 and y == 4:
                    new_tile.set_piece(2)
                board_row.append(new_tile)
            self._board.append(board_row)

        self._fences = []
        for x in range(10):
            fence_row = []
            for y in range(10):
                new_fence = Fence(x, y)
                if x == 0 and y < 9:
                    new_fence.set_h_fence(True)
                if y == 0 and x < 9:
                    new_fence.set_v_fence(True)
                if y == 9 and x < 9:
                    new_fence.set_v_fence(True)
                if x == 9 and y < 9:
                    new_fence.set_h_fence(True)
                fence_row.append(new_fence)
            self._fences.append(fence_row)

    def get_selected(self):
        """
        Gets the current status of whether the player's pawn whose turn it is was selected.
        """
        return self._selected

    def set_selected(self, status):
        """
        Sets current status of whether the player's pawn whose turn it is was selected.
        """
        if type(status) is not bool:
            return
        self._selected = status

    def toggle_selected(self):
        """
        Toggles the current status of whether the player's pawn whose turn it is has been selected.
        """
        if self._selected is True:
            self._selected = False
        else:
            self._selected = True

    def get_ortho_dirs(self):
        """Returns orthogonal move directions."""
        return self._ortho_dirs

    def get_diag_dirs(self):
        """Returns diagonal move directions."""
        return self._diag_dirs

    def get_jump_dirs(self):
        """Returns pawn jump move directions."""
        return self._jump_dirs

    def get_player_loc(self, player):
        """Returns the coords for the given player's pawn."""
        if player == 1:
            return self._p1_loc
        return self._p2_loc

    def set_player_loc(self, player, coords):
        """Sets the location of player's pawn."""
        if player == 1:
            self._p1_loc = coords
        else:
            self._p2_loc = coords

    def get_turn(self):
        """Returns 1 or 2 depending on which player's turn it is."""
        return self._turn

    def update_turn(self):
        """Updates whose turn it is (1 or 2) by toggling the value in the _turn data member."""
        if self.get_turn() == 1:
            self._turn = 2
        else:
            self._turn = 1

    def player_fences(self, player):
        """Returns the number of remaining fences that the given player has left to place."""
        if player == 1:
            return self._p1_fences
        elif player == 2:
            return self._p2_fences

    def use_fence(self, player):
        """Decrements available fences for given player."""
        if player == 1:
            if self.player_fences(1) > 0:
                self._p1_fences -= 1
                return True
            return False
        if self.player_fences(2) > 0:
            self._p2_fences -= 1
            return True
        return False

    def get_board(self):
        """Returns the game board (2D array of Tile objects)."""
        return self._board

    def get_fences(self):
        """Returns the board's fences (2D array of Fence objects)."""
        return self._fences

    def move_pawn(self, player, coords):
        """
        Allows a player to move their pawn.
        Takes following two parameters in order:
            an integer that represents which player (1 or 2) is making the move
            a tuple with the coordinates of where the pawn is going to be moved to.
        """

        # if game over, not player's turn, out of bounds, or destination occupied return False
        dest_x, dest_y = coords
        if self.is_winner(1) or self.is_winner(2) or self.get_turn() != player:
            return False
        elif not 0 <= dest_x < 9 or not 0 <= dest_y < 9:
            return False
        elif self.get_board()[dest_x][dest_y].get_piece():
            return False

        start_x, start_y = self.get_player_loc(player)

        if player == 1:
            opp_x, opp_y = self.get_player_loc(2)
        else:
            opp_x, opp_y = self.get_player_loc(1)

        if not self.check_move(start_x, start_y, opp_x, opp_y, dest_x, dest_y):
            return False

        self.update_board(player, start_x, start_y, dest_x, dest_y)
        self.update_turn()
        return True

    def check_move(self, start_x, start_y, opp_x, opp_y, dest_x, dest_y):
        """
        Checks whether the attempted move is valid given the starting, opponent, and destination locations.
        Returns True if valid move.
        Move must be in ortho_dirs, diag_dirs, or jump_dirs.
        Orthogonal move must have no fence between.
        Diagonal move must have:
            Fence behind opponent pawn from direction of player pawn.
        Diagonal move and Jump move must have:
            Player pawn orthogonal to opponent pawn with no fence between
            Opponent pawn orthogonal to destination pawn with no fence between
        """

        move = (dest_x - start_x, dest_y - start_y)

        if move not in self.get_ortho_dirs() + self.get_diag_dirs() + self.get_jump_dirs():
            return False
        elif opp_x == dest_x and opp_y == dest_y:
            return False
        elif move in self.get_ortho_dirs():
            return not self.check_fence(start_x, start_y, dest_x, dest_y)
        elif move in self.get_diag_dirs():
            if not self.check_fence_behind(start_x, start_y, opp_x, opp_y):
                return False
            elif not self.check_next_to(start_x, start_y, opp_x, opp_y, dest_x, dest_y):
                return False
            elif self.check_fence(start_x, start_y, opp_x, opp_y):
                return False
            elif self.check_fence(opp_x, opp_y, dest_x, dest_y):
                return False
        elif move in self.get_jump_dirs():
            if not self.check_next_to(start_x, start_y, opp_x, opp_y, dest_x, dest_y):
                return False
            elif self.check_fence(start_x, start_y, opp_x, opp_y):
                return False
            elif self.check_fence(opp_x, opp_y, dest_x, dest_y):
                return False

        return True

    def get_valid_destinations(self):
        """
        Returns a list of tuples for all valid destination tiles from the current player's location.
        """

        valid_moves = []
        
        player = self.get_turn()

        if player == 1:
            opp = 2
        else:
            opp = 1
            
        player_x, player_y = self.get_player_loc(player)
        opp_x, opp_y = self.get_player_loc(opp)

        for move in self.get_ortho_dirs() + self.get_jump_dirs() + self.get_diag_dirs():
            move_x, move_y = move
            dest_x, dest_y = player_x + move_x, player_y + move_y
            if self.check_move(player_x, player_y, opp_x, opp_y, dest_x, dest_y):
                valid_moves.append((dest_x, dest_y))

        return valid_moves

    def check_fence_behind(self, x1, y1, x2, y2):
        """
        Checks if there is a fence behind the destination's Tile.
        Used to determine if diagonal moves are valid.
        """
        move_opp = (x2 - x1, y2 - y1)

        if move_opp == (-1, 0):
            # check if opp Tile has h_fence
            return self.get_fences()[x2][y2].get_h_fence()
        elif move_opp == (0, -1):
            # check if opp Tile has v_fence
            return self.get_fences()[x2][y2].get_v_fence()
        elif move_opp == (1, 0):
            # check if Tile below opp has h_fence
            return self.get_fences()[x2+1][y2].get_h_fence()
        elif move_opp == (0, 1):
            # check if Tile to right of opp has v_fence
            return self.get_fences()[x2][y2+1].get_v_fence()

    def check_next_to(self, start_x, start_y, opp_x, opp_y, dest_x, dest_y):
        """
        Verifies that both the player pawn and opponent pawn as well as the opponent
        pawn and the destination tile are within one orthogonal space of each other.
        Both must be true for a valid diagonal move or valid pawn jump move.
        """
        if (opp_x - start_x, opp_y - start_y) not in self.get_ortho_dirs():
            return False
        elif (dest_x - opp_x, dest_y - opp_y) not in self.get_ortho_dirs():
            return False
        return True

    def update_board(self, player, x1, y1, x2, y2):
        """
        Moves the given player's pawn from start Tile to destination Tile.
        """
        self.set_player_loc(player, (x2, y2))
        self.get_board()[x2][y2].set_piece(player)
        self.get_board()[x1][y1].set_piece(None)

    def check_fence(self, x1, y1, x2, y2):
        """
        Checks if there is a fence in-between given coordinates.
        Coordinates must be within one space orthogonally.
        Returns True if there is a fence, False if not.
        """

        move = (x2 - x1, y2 - y1)

        if move == (-1, 0):
            return self.get_fences()[x1][y1].get_h_fence()
        elif move == (0, -1):
            return self.get_fences()[x1][y1].get_v_fence()
        elif move == (1, 0):
            return self.get_fences()[x2][y2].get_h_fence()
        elif move == (0, 1):
            return self.get_fences()[x2][y2].get_v_fence()

    def place_fence(self, player, pos, coords):
        """
        Allows a player to place a fence at the given coords in the given orientation.
        Takes following parameters in order:
            an integer that represents which player (1 or 2) is making the move
            a letter indicating whether it is vertical (v) or horizontal (h) fence
            a tuple of integers that represents the position on which the fence is to be placed
        """
        # if game already won or not their turn/no remaining fences, return False
        if self.is_winner(1) or self.is_winner(2):
            return False
        elif self.get_turn() != player or self.player_fences(player) == 0:
            return False

        # if placing vertical fence:
        # must not be vertical fence in current or below vertex
        # below left vertex must not have h_fence_start

        # if placing horizontal fence:
        # must not be horizontal fence in current or right vertex
        # above right vertex must not have v_fence_start

        x, y = coords

        # placement of fence must be within board boundaries and allowing for two fences
        if pos == 'h' and (not 1 <= x < 9 or not 0 <= y < 8):
            return False
        elif pos == 'v' and (not 0 <= x < 8 or not 1 <= y < 9):
            return False

        # if already fence there or next spot over, return False
        if pos == 'h' and (self.get_fences()[x][y].get_h_fence() or self.get_fences()[x][y+1].get_h_fence()):
            return False
        elif pos == 'v' and (self.get_fences()[x][y].get_v_fence() or self.get_fences()[x+1][y].get_v_fence()):
            return False

        # if placing vertical fence, below left vertex h_fence_start must be False
        if pos == 'v' and self.get_fences()[x+1][y-1].get_h_fence_start():
            return False
        # if placing horizontal fence, above right vertex v_fence_start must be False
        elif pos == 'h' and self.get_fences()[x-1][y+1].get_v_fence_start():
            return False

        # place fences and check fair play
        # if fair play not broken, update player turn and return True
        if pos == 'h':
            self.get_fences()[x][y].set_h_fence(True)
            self.get_fences()[x][y].set_h_fence_start(True)
            self.get_fences()[x][y+1].set_h_fence(True)

            if not self.check_fair_play(1) or not self.check_fair_play(2):
                self.get_fences()[x][y].set_h_fence(False)
                self.get_fences()[x][y].set_h_fence_start(False)
                self.get_fences()[x][y+1].set_h_fence(False)
                print('breaks fair play')
                return False

        elif pos == 'v':
            self.get_fences()[x][y].set_v_fence(True)
            self.get_fences()[x][y].set_v_fence_start(True)
            self.get_fences()[x+1][y].set_v_fence(True)

            if not self.check_fair_play(1) or not self.check_fair_play(2):
                self.get_fences()[x][y].set_v_fence(False)
                self.get_fences()[x][y].set_v_fence_start(False)
                self.get_fences()[x+1][y].set_v_fence(False)
                print('breaks fair play')
                return False

        self.update_turn()
        self.use_fence(player)
        return True

    def is_winner(self, player):
        """
        Returns True if the given player (1 or 2) has won, False if not.
        """
        if player == 2:
            for tile in self.get_board()[0]:
                if tile.get_piece() == player:
                    return True
            return False
        elif player == 1:
            for tile in self.get_board()[8]:
                if tile.get_piece() == player:
                    return True
            return False

    def check_fair_play(self, player, prev_indices=None, current_coords=None):
        """
        Checks if an attempted fence placement breaks fair play rules for a given player (1 or 2).
        The fence placement must not prevent a player from being able to reach a winning tile.
        Returns True if fair play is followed, returns False if fair play broken.
        """

        if current_coords is None and prev_indices is None:
            current_coords = self.get_player_loc(player)
            prev_indices = set()
            prev_indices.add(current_coords)

        new_moves = []

        # base case
        #   if player == 1 and (8, y) in prev_indices, there's still a path to win, return True
        #   elif player == 2 and (0, y) in prev_indices, there's still a path to win, return True
        for loc in prev_indices:
            if loc[0] == 8 and player == 1:
                return True
            elif loc[0] == 0 and player == 2:
                return True

        # now we'll have a set with the player's current coords
        start_x, start_y = current_coords

        # for each move in _ortho_dirs
        #   if not blocked by fence in that direction, not off board, and
        #   coords not already in prev_indices, add coords to prev_indices
        for move in self.get_ortho_dirs():
            move_x, move_y = move

            dest_x = start_x + move_x
            dest_y = start_y + move_y

            if 0 <= dest_x < 9 and 0 <= dest_y < 9 and (dest_x, dest_y) not in prev_indices:
                if not self.check_fence(start_x, start_y, dest_x, dest_y):
                    prev_indices.add((dest_x, dest_y))
                    new_moves.append((dest_x, dest_y))

        # call check_fair_play again with same player and current prev_indices
        if len(new_moves) == 1:
            return self.check_fair_play(player, prev_indices, new_moves[0])
        elif len(new_moves) == 2:
            return self.check_fair_play(player, prev_indices, new_moves[0]) or \
                   self.check_fair_play(player, prev_indices, new_moves[1])
        elif len(new_moves) == 3:
            return self.check_fair_play(player, prev_indices, new_moves[0]) or \
                   self.check_fair_play(player, prev_indices, new_moves[1]) or \
                   self.check_fair_play(player, prev_indices, new_moves[2])
        elif len(new_moves) == 4:
            return self.check_fair_play(player, prev_indices, new_moves[0]) or \
                   self.check_fair_play(player, prev_indices, new_moves[1]) or \
                   self.check_fair_play(player, prev_indices, new_moves[2]) or \
                   self.check_fair_play(player, prev_indices, new_moves[3])

        return False  # breaks fair play rule if we didn't find a 'return True' scenario above

    def print_board(self):
        """
        Prints the board to the console.
        """

        for row in range(19):
            if row % 2 == 0:
                for fence in self.get_fences()[int(row/2)]:
                    print('·', end='')
                    if fence.get_h_fence():
                        print(' ━━━ ', end='')
                    else:
                        print('     ', end='')
                print()
            else:
                for col in range(19):
                    if col % 2 == 0:
                        if self.get_fences()[int((row-1)/2)][int(col/2)].get_v_fence():
                            print('┃', end='')
                        else:
                            print(' ', end='')
                    else:
                        if self.get_board()[int((row-1)/2)][int((col-1)/2)].get_piece() == 1:
                            print(' P 1 ', end='')
                        elif self.get_board()[int((row - 1) / 2)][int((col - 1) / 2)].get_piece() == 2:
                            print(' P 2 ', end='')
                        else:
                            print('     ', end='')
                print()


class Fence:
    """
    Class that represents a Quoridor fence vertex.
    Each vertex can have a horizontal fence and vertical fence.
    _fence_start will store True if vertex is starting point of fence.
    """

    def __init__(self, x, y):
        """
        Initializes a new Quoridor fence vertex with given coordinates.
        """
        self._coords = (x, y)
        self._h_fence = False
        self._v_fence = False
        self._h_fence_start = False
        self._v_fence_start = False

    def get_coords(self):
        """Returns vertex's coordinates."""
        return self._coords

    def get_h_fence(self):
        """Returns True/False if horizontal fence to the right of vertex."""
        return self._h_fence

    def set_h_fence(self, state):
        """Adds a horizontal fence to the right of vertex."""
        self._h_fence = state

    def get_v_fence(self):
        """Returns True/False if vertical fence below vertex."""
        return self._v_fence

    def set_v_fence(self, state):
        """Adds a vertical fence below the vertex."""
        self._v_fence = state

    def get_h_fence_start(self):
        """Returns True/False if a horizontal fence starts from the fence vertex."""
        return self._h_fence_start

    def set_h_fence_start(self, state):
        """Sets whether a horizontal fence starts from the fence vertex."""
        self._h_fence_start = state

    def get_v_fence_start(self):
        """Returns True/False if a vertical fence starts from the fence vertex."""
        return self._v_fence_start

    def set_v_fence_start(self, state):
        """Sets whether a vertical fence starts from the fence vertex."""
        self._v_fence_start = state


class Tile:
    """
    Class that represents a Quoridor game tile.
    Each game tile can be occupied by 1 or 2 (None if unoccupied).
    """

    def __init__(self, x, y):
        """
        Initializes a new Quoridor game tile with given coordinates.
        """
        self._coords = (x, y)
        self._piece = None

    def get_coords(self):
        """Returns tile's coordinates."""
        return self._coords

    def get_piece(self):
        """Returns 1 or 2 if player's pawn occupies space; None if unoccupied."""
        return self._piece

    def set_piece(self, player):
        """Sets whether 1 or 2 occupies tile (None if unoccupied)."""
        self._piece = player
