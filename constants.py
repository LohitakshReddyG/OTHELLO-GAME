"""Essential constants for Othello.

Only the values needed for game logic and a minimal UI are kept.
"""

# Board pieces
EMPTY = 0
BLACK = 1   # Human player
WHITE = 2   # AI player

# Board dimensions
BOARD_SIZE = 8
CELL_SIZE = 70  # pixel size for each cell (used by UI)

# Directions for disc flipping (8 neighbours)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

# AI search depth (simple default)
AI_DEPTH = 3
