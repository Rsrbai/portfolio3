from random import randint

scores = {"computer": 0, "player": 0}




class Board:
    def __init__(self, size, ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = ships
        self.name = name 
        self.type = type
        self.ship_pos = []
        self.guesses = []
        

    def place_ship(self, size, x, y, orientation):
        if orientation == "up":
            for i in range(size):
                self.board[x-i][y] = "S"
                self.ship_pos.append((x-i, y))
        elif orientation == "down":
            for i in range(size):
                self.board[x+i][y] = "S"
                self.ship_pos.append((x+i, y))
        elif orientation == "left":
            for i in range(size):
                self.board[x][y-i] = "S"
                self.ship_pos.append((x, y-i))
        elif orientation == "right":
            for i in range(size):
                self.board[x][y+i] = "S"
                self.ship_pos.append((x, y+i))
    
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

def random_point_ship_size(ship_size):

    return randint(1, 5)

def validate_player_input(size, x, y, orientation):
    try:
        if orientation != "up" and orientation != "down" and orientation != "left" and orientation != "right":
            raise ValueError(
                f"Valid data = up, down, left and right, you entered {orientation}"
            )   
        elif orientation == "up":
            if x-size+1 < 0:
                raise ValueError(
                    f"Ships coordinates must not go off the board"
                )
        elif orientation == "down":
            if x+size-1 > size:
                raise ValueError(
                    f"Ships coordinates must not go off the board"
                )
        elif orientation == "left":
            if y-size+1 < 0:
                raise ValueError(
                    f"Ships coordinates must not go off the board"
                )
        elif orientation == "right":
            if y+size-1 > size:
                raise ValueError(
                    f"Ships coordinates must not go off the board"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def populate_player_board(player_board):
    
    for i in range(player_board.ships):
        while True:
            size = int(input("Enter the size of your ship: \n"))
            x = int(input("Enter row for ship placement: \n"))
            y = int(input("Enter column coordinate for ship placement: \n"))
            orientation = input("Enter the orientation for the ship: \n")
            if validate_player_input(size, x, y, orientation):
                player_board.place_ship(size, x, y, orientation)
            else:
                continue
            break

# def populate_computer_board(computer_board):

#     for i in range(computer_board.ships):
#       whil
#           size = random_point(computer_board.size)
        

def play_game(computer_board, player_board):
    
    player_board.print_board()
    print("**********************************")
    computer_board.print_board()    
    populate_player_board(player_board)
    player_board.print_board()
        

def new_game():

    size = 10
    ships_no = 1
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
