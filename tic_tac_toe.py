import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        # Initialize the game window and set up the initial state of the game
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [" " for _ in range(9)]  # A list representing the 3x3 board
        self.current_player = "X"  # X always starts first
        self.buttons = []  # List to store the button widgets
        self.create_board()  # Set up the game board

    def create_board(self):
        # Create the 3x3 grid of buttons that represent the Tic-Tac-Toe board
        for i in range(9):
            button = tk.Button(self.root, text=" ", font='normal 20 bold', height=3, width=6,
                               command=lambda i=i: self.click(i))  # Button triggers click method
            button.grid(row=i // 3, column=i % 3)  # Place button in grid layout
            self.buttons.append(button)  # Add button to the list of buttons

    def click(self, index):
        # Handle a player's move when they click on a button
        if self.board[index] == " ":  # Check if the cell is empty
            self.board[index] = self.current_player  # Update the board with the current player's mark
            self.buttons[index].config(text=self.current_player)  # Update the button text to show the mark
            if self.check_win(self.current_player):  # Check if the current player has won
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")  # Show a win message
                self.reset_board()  # Reset the board for a new game
            elif " " not in self.board:  # Check if the board is full (tie)
                messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")  # Show a tie message
                self.reset_board()  # Reset the board for a new game
            else:
                # Switch to the other player
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.ai_move()  # If it's the AI's turn, make the AI move

    def ai_move(self):
        # Make the AI's move
        index = self.find_best_move("X")  # Try to block the player from winning
        if index is None:  # If there's no need to block, pick a random empty spot
            empty_indices = [i for i, x in enumerate(self.board) if x == " "]
            if empty_indices:  # Ensure there are empty cells available
                index = random.choice(empty_indices)
        self.click(index)  # Make the move at the chosen index

    def find_best_move(self, player):
        # Find the best move for the specified player to block or win
        for i in range(9):
            if self.board[i] == " ":  # Check if the cell is empty
                self.board[i] = player  # Temporarily make the move
                if self.check_win(player):  # Check if this move wins the game
                    self.board[i] = " "  # Undo the move
                    return i  # Return the index that would win the game
                self.board[i] = " "  # Undo the move
        return None  # No winning move found

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

if __name__ == "__main__":
    # Create the main window and start the game
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()