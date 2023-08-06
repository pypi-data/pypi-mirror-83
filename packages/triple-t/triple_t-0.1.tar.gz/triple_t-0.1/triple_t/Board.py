class Board():
    def __init__(self, length= 3, width = 3):
        self.length = length
        self.width = width 
        self.game_board = []
        print("Created Board")
        
    def initialize_board(self):
        self.game_board = [['-']*self.width for _ in range(self.length)]
    
    def __repr__(self):
        out = ""
        for i in range(self.length):
            for j in range(self.width):
                out = out + self.game_board[i][j]
            out = out + '\n'
        return out