class DropToken:
    """Allows for operations to mimic functionality of the Drop Token game."""
    def __init__(self):
        """Instantiates an instance of the class.

        Attributes:
            board (list): A 4x4 matrix that will contain the values and status of our game.
            p1 (bool): Represent the status of player 1.
            p2 (bool): Represent the status of player 2.
            win (list): A one-element list that allows us to check for wins and draws.
            plays (list): A list that will keep track of the columns played in Drop Token.
        """
        self.board: list = [[0, 0, 0, 0] for _ in range(4)]
        self.p1: bool = True
        self.p2: bool = False
        self.win: list = ["None"]
        self.plays: list = []

    def zero_exists(self) -> bool:
        """Checks if a zero exists in our game board.

        Returns:
            has_zero (bool): True if 0 in board, False otherwise.
        """
        has_zero = False
        for row in self.board:
            for col in row:
                if col == 0:
                    has_zero = True
                    break
            else:  # Breaks out of outer loop if inner loop was broken out of
                continue
            break
        return has_zero

    def check_area(self, area: list) -> bool:
        """Checks if player 1 or player 2 won at a specific area.

        Args:
            area (list): A list that contains values in a specific portion of the board.

        Returns:
            check (bool): True if all items in area are 1 or 2, False otherwise.
        """
        check = area == [1, 1, 1, 1] or area == [2, 2, 2, 2]
        if check:
            self.win[0] = "p1" if self.p1 else "p2"  # This will allow us to check for a win in the main loop
        return check

    def check_win(self, point: list, column: list) -> bool:
        """Calculates the needed areas to check for a win.

        Args:
            point (list): A list that contains the row and column that the token was inserted at.
            column (list): A list of values in the board that contains the values in the same column as point.

        Returns:
            bool: True if any of the areas have all 1s or 2s, False otherwise.
        """
        # Checks current column
        has_won = self.check_area(column)
        if has_won:
            return True
        # Checks current row
        row = self.board[point[0]]
        has_won = self.check_area(row)
        if has_won:
            return True
        # Checks forward diagonal
        diagonal = []
        for i in range(len(self.board) - 1, -1, -1):
            diagonal.append(self.board[i][-i-1])
        has_won = self.check_area(diagonal)
        if has_won:
            return True
        # Checks backward diagonal
        diagonal.clear()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i == j:
                    diagonal.append(self.board[i][j])
        has_won = self.check_area(diagonal)
        self.p1, self.p2 = not self.p1, not self.p2  # Switches the players' turns every time
        return True if has_won else False

    def insert(self, column: int) -> str:
        """Simulates the functionality for the PUT statement and drops a token in the specified column.

        Args:
            column (int): The value specifying which column to drop the token in

        Returns:
            str: Returns a string denoting the status of the dropped token: OK|ERROR|WIN|DRAW
        """
        if self.win[0] == "None":  # Only if game has not been won or drawed
            col = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if column - 1 == j:
                        col.append(self.board[i][j])
            has_space = 0 in col
            if has_space:  # Only if there is a 0 in our column
                x, y = None, None  # Used to pass the inserted point after the loop
                for i in range(len(self.board) - 1, -1, -1):
                    for j in range(len(self.board[i])):
                        if column - 1 == j and self.board[i][j] == 0:
                            x, y = i, j
                            if self.p1:
                                self.board[i][j] = 1
                            else:
                                self.board[i][j] = 2
                            self.plays.append(j + 1)
                            break
                    else:
                        continue
                    break
                # Checks if there has been a win or draw
                if x is not None and y is not None:
                    # Check for win
                    col.clear()
                    for i in range(len(self.board)):
                        for j in range(len(self.board[i])):
                            if column - 1 == j:
                                col.append(self.board[i][j])
                    # Uses a combination of if there is a zero in the board and if there was a win to check for draw.
                    result = self.check_win([x, y], col)
                    zero_exists = self.zero_exists()
                    if not zero_exists and not result:
                        self.win[0] = "DRAW"  # Used to check entry to function
                        return "DRAW"  # Used to print the result
                    elif result:
                        return "WIN"
            # ERROR if a column is full but there are other 0s on the board
            zero_exists = self.zero_exists()
            if not has_space and zero_exists:
                return "ERROR"
            return "OK"  # Has to return OK if there has been no ERROR, DRAW, or WIN

    def get(self):
        """Prints the plays that have been made so far (columns); simulates functionality for GET statement."""
        for play in self.plays:
            print(play)

    def get_win(self) -> list:
        """Retrieves the win property so that proper checks can be made to continue when there is a win or draw.

        Returns:
            win (list): The one-element list that denotes the status of a game.
        """
        return self.win

    def clear(self):
        """Resets all properties for a Drop Token game."""
        self.board = [[0, 0, 0, 0] for _ in range(4)]
        self.p1: bool = True
        self.p2: bool = False
        self.win: list = ["None"]
        self.plays: list = []

    def __str__(self):
        """Prints out the specified format for a game; simulates functionality for BOARD statement."""
        results = []
        for i in range(len(self.board)):
            result = ["|"]
            for j in range(4):
                result.append(str(self.board[i][j]))
            results.append(" ".join(result))
        results.append("+--------")
        results.append("  1 2 3 4")
        return "\n".join(results)


def main():
    """The main loop for our game which consistently asks for input and uses error handling for invalid inputs."""
    mat = DropToken()
    prompt = str(input("> "))  # Starts off the loop
    while prompt.strip().upper() != "EXIT":
        play_again = False
        # Is used to eliminate extra spaces and converting extra spaces between PUT and value to one space
        splitted = ' '.join(prompt.strip().upper().split()).split(" ")
        if splitted[0] == "PUT":
            try:
                if len(splitted) == 2:
                    value = splitted[1]
                    if 0 < int(value) <= 4:
                        if mat.get_win()[0] == "None":
                            result = mat.insert(int(value))
                            if result == "DRAW":
                                print("OK")
                            print(result)
                        else:
                            # Added additional functionality to let the players play again if they want to
                            again = str(input("> PLAY AGAIN? (Y/N)? "))
                            if again.upper() == 'Y':
                                mat.clear()
                                play_again, prompt = True, ' '.join(prompt.strip().upper().split())
                    else:
                        raise ValueError("VALUE MUST BE BETWEEN 1 AND 4")
                else:
                    print("Use <HELP> to see the available commands")
            except ValueError:
                print("VALUE MUST BE A DIGIT AND BETWEEN 1 AND 4")
        elif prompt.strip().upper() == "BOARD":
            print(mat)
        elif prompt.strip().upper() == "GET":
            mat.get()
        # Added extra functionality to restart the game at any given time
        elif prompt.strip().upper() == "RESTART":
            mat.clear()
        elif prompt.strip().upper() == "HELP":
            print("AVAILABLE COMMANDS:")
            print("\tBOARD: Print out the board")
            print("\tGET: Print out all columns that have been places so far")
            print("\tPUT <value>: Inserts a token at column <value>")
            print("\tRESTART: Restarts the game")
            print("\tEXIT: Quits the game")
        else:
            print("Use <HELP> to see the available commands")
        if not play_again:
            prompt = str(input("> "))


if __name__ == '__main__':
    main()