from random import randint
from sys import exit

scores = {"computer": 0, "player": 0}


class Board:
    """
    Board class with a method to initialise a class of board which is what
    holds all the data of each board in use and stores data such as ship
    positions, number of attacks, size of board, hits and guesses, also stores
    the code used to print each board
    """
    def __init__(self, size, ships, name, attacks, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = ships
        self.name = name
        self.type = type
        self.attacks = attacks
        self.ship_pos = []
        self.guesses = []
        self.hits = []

    def place_ship(self, ship_size, x, y, orien, type):
        """
        Method to place each ships on the board and store the ship location in
        the ship position array
        """
        if orien == "up":
            for i in range(ship_size):
                if type == "player":
                    self.board[x-i][y] = "S"
                self.ship_pos.append((x-i, y))
        elif orien == "down":
            for i in range(ship_size):
                if type == "player":
                    self.board[x+i][y] = "S"
                self.ship_pos.append((x+i, y))
        elif orien == "left":
            for i in range(ship_size):
                if type == "player":
                    self.board[x][y-i] = "S"
                self.ship_pos.append((x, y-i))
        elif orien == "right":
            for i in range(ship_size):
                if type == "player":
                    self.board[x][y+i] = "S"
                self.ship_pos.append((x, y+i))

    def print_computer_end(self):
        """
        Method to print the computers final board of the game, revealing all
        ship locations to the player
        """
        for x, y in self.ship_pos:
            self.board[x][y] = "S"
        for x, y in self.hits:
            self.board[x][y] = "H"
        self.print_board()

    def guess(self, x, y):
        """
        Method to check if the computer or users guess is in the ship_pos array
        therefore indicating a hit, changing the coordinates to represent
        the outcome of the guess, hit or miss. Stores hits in the hits array.
        """
        self.guesses.append((x, y))
        self.board[x][y] = "M"

        if (x, y) in self.ship_pos:
            self.board[x][y] = "H"
            self.hits.append((x, y))
            return "Hit"
        else:
            return "Miss"

    def print_board(self):
        """
        Method to print each board for the user and computer, numbering the
        top and left hand side as a visual aide to the user.
        """
        if self.type == "player":
            print(f"{self.type}: {self.name}")
            print("  ", end="")
            for i in range(0, self.size):
                print(f"{i} ", end="")
            print("")
        else:
            print("Computer")
            print("  ", end="")
            for i in range(0, self.size):
                print(f"{i} ", end="")
            print("")
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))


def random_point(size):
    """
    Helper function to get a random interger between 0 and board size - 1
    """
    return randint(0, size-1)


def random_point_ship_size():
    """
    Helper function to get a random integer between 1 and 4
    """
    return randint(1, 4)


def random_point_ship_orien():
    """
    Helper function to get a random integer between 0 and 3
    """
    return randint(0, 3)


def validate_attacks_input(attack_input):
    """
    Function checking the data input from the user setting the amount of
    attacks
    """
    try:
        if attack_input == "n":
            exit("You have ended the game.")
        int(attack_input)
        if int(attack_input) < 0:
            raise ValueError("Attacks must be a positive number")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True


def validate_computer_input(computer_board, ship_size, x, y, orien):
    """
    Function validating the computers input, ensuring ships dont go off the
    board or if the direction of your ship means your ship would extend over
    another ship this catches that
    """
    try:
        if (x, y) in computer_board.ship_pos:
            raise ValueError("Computer picking...")
        if orien not in ["up", "down", "left", "right"]:
            exit("Fatal error")
        ship_end_x_up = x - (ship_size - 1)
        ship_end_x_down = x + (ship_size - 1)
        ship_end_y_right = y + (ship_size - 1)
        ship_end_y_left = y - (ship_size - 1)
        if orien == "up":
            if ship_end_x_up < 0:
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x-i, y) in computer_board.ship_pos:
                        raise ValueError("Computer picking...1")
        elif orien == "down":
            if ship_end_x_down >= (computer_board.size-1):
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x+i, y) in computer_board.ship_pos:
                        raise ValueError("Computer picking...2")
        elif orien == "right":
            if ship_end_y_right >= (computer_board.size-1):
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x, y+i) in computer_board.ship_pos:
                        raise ValueError("Computer picking...3")
        elif orien == "left":
            if ship_end_y_left < 0:
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x, y-i) in computer_board.ship_pos:
                        raise ValueError("Computer picking...4")
    except ValueError as e:
        print(f"Please wait: {e}")
        return False
    return True


def validate_p_in(player_board, ship_size, x, y, orien):
    """
    Function validating the data input from the user to ensure ships dont go
    out of bounds, they havnt already tried to place in the coordinates
    and to stop ships extending over other ships
    """
    try:
        if (x, y) in player_board.ship_pos:
            raise ValueError("You have already placed a ship here")
        if orien not in ["up", "down", "left", "right"]:
            raise ValueError(f"You entered {orien}")
        elif x < 0 or x > (player_board.size - 1):
            raise ValueError(f"Row not between 0 and {player_board.size-1}")
        elif y < 0 or y > (player_board.size - 1):
            raise ValueError(f"Col not between 0 and {player_board.size-1}")
        ship_end_x_up = x - (ship_size - 1)
        ship_end_x_down = x + (ship_size - 1)
        ship_end_y_right = y + (ship_size - 1)
        ship_end_y_left = y - (ship_size - 1)
        if orien == "up":
            if ship_end_x_up < 0:
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x-i, y) in player_board.ship_pos:
                        raise ValueError("Cannot extend over another ship")
        elif orien == "down":
            if ship_end_x_down >= (player_board.size-1):
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x+i, y) in player_board.ship_pos:
                        raise ValueError("Cannot extend over another ship")
        elif orien == "right":
            if ship_end_y_right >= (player_board.size-1):
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x, y+i) in player_board.ship_pos:
                        raise ValueError("Cannot extend over another ship")
        elif orien == "left":
            if ship_end_y_left < 0:
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x, y-i) in player_board.ship_pos:
                        raise ValueError("Cannot extend over another ship")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def validate_player_dtype(ship_size_in, x_in, y_in, orien):
    """
    Function to validate the data type of the input values and that they
    are within paramaters
    """
    try:
        if ship_size_in == "n" or x_in == "n":
            exit("You have ended the game.")
        elif y_in == "n" or orien == "n":
            exit("You have ended the game.")
        int(ship_size_in)
        int(x_in)
        int(y_in)
        if int(ship_size_in) < 1:
            raise ValueError("Ship size cannot be less than 1")
        elif int(ship_size_in) > 4:
            raise ValueError("Ship size cannot be greater than 4")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True


def populate_player_board(player_board):
    """
    Function taking data from the user and using it to pass to the place_ship
    method in the board class
    """
    for i in range(player_board.ships):

        while True:
            ship_size_in = input("Enter the size of your ship from 1-4: \n")
            x_in = input("Enter row coordinate: \n")
            y_in = input("Enter column coordinate: \n")
            orien = input("Enter up, down, left or right (n to quit): \n")
            if validate_player_dtype(ship_size_in, x_in, y_in, orien):
                ship_size = int(ship_size_in)
                x = int(x_in)
                y = int(y_in)
                if validate_p_in(player_board, ship_size, x, y, orien):
                    player_board.place_ship(ship_size, x, y, orien, "player")
                    break
                else:
                    continue
                break


def populate_computer_board(computer_board):
    """
    Function generating data for the computer and using it to pass to the
    place_ship method in the board class
    """
    ship_orientations = ["up", "down", "left", "right"]
    for i in range(computer_board.ships):
        while True:
            ship_size = random_point_ship_size()
            x = random_point(computer_board.size)
            y = random_point(computer_board.size)
            orien = ship_orientations[random_point_ship_orien()]
            if validate_computer_input(computer_board, ship_size, x, y, orien):
                computer_board.place_ship(ship_size, x, y, orien, "computer")
            else:
                continue
            break


def validate_attacks(computer_board, player_board, x, y, type):
    """
    Function validating the attack data from the user checking that the user
    hasnt attacked this coordinates already
    """
    try:
        if type == "player":
            if (x, y) in computer_board.guesses:
                raise ValueError("You have already hit these coordinates")
        elif type == "computer":
            if (x, y) in player_board.guesses:
                raise ValueError("Computer attacking itself..")
    except ValueError as e:
        if type == "player":
            print(f"Invalid data: {e}, please try again.")
        elif type == "computer":
            print(f"Computer malfunction: {e}.")
        return False
    return True


def validate_attacks_data(player_board, x_input, y_input):
    """
    Function validating data type and checking that it is within paramaters
    """
    try:
        if x_input == "n" or y_input == "n":
            exit("You have ended the game.")
        int(x_input)
        int(y_input)
        if int(x_input) < 0:
            raise ValueError(f"Row no. not between 0-{player_board.size-1}")
        elif int(x_input) > player_board.size-1:
            raise ValueError(f"Row no. not between 0-{player_board.size-1}")
        elif int(y_input) < 0:
            raise ValueError(f"Col no. not between 0-{player_board.size-1}")
        elif int(y_input) > player_board.size-1:
            raise ValueError(f"Col no. not between 0-{player_board.size-1}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True


def player_attack(computer_board, player_board):
    """
    Function taking data from the user, validating it and passing it to the
    guess method
    """
    while True:
        type = "player"
        x_input = input("Enter the row for your attack!: \n")
        y_input = input("Enter the col for your attack!(Enter n to quit): \n")
        if validate_attacks_data(player_board, x_input, y_input):
            x = int(x_input)
            y = int(y_input)
            if validate_attacks(computer_board, player_board, x, y, type):
                if computer_board.guess(x, y) == "Hit":
                    print("You hit their ship!")
                    scores["player"] += 1
                elif computer_board.guess(x, y) == "Miss":
                    print("You missed their ship!")
                else:
                    continue
                break


def computer_attack(computer_board, player_board):
    """
    Function generating data for the computer to be validated and passed to
    the guess method
    """
    while True:
        type = "computer"
        x = random_point(computer_board.size)
        y = random_point(computer_board.size)
        if validate_attacks(computer_board, player_board, x, y, type):
            if player_board.guess(x, y) == "Hit":
                print("The computer hit your ship!")
                scores["computer"] += 1
            elif player_board.guess(x, y) == "Miss":
                print("The computer missed your ship!")
            else:
                continue
            break


def play_game(computer_board, player_board):
    """
    Function that controls the overall flow of the game
    """
    player_board.print_board()
    computer_board.print_board()
    populate_player_board(player_board)
    populate_computer_board(computer_board)
    player_board.print_board()
    computer_board.print_board()
    print(f"Scores are: {scores}")
    for i in range(player_board.attacks):
        player_attack(computer_board, player_board)
        computer_attack(computer_board, player_board)
        player_board.print_board()
        computer_board.attacks -= 1
        if computer_board.attacks > 0:
            computer_board.print_board()
        else:
            computer_board.print_computer_end()
        print(f"Scores are: {scores}")
    if scores["player"] > scores["computer"]:
        print("Player wins!")
    elif scores["player"] == scores["computer"]:
        print("It's a tie!")
    else:
        print("Computer wins!")


def new_game():
    """
    Function starting a new game, taking input from the user and using it to
    initialise a class of player_board and computer_board
    """
    size = 7
    ships = 3
    scores["computer"] = 0
    scores["player"] = 0
    print("**********************************")
    print("Welcome to World of Battleships")
    player_name = input("Please enter your name: \n")
    while True:
        attack_input = input("Enter No. of attacks(n to quit): \n")
        if validate_attacks_input(attack_input):
            attacks = int(attack_input)
        else:
            continue
        break
    print(f"Board size:{size} No. of: {ships} No. of attacks: {attacks}")
    print("Top left corner is row: 0, col: 0")
    computer_board = Board(size, ships, "Computer", attacks, type="computer")
    player_board = Board(size, ships, player_name, attacks, type="player")
    play_game(computer_board, player_board)


new_game()
