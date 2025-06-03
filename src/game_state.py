class GameState:
    def __init__(self):
        self.states = ["menu", "recipe_selection", "cooking", "result"]
        self.current_state = "menu"
    
    def set_state(self, state):
        if state in self.states:
            self.current_state = state
        else:
            print(f"Invalid state: {state}")
    
    def get_state(self):
        return self.current_state
