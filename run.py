from random import randint

class board:
    def __init__(self, size, ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = ships
        self.name = name 
        self.type = type

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
                