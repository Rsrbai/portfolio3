from random import randint

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

    def guess(self, x, y):

        self.guesses.append((x, y))
        self.board[x][y] = "M"

        if (x, y) in self.ship_pos:
            self.board[x][y] = "H"
            return "Hit"
        else:
            return "Miss"
    
    def print_board(self):
        if self.type == "player":
            print(f"{self.type}: {self.name}")
            print("0 1 2 3 4 5 6 7 8 9")
        else:
            print("Computer")
            print("0 1 2 3 4 5 6 7 8 9")
        for row in self.board:
            print(" ".join(row))

def random_point(size):

    return randint(0, size-1)

def random_point_ship_size():

    return randint(1, 4)

def random_point_ship_orientation():

    return randint(0,3)

def validate_attacks_input(attack_input):
    try:
        int(attack_input)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True

def validate_computer_input(computer_board, ship_size, x, y, orientation):
    try:
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


def populate_player_board(player_board):
    
    for i in range(player_board.ships):
        while True:
            ship_size = int(input("Enter the size of your ship: \n"))
            x = int(input("Enter row for ship placement: \n"))
            y = int(input("Enter column coordinate for ship placement: \n"))
            orientation = input("Enter the orientation for the ship: \n")
            if validate_player_input(player_board, ship_size, x, y, orientation):
                player_board.place_ship(ship_size, x, y, orientation, "player") 
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

def player_attack(computer_board, player_board):
    while True:
        type = "player"
        x = int(input("Enter the row coordinate for your attack!: \n"))
        y = int(input("Enter the column coordinate for your attack! \n"))
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
                scores["computer"] += 1
            elif player_board.guess(x, y) == "Miss":
                print("The computer missed your ship!")
            else: 
                continue
            break

    


def play_game(computer_board, player_board):
    
    player_board.print_board()
    print("**********************************")
    computer_board.print_board()    
    populate_player_board(player_board)
    populate_computer_board(computer_board)
    player_board.print_board()
    print("**********************************")    
    computer_board.print_board()   
    print(f"Scores are: {scores}")
    print(player_board.ship_pos)
    print(computer_board.ship_pos)
    for i in range(player_board.attacks):
        player_attack(computer_board, player_board)
        computer_attack(computer_board, player_board)
        player_board.print_board()
        print("**********************************")    
        computer_board.print_board()
        print(f"Scores are: {scores}")
    if scores["player"] > scores["computer"]:
        print("Player wins!")
    else:
        print("Computer")
    

    

def new_game():

    size = 10
    ships_no = 3
    scores["computer"] = 0
    scores["player"] = 0
    print("**********************************")
    print("Welcome to World of Battleships")
    player_name = input("Please enter your name: \n")
    while True:
        attack_input = input("Enter the amount of attacks each player will have: \n")
        if validate_attacks_input(attack_input):
            attacks = int(attack_input)
        else:
            continue
        break
    print(f"Board size:{size}. Number of ships: {ships_no} Number of attacks: {attacks}")
    print("Top left corner is row: 0, col: 0")
    print("**********************************")
    
    

    computer_board = Board(size, ships_no, "Computer", attacks, type="computer")
    player_board = Board(size, ships_no, player_name, attacks, type="player")

    play_game(computer_board, player_board)



new_game()
