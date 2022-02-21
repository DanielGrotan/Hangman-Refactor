class State:
    def __init__(self, game):
        self.game = game
        self.previous_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def on_resize(self, new_width, new_height):
        pass

    def enter_state(self):
        if self.game.state_stack:
            self.previous_state = self.game.state_stack[-1]

        self.game.state_stack.append(self)
        self.game.on_resize_callback.append(self.on_resize)

    def exit_state(self):
        self.game.state_stack.pop()
        self.game.on_resize_callback.pop()
