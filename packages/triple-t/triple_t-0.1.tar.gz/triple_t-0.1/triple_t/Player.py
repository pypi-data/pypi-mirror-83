class Player():
    def __init__(self, state, turn = False):
        self.state = state
        self.turn = turn
        print("Created player {}".format(self.state))
        
        
    def __repr__(self):
        return self.state
    
    