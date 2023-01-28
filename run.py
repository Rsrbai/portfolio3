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
            if x-size+1 < 0:
                print("Ship does not fit on the board")
                return
            for i in range(size):
                self.board[x-i][y] = "S"
        elif orientation == "down":
            if x+size-1 > self.size:
                print("Ship does not fit on the board")
                return
            for i in range(size):
                self.board[x+i][y] = "S"
        elif orientation == "left":
            if y-size+1 < 0:
                print("Ship does not fit on the board")
                return
            for i in range(size):
                self.board[x][y-i] = "S"
        else:
            if y+size-1 > self.size:
                print("Ship does not fit on the board")
                return
            for i in range(size):
                self.board[x][y+i] = "S"
    
    def print_board(self):
        if self.type == "player":
            print(f"{self.type}: {self.name}")
            print("0 1 2 3 4 5 6 7 8 9")
        else:
            print("Computer")
            print("0 1 2 3 4 5 6 7 8 9")
        for row in self.board:
            print(" ".join(row))

# def validate_player_input(size, x, y, orientation):


def populate_player_board(player_board):
    
    for i in range(player_board.ships):
        size = int(input("Enter the size of your ship: \n"))
        x = int(input("Enter x coordinate for ship placement: \n"))
        y = int(input("Enter y coordinate for ship placement: \n"))
        orientation = input("Enter the orientation for the ship: \n")
        # validate_player_input(size, x, y, orientation)
        player_board.place_ship(size, x, y, orientation)
        

def play_game(computer_board, player_board):
    
    player_board.print_board()
    print("**********************************")
    computer_board.print_board()    
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
