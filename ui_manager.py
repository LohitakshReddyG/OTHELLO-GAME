"""UI manager for Othello using Tkinter.

This module defines the UI class that builds the window, draws the board,
handles user interaction and coordinates with the Game logic and AI engine.
"""

import tkinter as tk
from tkinter import messagebox

from constants import (
    BOARD_SIZE,
    CELL_SIZE,
    BLACK,
    WHITE,
    BLACK_COLOR,
    WHITE_COLOR,
    BOARD_COLOR,
    GRID_COLOR,
    HINT_COLOR,
    BG_COLOR,
    HIGHLIGHT_COLOR
)

from game_logic import Game
from ai_engine import AI


class UI:
    """Tkinter interface for the Othello game.

    Human (BLACK) plays against the AI (WHITE). The UI shows the board,
    valid‑move hints for the human player, current turn, scores and a
    restart button.
    """

    # Colours – defined in constants for easy theming
    # (fallback defaults kept for backward compatibility)
    BG_COLOR = BG_COLOR
    BOARD_COLOR = BOARD_COLOR
    GRID_COLOR = GRID_COLOR
    BLACK_COLOR = BLACK_COLOR
    WHITE_COLOR = WHITE_COLOR
    HINT_COLOR = HINT_COLOR
    HIGHLIGHT_COLOR = HIGHLIGHT_COLOR

    def __init__(self, root: tk.Tk):
        self.root = root
        self.game = Game()
        self.ai = AI(self.game)
        self.ai_thinking = False
        self._build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.root.title("Othello — Human (Black) vs AI (White)")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        # Top info bar
        info_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=8)
        info_frame.pack(fill=tk.X, padx=10)
        self.turn_label = tk.Label(
            info_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg=self.BG_COLOR,
            fg="white",
        )
        self.turn_label.pack(side=tk.LEFT)
        self.score_label = tk.Label(
            info_frame,
            text="",
            font=("Helvetica", 14),
            bg=self.BG_COLOR,
            fg="white",
        )
        self.score_label.pack(side=tk.RIGHT)

        # Board canvas
        canvas_size = BOARD_SIZE * CELL_SIZE
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg=self.BOARD_COLOR,
            highlightthickness=2,
            highlightbackground="#52b788",
        )
        self.canvas.pack(padx=10, pady=4)
        self.canvas.bind("<Button-1>", self._on_click)

        # Bottom bar with Restart button
        bottom_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=6)
        bottom_frame.pack(fill=tk.X, padx=10)
        restart_btn = tk.Button(
            bottom_frame,
            text="Restart Game",
            command=self._restart,
            font=("Helvetica", 11, "bold"),
            bg="#52b788",
            fg="white",
            activebackground="#74c69d",
            relief=tk.FLAT,
            padx=12,
            pady=4,
        )
        restart_btn.pack(side=tk.LEFT)
        self.status_label = tk.Label(
            bottom_frame,
            text="",
            font=("Helvetica", 10, "italic"),
            bg=self.BG_COLOR,
            fg="#adb5bd",
        )
        self.status_label.pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def _draw_board(self):
        self.canvas.delete("all")
        size = BOARD_SIZE * CELL_SIZE
        for i in range(BOARD_SIZE + 1):
            pos = i * CELL_SIZE
            self.canvas.create_line(pos, 0, pos, size, fill=self.GRID_COLOR, width=1)
            self.canvas.create_line(0, pos, size, pos, fill=self.GRID_COLOR, width=1)
        # Standard Othello star points (optional visual aid)
        for r, c in [(2, 2), (2, 5), (5, 2), (5, 5)]:
            cx = c * CELL_SIZE + CELL_SIZE // 2
            cy = r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=self.GRID_COLOR, outline="")

    def _draw_discs(self):
        pad = 6
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.game.board[r][c]
                if val == 0:
                    continue
                x1 = c * CELL_SIZE + pad
                y1 = r * CELL_SIZE + pad
                x2 = (c + 1) * CELL_SIZE - pad
                y2 = (r + 1) * CELL_SIZE - pad
                colour = self.BLACK_COLOR if val == BLACK else self.WHITE_COLOR
                self.canvas.create_oval(x1, y1, x2, y2, fill=colour, outline="", width=0)

    def _draw_hints(self, moves):
        half = CELL_SIZE // 2
        radius = 6
        for r, c in moves:
            cx = c * CELL_SIZE + half
            cy = r * CELL_SIZE + half
            self.canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                fill=self.HINT_COLOR,
                outline="",
            )

    # ------------------------------------------------------------------
    # Refresh UI
    # ------------------------------------------------------------------
    def refresh(self):
        board = self.game.board
        player = self.game.current_player
        valid = self.game.get_valid_moves(board, player)
        black, white = self.game.score(board)
        self._draw_board()
        self._draw_discs()
        if player == BLACK:
            self._draw_hints(valid)
        self.turn_label.config(text="⚫ Your Turn (Black)" if player == BLACK else "⚪ AI Thinking… (White)")
        self.score_label.config(text=f"⚫ {black} | ⚪ {white}")
        if self.game.is_game_over(board):
            self._show_result(black, white)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _on_click(self, event):
        if self.game.current_player != BLACK or self.ai_thinking:
            return
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if not self.game.is_on_board(r, c):
            return
        if not self.game.human_move(r, c):
            self.status_label.config(text="Invalid move — click a highlighted square.")
            return
        self.status_label.config(text="")
        self._advance_turn()

    def _advance_turn(self):
        board = self.game.board
        next_player = WHITE if self.game.current_player == BLACK else BLACK
        if self.game.get_valid_moves(board, next_player):
            self.game.current_player = next_player
        elif self.game.get_valid_moves(board, self.game.current_player):
            skipped = "White" if next_player == WHITE else "Black"
            self.status_label.config(text=f"{skipped} has no moves — turn skipped.")
        else:
            self.game.current_player = next_player
            self.refresh()
            return
        self.refresh()
        if self.game.current_player == WHITE and not self.game.is_game_over(board):
            self.ai_thinking = True
            self.root.after(300, self._ai_move)

    def _ai_move(self):
        board = self.game.board
        move = self.ai.best_move(board)
        if move:
            r, c = move
            self.game.apply_move(board, r, c, WHITE)
        self.ai_thinking = False
        self._advance_turn()

    def _restart(self):
        self.game.reset()
        self.ai_thinking = False
        self.status_label.config(text="")
        self.refresh()

    def _show_result(self, black, white):
        if black > white:
            result = f"You Win! ⚫ {black} vs ⚪ {white}"
        elif white > black:
            result = f"AI Wins! ⚪ {white} vs ⚫ {black}"
        else:
            result = f"Draw! {black} – {white}"
        self.turn_label.config(text="Game Over")
        messagebox.showinfo("Game Over", result)
