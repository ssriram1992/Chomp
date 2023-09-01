# https://www.math.ucla.edu/~tom/Games/chomp.html
# https://en.wikipedia.org/wiki/Chomp

# Chomp is a two-player strategy game played on a rectangular grid of squares.
# The grid is arbitrarily large, and may even be infinite. The top left
# square is poisoned; the player who eats this square loses. Players alternate
# turns, and on a given turn a player must eat a square in the bottom right
# corner of the grid, or in the same row or column as a square that has
# already been eaten. The game ends when the poisoned square has been eaten.

# The following code is a simple implementation of the game. It is not
# optimized for speed or memory usage, but it is easy to understand and
# modify. It is written in Python 3, but should be easy to port to Python 2.

# %%
import random
import numpy as np

# %%
# The following class represents a rectangular grid of squares. Each square
# is either poisoned or not poisoned. The top left square is poisoned, and
# the rest are not poisoned. The grid is represented as a 2D array of booleans.
# The grid is indexed by row and column, with the top left square being
# (0, 0). The grid is immutable, and cannot be resized after it is created.
# The grid is also hashable, so it can be used as a key in a dictionary.
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows, cols), True, dtype=int)
        Grid.winnables = []
        Grid.losables = []
        self.move = None
        self.bestMove = (rows-1, cols-1)
        # self.grid[0, 0] = True

    def __hash__(self):
        return hash(self.grid.tobytes())

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return repr(self.grid)

    def hasArray(self, arr, arrList):
        for a in arrList:
            if np.array_equal(a[0], arr):
                # print("Found array ", a)
                self.move = a[1]
                return True
        return False
    # Returns True if the square at (row, col) is in the grid.
    def is_in_grid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_eatable(self, row, col, testGrid=None):
        if not self.is_in_grid(row, col):
            print("Square is not in grid")
            return False
        if testGrid is None:
            testGrid = self.grid
        return testGrid[row, col]

    # Returns a new grid that is the result of eating the square at (row, col).
    # The square at (row, col) must be poisoned.
    def eat(self, row, col, testGrid=None, onSelf=True):
        if testGrid is None:
            testGrid = self.grid
        if onSelf:
            myCpy = testGrid
        else:
            myCpy = np.copy(testGrid)
        if not self.is_eatable(row, col, myCpy):
            print("Square is not eatable")
            return myCpy
        for i in range(row, self.rows):
            for j in range(col, self.cols):
                myCpy[i, j] = False
        return myCpy

    def trivialWins(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid
        if np.sum((testGrid)) == 0:
            return True
        if np.sum((testGrid)) == 1:
            return False
        if np.sum(testGrid[0,1:]) == 0 or np.sum(testGrid[1:,0]) == 0:
            return True
        if np.sum(testGrid) == self.rows*self.cols:
            return True
        if np.sum(testGrid) == self.rows*self.cols - 1:
            return False
        if np.sum(sum(testGrid)) == 2:
            return True
        if testGrid[1,1] == False:
            if np.sum(testGrid[0,1:]) == np.sum(testGrid[1:,0]):
                return False
            else:
                return True 
        if testGrid[2, 0] == False:
            if np.sum(testGrid[0,:]) == np.sum(testGrid[1,:])+1:
                return False
            else:
                return True
        if testGrid[0, 2] == False:
            if np.sum(testGrid[:,0]) == np.sum(testGrid[:,1])+1:
                return False
            else:
                return True
        return None
    
    def isWin(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid
        ans = self.trivialWins(testGrid)
        if ans is not None:
            self.bestMove = "Trivial"
            return ans
        if self.hasArray(testGrid, Grid.winnables):
            self.bestMove = self.move
            return True
        if self.hasArray(testGrid, Grid.losables):
            self.bestMove = None
            return False
        for (row, col) in self.next_states(testGrid):
            myCpy = self.eat(row, col, testGrid, False)
            ans = self.isWin(myCpy)
            if not ans:
                Grid.winnables.append((testGrid.copy(), (row, col)))
                self.bestMove = (row, col)
                return True
        Grid.losables.append((testGrid.copy(), (0, 0)))
        self.bestMove = None
        return False
    
    def printGrid(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid
        for i in range(self.rows):
            for j in range(self.cols):
                if testGrid[i, j]:
                    print("O", end="")
                else:
                    print("X", end="")
            print()
        print()

    def takeEatInput(self):
        row = int(input("Enter row: "))
        col = int(input("Enter col: "))
        return self.eat(row, col, self.grid, True)

    def sequentialMove(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid 
        for col in range(self.cols):    
            for row in range(self.rows):
                if testGrid[self.rows - row-1, self.cols - col-1]:
                    return (self.rows - row-1, self.cols - col-1)
    
    def randomMove(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid 
        while True:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
            if testGrid[row, col]:
                return (row, col)
    
    # Returns a list of all possible grids that can be reached in one move.
    # The list is empty if the grid is in a terminal state.
    def next_states(self, testGrid=None):
        if testGrid is None:
            testGrid = self.grid 
        for row in range(self.rows):
            for col in range(self.cols):
                if testGrid[row, col]:
                    yield (row, col)
    

# %%
G = Grid(7, 4)
# while np.sum(G.grid)>=1:
#     G.printGrid()
#     print(G.isWin())
#     print(G.bestMove)
#     G.takeEatInput()

while np.sum(G.grid) >= 1:
    G.printGrid()
    win = G.isWin()
    if win:
        if G.bestMove == "Trivial":
            print("Trivial win")
            G.bestMove = (G.rows-1, G.cols-1)
            if G.is_eatable(*G.bestMove):
                print("Playing best move: ", G.bestMove)
                G.eat(*G.bestMove)
            else:
                break
        else:
            print("Playing best move: ", G.bestMove)
            G.eat(*G.bestMove)
    else:
        rndMv = G.sequentialMove()
        print("Playing sequential move: ", rndMv)
        G.eat(*rndMv)
print("Game over!")
for gg in Grid.losables:
    print(gg)
    print()

print(f"Winnable count: {len(Grid.winnables)}")
print(f"Losable count: {len(Grid.losables)}")
# %%
