"""Game logic for Othello.

This module defines the `Game` class which encapsulates the board state,
move validation, disc flipping and basic scoring. It is deliberately free
of any UI code so it can be reused or unit‑tested independently.
"""

from constants import EMPTY, BLACK, WHITE, BOARD_SIZE, DIRECTIONS


class Game:
    """Manages the Othello board state and core rules.
    The board is represented as a list of lists of integers where:
        EMPTY = 0, BLACK = 1 (human), WHITE = 2 (AI).
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Initialise a fresh board with the standard four centre discs."""
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        mid = BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = WHITE
        self.board[mid - 1][mid] = BLACK
        self.board[mid][mid - 1] = BLACK
        self.board[mid][mid] = WHITE
        self.current_player = BLACK  # Black always moves first

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------
    def is_on_board(self, r: int, c: int) -> bool:
        """Return ``True`` if ``(r, c)`` lies inside the 8×8 board."""
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    # ------------------------------------------------------------------
    # Move validation
    # ------------------------------------------------------------------
    def get_flips(self, board, r: int, c: int, player: int):
        """Return a list of positions that would be flipped for ``player``.

        If the square is not empty or no direction yields a capture, an empty
        list is returned.
        """
        if board[r][c] != EMPTY:
            return []

        opponent = WHITE if player == BLACK else BLACK
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            nr, nc = r + dr, c + dc
            while self.is_on_board(nr, nc) and board[nr][nc] == opponent:
                line.append((nr, nc))
                nr += dr
                nc += dc
            if line and self.is_on_board(nr, nc) and board[nr][nc] == player:
                flips.extend(line)
        return flips

    def is_valid_move(self, board, r: int, c: int, player: int) -> bool:
        """A move is legal when at least one disc would be flipped."""
        return bool(self.get_flips(board, r, c, player))

    def get_valid_moves(self, board, player: int):
        """Return a list of ``(row, col)`` tuples representing legal moves."""
        return [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.is_valid_move(board, r, c, player)
        ]

    # ------------------------------------------------------------------
    # State mutation
    # ------------------------------------------------------------------
    def apply_move(self, board, r: int, c: int, player: int):
        """Place ``player``'s disc at ``(r, c)`` and flip the captured discs.

        The function mutates ``board`` in‑place and returns the list of flipped
        positions for possible UI highlighting.
        """
        flips = self.get_flips(board, r, c, player)
        board[r][c] = player
        for fr, fc in flips:
            board[fr][fc] = player
        return flips

    # ------------------------------------------------------------------
    # Scoring and termination helpers
    # ------------------------------------------------------------------
    def score(self, board):
        """Return a tuple ``(black_count, white_count)`` of disc totals."""
        black = sum(row.count(BLACK) for row in board)
        white = sum(row.count(WHITE) for row in board)
        return black, white

    def is_game_over(self, board) -> bool:
        """The game ends when neither player has a legal move."""
        return not self.get_valid_moves(board, BLACK) and not self.get_valid_moves(board, WHITE)

    # ------------------------------------------------------------------
    # Human convenience wrapper
    # ------------------------------------------------------------------
    def human_move(self, r: int, c: int) -> bool:
        """Attempt a human (BLACK) move; return ``True`` if successful."""
        if self.is_valid_move(self.board, r, c, BLACK):
            self.apply_move(self.board, r, c, BLACK)
            return True
        return False
