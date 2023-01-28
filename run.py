from random import randint

scores = {"computer": 0, "player": 0}

class board:
    def __init__(self, size, ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = ships
        self.name = name 
        self.type = type
        self.guesses = []
        self.ships = []

    def place_ship(self, ship, x, y, orientation):
        if orientation == "up":
            for i in range(ship.size):
                self.board[x][y+i] = "S"
        elif orientation == "down":
            for i in range(ship.size):
                self.board[x][y-i] = "S"
        elif orientation == "left":
            for i in range(ship.size):
                self.board[x-i][y] = "S"
        else:
            for i in range(ship.size):
                self.board[x+i][y] = "S"

class Ship:
    def __init__(self, size, name):
        self.size = size
        self.name = name

def new_game():

    size = 10
    ships_no = 3
    scores.computer = 0
    scores.player = 0
    print("**********************************")
    print("Welcome to Triple Threat")
    print(f"Board size:{size}. Number of ships: {ships_no}")
    print("Top left corner is row: 0, col: 0")
    print("**********************************")
    player_name = input("Please enter your name: \n")
    print("**********************************")

    computer_board = Board(size, ships_no, "Computer", type="computer")
    player_board = Board(size, ships_no, player_name, type="player")



new_game()
