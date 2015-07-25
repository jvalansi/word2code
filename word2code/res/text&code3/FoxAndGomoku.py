from problem_utils import *
from operator import *

class FoxAndGomoku:
    def win(self, board):
        input_array = board
        # Fox Ciel is going to play Gomoku with her friend Fox Jiro.
        # Ciel plays better, so before they start she allowed Jiro to put some of his pieces on the board.
        
        
        # You are given a String[] board that represents a square board.
        # The character board[i][j] represents the cell with coordinates (i,j).
        # Each of those characters is either '.' (representing an empty cell) or 'o' (representing a cell with Jiro's piece).
        types = ['o','.']
        
        # Of course, Ciel does not want Jiro to win the game before she has a chance to play.
        # Thus she now has to check the board and determine whether there are five consecutive tokens somewhere on the board.
                
        # Determine whether there are 5 consecutive cells (horizontally, vertically, or diagonally) that contain Jiro's tokens.
        #### valid = lambda possibilities: are(len(possibility for possibility in possibilities if contain(tokens[0], possibility)),5) 
        valid = lambda possibilities: eq(len(possibility for possibility in possibilities if contains(types[0], possibility)),5) 
 
        
        # Return "found" (quotes for clarity) if there are five such cells anywhere on the board. Otherwise, return "not found".
        #### return "found" if anywhere(such(cells) for cells in csubsets(board, five)) otherwise "not found"
        return "found" if any(valid(possibility) for possibility in csubsets(input_array, 5)) else "not found"

        
if __name__ == '__main__':
    board = ".ooooo"
    fag = FoxAndGomoku()
    print(fag.win(board))