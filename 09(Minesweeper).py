import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        #keeping tracks of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #creating a board
        #helper function
        self.board = self.make_new_board() #plant the bombs
        self.assign_values_to_b0ard()

        #inintialise a set to keep track which places have been dug
        self.dug =  set()

    def make_new_board(self):

        #create a new board based on dim_size and plant the bombs
        #making a 2D board a list of list is more preferred
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]


        #planting a bomb
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size*2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                continue  #this means we already planted the bombs so keep going

            board[row][col] = "*" #if not then plant the bomb
            bombs_planted = bombs_planted + 1    

        return board

    def assign_values_to_b0ard(self):
        #we are doing this to check the spots for empty spaces on the board which represemts neighbouring bombs, this 
        # will check what's around the board later on
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue   #don't modify anything if there is a bomb there already

                self.board[r][c] = self.get_neighbour_bombs(r , c)

    def get_neighbour_bombs(self, row, col):
        #all neighbouring cases
        #top left: row - 1, col - 1
        #top middle: row - 1, col
        #top: right row - 1, col + 1
        #left: row, col - 1
        #right: row, col + 1
        #bottom left: row + 1, col - 1
        #bottom middle: row + 1, col
        #bottom right: row + 1, col + 1

        #we need to check all these spots and make sure we remain within the bounds
        num_neighbour_bombs = 0 
        for r in range(max(0, row - 1), min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue  #original location so don't check anything

                if self.board[r][c] == "*":
                    num_neighbour_bombs = num_neighbour_bombs + 1

        
        return num_neighbour_bombs

    def dig(self, row, col):


        #dig if succesful dig return true else a bomb then false
        #some cases
        #--> dig somewhere and a bomb found = game over
        #--> dig a location with neighbouring bombs = finish digging
        #--> dig a location with no neighbouring bombs = dig recursively

        self.dug.add((row, col)) #to keep track of dug locations 

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        #for slef.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue #dont dig where we've already dug

                self.dig(r,c)

        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep



def play(dim_size=  10, num_bombs = 10):  #plays the game

    #Step1 = create the board and plants the bombs
    board = Board(dim_size, num_bombs)
    #Step2 = display the board to the user and ask them where to dig
    #Step3a = if they dug a bomb GAME OVER!!!!!
    #3b = if location is not a bomb then dig recursively until each squaere is next to a bomb
    
    #step4 = keep repeating step 2 & 3a, 3b until there are no more places to dig (A WIN BASICALLY!!!)
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        #deals with 0,0   0, 0    0,  0
        user = re.split(",(\\s)*",input("Choose your location: input as row, column: "))
        row, col =  int(user[0]), int(user[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Not a valid LOCATION!!")
            continue

        #if user inputs valid
        safe = board.dig(row,col)
        if not safe:
            break  #found a bomb so game over

    #2ways to exit : 1- dug a bomb   2- no spaces left to dig
    if safe:
        print("you actually won. Absolute madlad")
    else:
        print("Sorry, you lost..")
        board.dug = [(r , c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()