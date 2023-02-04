from random import randint
from sys import exit

# Welcome to World of Battleships, the aim of the game is to have a higher score than the computer
# once all attacks have been used up. This means the length of the game is determined by the amount
# of attacks set when asked to set the amount of attacks you would like to have.
# Enter "n" into any field that requires input except the "name" field to end the game at the end of the 
# current phase. The game is fully customizable although the game size is not 
# customizable by the player as there are limitations on how big the board game can be inside the heroku 
# terminal so game size is set to 7, feel free to play a game on a higher board size but this must be 
# done through changing the code in the variable size in the new_game function.

scores = {"computer": 0, "player": 0}

class Board:
    """
    Board class with a method to initialise a class of board which is what
    holds all the data of each board in use and stores data such as ship
    positions, number of attacks, size of board, hits and guesses, also stores the code
    used to print each board
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

    def place_ship(self, ship_size, x, y, orientation, type):
        """
        Method to place each ships on the board and store the ship location in the 
        ship position array 
        """
        if orientation == "up":
            for i in range(ship_size):
                if type == "player":
                    self.board[x-i][y] = "S"
                self.ship_pos.append((x-i, y))
        elif orientation == "down":
            for i in range(ship_size):
                if type == "player":
                    self.board[x+i][y] = "S"
                self.ship_pos.append((x+i, y))
        elif orientation == "left":
            for i in range(ship_size):
                if type == "player":
                    self.board[x][y-i] = "S"
                self.ship_pos.append((x, y-i))
        elif orientation == "right":
            for i in range(ship_size):
                if type == "player":
                    self.board[x][y+i] = "S"
                self.ship_pos.append((x, y+i))
    
    def print_computer_end(self):
        """
        Method to print the computers final board of the game, revealing all ship locations
        to the player
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
        Method to print each board for the user and computer, numbering the top and left hand
        side as a visual aide to the user.
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

    return randint(0, size-1)

def random_point_ship_size():

    return randint(1, 4)

def random_point_ship_orientation():

    return randint(0,3)

def validate_attacks_input(attack_input):
    """
    Function checking the data input from the user setting the amount of attacks
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

def validate_computer_input(computer_board, ship_size, x, y, orientation):
    """
    Function validating the computers input, ensuring ships dont go off the board
    or if the direction of your ship means your ship would extend over 
    another ship this catches that
    """
    try:
        if (x, y) in computer_board.ship_pos:
            raise ValueError("Computer picking...")
        if orientation != "up" and orientation != "down" and orientation != "left" and orientation != "right":
            exit("Fatal error")   
        ship_end_x_up = x - (ship_size - 1)
        ship_end_x_down = x + (ship_size - 1)
        ship_end_y_right = y + (ship_size - 1) 
        ship_end_y_left = y - (ship_size - 1)
        if orientation == "up":
            if ship_end_x_up < 0:
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x-i, y) in computer_board.ship_pos:
                        raise ValueError("Computer picking...1") 
        elif orientation == "down":
            if ship_end_x_down >= (computer_board.size-1):
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x+i, y) in computer_board.ship_pos:
                        raise ValueError("Computer picking...2") 
        elif orientation == "right":
            if ship_end_y_right >= (computer_board.size-1):
                raise ValueError("Computer picking...")
            else:
                for i in range(computer_board.ships):
                    if (x, y+i) in computer_board.ship_pos:
                        raise ValueError("Computer picking...3") 
        elif orientation == "left":
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

def validate_player_input(player_board, ship_size, x, y, orientation):
    """
    Function validating the data input from the user to ensure ships dont go
    out of bounds, they havnt already tried to place in the coordinates
    and to stop ships extending over other ships
    """
    try:
        if (x, y) in player_board.ship_pos:
            raise ValueError("You have already placed a ship here")
        if orientation != "up" and orientation != "down" and orientation != "left" and orientation != "right":
            raise ValueError(f"Valid data = up, down, left and right, you entered {orientation}")   
        elif x < 0 or x > (player_board.size - 1):
            raise ValueError(f"Row number must be between 0 and {player_board.size-1}")
        elif y < 0 or y > (player_board.size - 1):
            raise ValueError(f"Column number must be between 0 and {player_board.size-1}")
        ship_end_x_up = x - (ship_size - 1)
        ship_end_x_down = x + (ship_size - 1)
        ship_end_y_right = y + (ship_size - 1) 
        ship_end_y_left = y - (ship_size - 1)
        if orientation == "up":
            if ship_end_x_up < 0:
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x-i, y) in player_board.ship_pos:
                        raise ValueError("Ship cannot extend on top of another ship1") 
        elif orientation == "down":
            if ship_end_x_down >= (player_board.size-1):
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x+i, y) in player_board.ship_pos:
                        raise ValueError("Ship cannot extend on top of another ship2") 
        elif orientation == "right":
            if ship_end_y_right >= (player_board.size-1):
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x, y+i) in player_board.ship_pos:
                        raise ValueError("Ship cannot extend on top of another ship3")
        elif orientation == "left":
            if ship_end_y_left < 0:
                raise ValueError("Ship goes out of bounds")
            else:
                for i in range(player_board.ships):
                    if (x, y-i) in player_board.ship_pos:
                        raise ValueError("Ship cannot extend on top of another ship4") 
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True

def validate_player_input_data_type(ship_size_input, x_input, y_input, orientation):
    """
    Function to validate the data type of the input values and that they are within paramaters
    """
    try:
        if ship_size_input == "n" or x_input == "n" or y_input == "n" or orientation == "n":
            exit("You have ended the game.")
        int(ship_size_input)
        int(x_input)
        int(y_input)
        if int(ship_size_input) < 1:
            raise ValueError("Ship size cannot be less than 1")
        elif int(ship_size_input) > 4:
            raise ValueError("Ship size cannot be greater than 4")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True


def populate_player_board(player_board):
    """
    Function taking data from the user and using it to pass to the place_ship method in the board class
    """
    for i in range(player_board.ships):

        while True:
            ship_size_input = input("Enter the size of your ship from 1-4 (Enter n to quit at end of phase): \n")
            x_input = input("Enter row for ship placement (Enter n to quit at end of phase): \n")
            y_input = input("Enter column coordinate for ship placement (Enter n to quit at end of phase): \n")
            orientation = input("Enter the orientation for the ship (Enter n to quit): \n")
            if validate_player_input_data_type(ship_size_input, x_input, y_input, orientation):
                ship_size = int(ship_size_input)
                x = int(x_input)
                y = int(y_input)
                if validate_player_input(player_board, ship_size, x, y, orientation):
                    player_board.place_ship(ship_size, x, y, orientation, "player") 
                    break
                else:
                    continue
                break

def populate_computer_board(computer_board):
    """
    Function generating data for the computer and using it to pass to the place_ship method in the board class
    """
    ship_orientations = ["up", "down","left","right"]
    for i in range(computer_board.ships):
        while True:
            ship_size = random_point_ship_size()
            x = random_point(computer_board.size)
            y = random_point(computer_board.size)
            orientation = ship_orientations[random_point_ship_orientation()]  
            if validate_computer_input(computer_board, ship_size, x, y, orientation):
                computer_board.place_ship(ship_size, x, y, orientation, "computer")     
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
            raise ValueError(f"Row number must be between 0 and {player_board.size - 1}")
        elif int(x_input) > player_board.size-1:
            raise ValueError(f"Row number must be between 0 and {player_board.size - 1}")
        elif int(y_input) < 0:
            raise ValueError(f"Column number must be between 0 and {player_board.size - 1}") 
        elif int(y_input) > player_board.size-1:
            raise ValueError(f"Column number must be between 0 and {player_board.size - 1}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True

def player_attack(computer_board, player_board):
    """
    Function taking data from the user, validating it and passing it to the guess method
    """
    while True:
        type = "player"
        x_input = input("Enter the row coordinate for your attack!(Enter n to quit at end of phase): \n")
        y_input = input("Enter the column coordinate for your attack!(Enter n to quit): \n")
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
    Function generating data for the computer to be validated and passed to the guess method
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
    Function starting a new game, taking input from the user and using it to initialise a class of 
    player_board and computer_board
    """
    size = 7
    ships = 3
    scores["computer"] = 0
    scores["player"] = 0
    print("**********************************")
    print("Welcome to World of Battleships")
    player_name = input("Please enter your name: \n")
    while True:
        attack_input = input("Enter the amount of attacks(No. of attacks sets game length, n to quit): \n")
        if validate_attacks_input(attack_input):
            attacks = int(attack_input)
        else:
            continue
        break
    print(f"Board size:{size} Number of ships: {ships} Number of attacks: {attacks}")
    print("Top left corner is row: 0, col: 0")
    computer_board = Board(size, ships, "Computer", attacks, type="computer")
    player_board = Board(size, ships, player_name, attacks, type="player")
    play_game(computer_board, player_board)

new_game()
