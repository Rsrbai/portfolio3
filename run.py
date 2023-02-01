from random import randint
from sys import exit

scores = {"computer": 0, "player": 0}




class Board:
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

        for x, y in self.ship_pos:
            self.board[x][y] = "S"
        for x, y in self.hits:
            self.board[x][y] = "H"
        self.print_board()

    def guess(self, x, y):

        self.guesses.append((x, y))
        self.board[x][y] = "M"

        if (x, y) in self.ship_pos:
            self.board[x][y] = "H"
            self.hits.append((x, y))
            return "Hit"
        else:
            return "Miss"
    
    def print_board(self):
        if self.type == "player":
            print(f"{self.type}: {self.name}")
            print("  0 1 2 3 4 5 6 7 8 9")
        else:
            print("Computer")
            print("  0 1 2 3 4 5 6 7 8 9")
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))

def random_point(size):

    return randint(0, size-1)

def random_point_ship_size():

    return randint(1, 4)

def random_point_ship_orientation():

    return randint(0,3)

def validate_attacks_input(attack_input):
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
    try:
        for i in range(computer_board.ships):
            if (x, y+i) in computer_board.ship_pos:
                raise ValueError("Computer picking...") 
        if orientation != "up" and orientation != "down" and orientation != "left" and orientation != "right":
            raise ValueError(f"Valid data = up, down, left and right. You entered {orientation}")   
        elif orientation == "up":
            if x-ship_size+1 < 0:
                raise ValueError("Computer picking...")
        elif orientation == "down":
            if x+ship_size-1 > computer_board.size:
                raise ValueError("Computer picking...")
        elif orientation == "left":
            if y-ship_size+1 < 0:
                raise ValueError("Computer picking...")
        elif orientation == "right":
            if y+ship_size-1 > computer_board.size:
                raise ValueError("Computer picking...")
    except ValueError as e:
        print(f"Please wait: {e}")
        return False
    return True

def validate_player_input(player_board, ship_size, x, y, orientation):
    try:
        for i in range(player_board.ships):
            if (x, y+i) in player_board.ship_pos:
                raise ValueError("You have already placed a ship here")
        if orientation != "up" and orientation != "down" and orientation != "left" and orientation != "right":
            raise ValueError(f"Valid data = up, down, left and right, you entered {orientation}")   
        elif orientation == "up":
            if x-ship_size+1 < 0:
                raise ValueError("Ships coordinates must not go off the board")
        elif orientation == "down":
            if x+ship_size-1 > player_board.size:
                raise ValueError("Ships coordinates must not go off the board")
        elif orientation == "left":
            if y-ship_size+1 < 0:
                raise ValueError("Ships coordinates must not go off the board")
        elif orientation == "right":
            if y+ship_size-1 > player_board.size:
                raise ValueError("Ships coordinates must not go off the board")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def validate_player_input_data(ship_size_input, x_input, y_input, orientation):
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
    
    for i in range(player_board.ships):

        while True:
            ship_size_input = input("Enter the size of your ship: \n")
            x_input = input("Enter row for ship placement: \n")
            y_input = input("Enter column coordinate for ship placement: \n")
            orientation = input("Enter the orientation for the ship: \n")
            if validate_player_input_data(ship_size_input, x_input, y_input, orientation):
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

    try:
        if type == "player":
            if (x, y) in computer_board.guesses:
                raise ValueError("You have already hit these coordinates")
        if type == "computer":
            if (x, y) in player_board.guesses:
                raise ValueError("Computer attacking..")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True

def validate_attacks_data(x_input, y_input):

    try:
        if x_input == "n" or y_input == "n":
            exit("You have ended the game.")
        int(x_input)
        int(y_input)
        if int(x_input) < 0:
            raise ValueError(f"Row number must be between 0 and 9")
        elif int(x_input) > 9:
            raise ValueError(f"Row number must be between 0 and 9")
        elif int(y_input) < 0:
            raise ValueError(f"Column number must be between 0 and 9") 
        elif int(y_input) > 9:
            raise ValueError(f"Column number must be between 0 and 9")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True

def player_attack(computer_board, player_board):
    while True:
        type = "player"
        x_input = input("Enter the row coordinate for your attack!: \n")
        y_input = input("Enter the column coordinate for your attack! \n")
        if validate_attacks_data(x_input, y_input):
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
    while True:
        type = "computer"
        x = random_point(computer_board.size)
        y = random_point(computer_board.size)
        if validate_attacks(computer_board, player_board, x, y, type):
            if player_board.guess(x, y) == "Hit":
                print("The computer hit your ship!")
                print("**********************************")
                scores["computer"] += 1
            elif player_board.guess(x, y) == "Miss":
                print("The computer missed your ship!")
                print("**********************************")
            else: 
                continue
            break

    


def play_game(computer_board, player_board):

    print("**********************************")
    player_board.print_board()
    print("**********************************")
    computer_board.print_board()   
    print("Enter 'n' and game will end at end of current phase") 
    populate_player_board(player_board)
    populate_computer_board(computer_board)
    print("**********************************")
    player_board.print_board()
    print("**********************************")    
    computer_board.print_board()   
    print(f"Scores are: {scores}")
    print("Enter 'n' and game will end at end of current phase")
    print(player_board.ship_pos)
    print(computer_board.ship_pos)
    for i in range(player_board.attacks):
        player_attack(computer_board, player_board)
        computer_attack(computer_board, player_board)
        player_board.print_board()
        print("**********************************")
        computer_board.attacks -= 1
        if computer_board.attacks > 0:    
            computer_board.print_board()
        else:
            computer_board.print_computer_end()
        print(f"Scores are: {scores}")
        print("Enter 'n' and the game will end at end of current phase")
    if scores["player"] > scores["computer"]:
        print("Player wins!")
    elif scores["player"] == scores["computer"]:
        print("It's a tie!")
    else:
        print("Computer wins!")
     
    

    

def new_game():

    size = 10
    ships = 3
    scores["computer"] = 0
    scores["player"] = 0
    print("**********************************")
    print("Welcome to World of Battleships")
    player_name = input("Please enter your name: \n")
    while True:
        attack_input = input("Enter the amount of attacks(Number of attacks determines game length): \n")
        if validate_attacks_input(attack_input):
            attacks = int(attack_input)
        else:
            continue
        break
    print(f"Board size:{size}. Number of ships: {ships} Number of attacks: {attacks}")
    print("Top left corner is row: 0, col: 0")
    
    
    

    computer_board = Board(size, ships, "Computer", attacks, type="computer")
    player_board = Board(size, ships, player_name, attacks, type="player")

    play_game(computer_board, player_board)



new_game()
