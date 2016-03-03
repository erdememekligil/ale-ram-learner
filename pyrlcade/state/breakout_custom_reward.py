
class breakout_custom_reward(object):
    def __init__(self):
        self.remaining_lives_ram_loc = 0x39
        self.remaining_lives = 5

    # each ball loss is -8
    def get_custom_reward(self, ram):
        curr_lives = ram[self.remaining_lives_ram_loc]
        if curr_lives < self.remaining_lives:
            self.remaining_lives = curr_lives
            return -8
        elif curr_lives > self.remaining_lives:
            self.remaining_lives = curr_lives
            return 0
        else:
            return 0