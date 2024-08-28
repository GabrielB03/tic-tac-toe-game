import tkinter as tk
from tkinter import messagebox
import random
import math

class TicTacToe:
    def __init__(self, root):
        # Initialize the game window and set up the initial state of the game
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [" " for _ in range(9)]  # A list representing the 3x3 board
        self.current_player = "X"  # X always starts first
        self.buttons = []  # List to store the button widgets
        self.game_mode = None  # To store the current game mode (singleplayer or multiplayer)
        self.difficulty = "Medium"  # Default difficulty
        self.theme = "Light"  # Default theme
        self.create_menu()  # Set up the initial menu

    def create_menu(self):
        # Create the main menu with options
        self.clear_window()  # Clear any existing widgets in the window

        # Create buttons for each menu option
        tk.Label(self.root, text="Tic-Tac-Toe", font='normal 20 bold').pack(pady=20)
        tk.Button(self.root, text="Singleplayer", font='normal 15', command=self.start_singleplayer).pack(pady=10)
        tk.Button(self.root, text="Multiplayer", font='normal 15', command=self.start_multiplayer).pack(pady=10)
        tk.Button(self.root, text="Settings", font='normal 15', command=self.show_settings).pack(pady=10)

    def start_singleplayer(self):
        # Start the game in singleplayer mode
        self.game_mode = "singleplayer"
        self.current_player = "X"
        self.create_board()

    def start_multiplayer(self):
        # Start the game in multiplayer mode
        self.game_mode = "multiplayer"
        self.current_player = "X"
        self.create_board()

    def show_settings(self):
        # Show settings menu
        self.clear_window()
        tk.Label(self.root, text="Settings", font='normal 20 bold').pack(pady=20)

        # Difficulty settings
        tk.Label(self.root, text="Select AI Difficulty:", font='normal 15').pack(pady=10)
        tk.Button(self.root, text="Easy", font='normal 12', command=lambda: self.set_difficulty("Easy")).pack(pady=5)
        tk.Button(self.root, text="Medium", font='normal 12', command=lambda: self.set_difficulty("Medium")).pack(pady=5)
        tk.Button(self.root, text="Hard", font='normal 12', command=lambda: self.set_difficulty("Hard")).pack(pady=5)

        # Theme settings
        tk.Label(self.root, text="Select Theme Mode:", font='normal 15').pack(pady=10)
        tk.Button(self.root, text="Light Mode", font='normal 12', command=lambda: self.set_theme("Light")).pack(pady=5)
        tk.Button(self.root, text="Dark Mode", font='normal 12', command=lambda: self.set_theme("Dark")).pack(pady=5)
        tk.Button(self.root, text="Black", font='normal 12', command=lambda: self.set_theme("Black")).pack(pady=5)
        tk.Button(self.root, text="Dark Blue", font='normal 12', command=lambda: self.set_theme("Dark Blue")).pack(pady=5)
        tk.Button(self.root, text="Gray", font='normal 12', command=lambda: self.set_theme("Gray")).pack(pady=5)
        tk.Button(self.root, text="Olive Green", font='normal 12', command=lambda: self.set_theme("Olive Green")).pack(pady=5)

        # Back to menu button
        tk.Button(self.root, text="Back to Menu", font='normal 15', command=self.create_menu).pack(pady=10)

    def set_difficulty(self, level):
        # Set the difficulty level for the AI
        self.difficulty = level
        messagebox.showinfo("Settings", f"AI Difficulty set to {level}")

    def set_theme(self, theme):
        # Set the theme mode for the game
        self.theme = theme
        self.apply_theme()
        messagebox.showinfo("Settings", f"{theme} mode activated")

    def apply_theme(self):
        # Apply the current theme to all buttons and window
        if self.theme == "Dark":
            self.root.configure(bg="black")
            button_bg, button_fg = "gray", "white"
        elif self.theme == "Light":
            self.root.configure(bg="white")
            button_bg, button_fg = "white", "black"
        elif self.theme == "Black":
            self.root.configure(bg="black")
            button_bg, button_fg = "dark gray", "white"
        elif self.theme == "Dark Blue":
            self.root.configure(bg="navy")
            button_bg, button_fg = "dark blue", "white"
        elif self.theme == "Gray":
            self.root.configure(bg="gray")
            button_bg, button_fg = "dark gray", "white"
        elif self.theme == "Olive Green":
            self.root.configure(bg="olive")
            button_bg, button_fg = "beige", "black"
        else:
            # Default theme (Light)
            self.root.configure(bg="white")
            button_bg, button_fg = "white", "black"

        for button in self.buttons:
            button.config(bg=button_bg, fg=button_fg)

    def create_board(self):
        # Create the 3x3 grid of buttons that represent the Tic-Tac-Toe board
        self.clear_window()
        self.board = [" " for _ in range(9)]
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text=" ", font='normal 20 bold', height=3, width=6,
                               command=lambda i=i: self.click(i))  # Button triggers click method
            button.grid(row=i // 3, column=i % 3)  # Place button in grid layout
            self.buttons.append(button)  # Add button to the list of buttons

        # Add a reset button
        tk.Button(self.root, text="Reset", font='normal 15', command=self.reset_board).grid(row=3, column=1, pady=10)
        tk.Button(self.root, text="Exit", font='normal 15', command=self.root.quit).grid(row=3, column=2, pady=10)

        # Apply current theme to the board
        self.apply_theme()

    def click(self, index):
        # Handle a player's move when they click on a button
        if self.board[index] == " ":  # Check if the cell is empty
            self.board[index] = self.current_player  # Update the board with the current player's mark
            self.buttons[index].config(text=self.current_player)  # Update the button text to show the mark
            if self.check_win(self.current_player):  # Check if the current player has won
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")  # Show a win message
            elif " " not in self.board:  # Check if the board is full (tie)
                messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")  # Show a tie message
            else:
                # Switch to the other player or let the AI play if singleplayer
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.game_mode == "singleplayer" and self.current_player == "O":
                    self.ai_move()  # If it's the AI's turn, make the AI move

    def ai_move(self):
        # Make the AI's move based on difficulty level
        if self.difficulty == "Easy":
            self.easy_ai()
        elif self.difficulty == "Medium":
            self.medium_ai()
        elif self.difficulty == "Hard":
            self.hard_ai()

    def easy_ai(self):
        # Easy AI: Random move
        empty_indices = [i for i, x in enumerate(self.board) if x == " "]
        if empty_indices:
            index = random.choice(empty_indices)
            self.click(index)

    def medium_ai(self):
        # Medium AI: Random move with a chance to block
        index = self.find_best_move("X")  # type: ignore
        if index is None:  # If there's no winning move, pick random
            empty_indices = [i for i, x in enumerate(self.board) if x == " "]
            if empty_indices:
                index = random.choice(empty_indices)
        self.click(index)

    def hard_ai(self):
        # Hard AI: Minimax algorithm for the best move
        best_score = -math.inf
        best_move = None

        for i in range(9):
            if self.board[i] == " ":  # Check if the cell is empty
                self.board[i] = "O"  # Try the move for AI
                score = self.minimax(0, False)  # Get the score for this move
                self.board[i] = " "  # Undo the move
                if score > best_score:  # If this move is better, choose it
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.click(best_move)  # Make the best move

    def minimax(self, depth, is_maximizing):
        # Minimax algorithm to evaluate the board state
        if self.check_win("O"):
            return 1  # AI wins
        elif self.check_win("X"):
            return -1  # Player wins
        elif " " not in self.board:
            return 0  # Tie

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(depth + 1, False)
                    self.board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "X"
                    score = self.minimax(depth + 1, True)
                    self.board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_win(self, player):
        # Check if the specified player has won the game
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal wins
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical wins
                          (0, 4, 8), (2, 4, 6)]  # Diagonal wins
        return any(all(self.board[i] == player for i in condition) for condition in win_conditions)

    def reset_board(self):
        # Reset the game board to start a new game
        self.board = [" " for _ in range(9)]  # Clear the board
        self.current_player = "X"  # X always starts first
        for button in self.buttons:
            button.config(text=" ")  # Clear the text on all buttons
        self.apply_theme()  # Reapply the theme to buttons

    def clear_window(self):
        # Remove all widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Create the main window and start the game
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()