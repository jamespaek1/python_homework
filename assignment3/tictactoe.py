"""
Task 6: More on Classes – Tic Tac Toe

This module implements a simple Tic Tac Toe game using classes. It
defines a custom exception ``TictactoeException`` for invalid moves
and a ``Board`` class to represent the game state. The ``Board``
class manages turns, validates moves, detects wins or draws and
provides a string representation of the game grid.

When run as a script, the module starts an interactive two‑player
game. Players take turns entering moves by name (e.g., "upper left").
Invalid or taken moves raise exceptions that are reported to the user.
After each move, the board is displayed and the game status is
checked. The game ends when there is a winner or the board is full.
"""

from __future__ import annotations

from typing import List, Tuple


class TictactoeException(Exception):
    """Custom exception type for Tic Tac Toe errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class Board:
    """Represent a Tic Tac Toe game board."""

    # Valid move names in reading order
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right",
    ]

    def __init__(self) -> None:
        # Initialize a 3x3 board with spaces
        self.board_array: List[List[str]] = [[" " for _ in range(3)] for _ in range(3)]
        # 'X' always starts
        self.turn: str = "X"
        # Track last move index if needed for advanced logic
        self.last_move: int | None = None

    def __str__(self) -> str:
        """Return a human‑friendly string representation of the board."""
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string: str) -> None:
        """Place the current player's mark on the board.

        :param move_string: A string describing the desired move (see
            ``Board.valid_moves``). Raises ``TictactoeException`` if the
            move is invalid or the target square is occupied.
        """
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        # Record the last move for potential future optimisations
        self.last_move = move_index
        # Place the mark and toggle the turn
        self.board_array[row][column] = self.turn
        self.turn = "O" if self.turn == "X" else "X"

    def whats_next(self) -> Tuple[bool, str]:
        """Determine whether the game is over and provide status.

        :returns: A tuple ``(finished, message)``. ``finished`` is
            ``True`` if the game has ended (win or draw) and ``False``
            otherwise. The ``message`` describes the outcome or whose
            turn is next.
        """
        # Check for a win on rows
        for i in range(3):
            if self.board_array[i][0] != " ":
                if (self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]):
                    winner = self.board_array[i][0]
                    return True, f"{winner} wins!"
        # Check for a win on columns
        for i in range(3):
            if self.board_array[0][i] != " ":
                if (self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]):
                    winner = self.board_array[0][i]
                    return True, f"{winner} wins!"
        # Check diagonals
        center = self.board_array[1][1]
        if center != " ":
            if (self.board_array[0][0] == center == self.board_array[2][2]) or (
                self.board_array[0][2] == center == self.board_array[2][0]
            ):
                return True, f"{center} wins!"
        # Check for a draw: no spaces left
        cat_game = True
        for row in self.board_array:
            if " " in row:
                cat_game = False
                break
        if cat_game:
            return True, "Cat's Game."
        # Otherwise, game is not finished; indicate whose turn
        return False, f"{self.turn}'s turn."


def main() -> None:
    """Run an interactive Tic Tac Toe game in the console."""
    print("Welcome to Tic Tac Toe!")
    board = Board()
    finished = False
    while not finished:
        # Display the current board
        print(board)
        # Report whose turn it is according to the board's state
        _, status_message = board.whats_next()
        # If the game is over before making a move (unlikely), break
        if status_message.endswith("wins!") or status_message.startswith("Cat"):
            print(status_message)
            break
        print(status_message)
        # Prompt the current player for their move
        move_input = input("Enter your move: ")
        try:
            board.move(move_input)
        except TictactoeException as exc:
            print(exc.message)
            # Re‑prompt the same player
            continue
        # After a valid move, check if the game has ended
        finished, message = board.whats_next()
        if finished:
            # Print the final state and outcome
            print(board)
            print(message)


if __name__ == "__main__":
    main()