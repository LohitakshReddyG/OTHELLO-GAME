from copy import deepcopy
from constants import AI_DEPTH, WHITE, BLACK
from game_logic import Game

class AI:
    # weights
    DISC_WEIGHT = 1
    CORNER_WEIGHT = 25
    MOBILITY_WEIGHT = 5
    CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
    def __init__(self, game: Game, depth: int = AI_DEPTH):
        self.game = game
        self.depth = depth
    
    def best_move(self, board):
        # Return the best position for WHITE or None if no moves.
        moves = self.game.get_valid_moves(board, WHITE)
        if not moves:
            return None
        best_score = float('-inf')
        best_move = moves[0]
        for r, c in moves:
            new_board = deepcopy(board)
            self.game.apply_move(new_board, r, c, WHITE)
            score = self._minimax(new_board, self.depth - 1, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
    # Minimax implementation
    def _minimax(self, board, depth, alpha, beta, maximizing):
        """Recursive Minimax with Alpha‑Beta pruning.
        maximizing -> True when it is WHITE turn.
        """
        if depth == 0 or self.game.is_game_over(board):
            return self._evaluate(board)
        player = WHITE if maximizing else BLACK
        moves = self.game.get_valid_moves(board, player)
        if not moves:
            # Pass turn if no moves
            return self._minimax(board, depth - 1, alpha, beta, not maximizing)
        if maximizing:
            value = float('-inf')
            for r, c in moves:
                new_board = deepcopy(board)
                self.game.apply_move(new_board, r, c, WHITE)
                value = max(value, self._minimax(new_board, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta: #aplha-beta pruning
                    break  
            return value
        else:
            value = float('inf')
            for r, c in moves:
                new_board = deepcopy(board)
                self.game.apply_move(new_board, r, c, BLACK)
                value = min(value, self._minimax(new_board, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cut‑off
            return value
    # Evaluation function
    def _evaluate(self, board):
        """Heuristic score from WHITE's perspective.

        Considers disc difference, corner control and mobility.
        """
        black, white = self.game.score(board)
        total = black + white
        disc_score = 0 if total == 0 else 100 * (white - black) / total

        white_corners = sum(1 for r, c in self.CORNERS if board[r][c] == WHITE)
        black_corners = sum(1 for r, c in self.CORNERS if board[r][c] == BLACK)
        corner_score = white_corners - black_corners

        white_moves = len(self.game.get_valid_moves(board, WHITE))
        black_moves = len(self.game.get_valid_moves(board, BLACK))
        mobility_score = 0 if (white_moves + black_moves) == 0 else 100 * (white_moves - black_moves) / (white_moves + black_moves)

        return (
            self.DISC_WEIGHT * disc_score +
            self.CORNER_WEIGHT * corner_score +
            self.MOBILITY_WEIGHT * mobility_score
        )
