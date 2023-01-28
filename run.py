from random import randint

scores = {"computer": 0, "player": 0}

class Board:
    def __init__(self, size, ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = ships
        self.name = name 
        self.type = type
        self.guesses = []
        self.ships_pos = []

    def place_ship(self, size, x, y, orientation):
        if orientation == "up":
            for i in range(size):
                self.board[x][y+i] = "S"
        elif orientation == "down":
            for i in range(size):
                self.board[x][y-i] = "S"
        elif orientation == "left":
            for i in range(size):
                self.board[x-i][y] = "S"
        else:
            for i in range(size):
                self.board[x+i][y] = "S"
    
    def print(self):
        if self.type == "player":
            print(f"{self.type}: {self.name}")
            print("0 1 2 3 4 5 6 7 8 9")
        else:
            print("Computer")
            print("0 1 2 3 4 5 6 7 8 9")
        for row in self.board:
            print(" ".join(row))

def populate_player_board(player_board):
    
    for i in range(player_board.ships):
        size = int(input("Enter the size of your ship: \n"))
        x = int(input("Enter x coordinate for ship placement: \n"))
        y = int(input("Enter y coordinate for ship placement: \n"))
        orientation = input("Enter the orientation for the ship: \n")
        player_board.place_ship(size, x, y, orientation)
        

def play_game(computer_board, player_board):
    
    player_board.print()
    print("**********************************")
    computer_board.print()    
    populate_player_board(player_board)

def new_game():

    size = 10
    ships_no = 3
    scores["computer"] = 0
    scores["player"] = 0
    print("**********************************")
    print("Welcome to Impending Doom")
    print(f"Board size:{size}. Number of ships: {ships_no}")
    print("Top left corner is row: 0, col: 0")
    print("**********************************")
    player_name = input("Please enter your name: \n")
    print("**********************************")

    computer_board = Board(size, ships_no, "Computer", type="computer")
    player_board = Board(size, ships_no, player_name, type="player")

    play_game(computer_board, player_board)



new_game()
