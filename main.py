"""Entry point for the modular Othello game.

This script simply creates the Tkinter root window and starts the UI manager.
"""

import tkinter as tk
from ui_manager import UI


def main():
    root = tk.Tk()
    UI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
