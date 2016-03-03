# this class implements a tabular storage for a Qsa table
import numpy as np


class breakout_ram_extractor(object):
    def __init__(self, tabular):
        self.divs = np.array([10, 10, 5, 250, 40])

        self.mins = np.array([0x00, 0x1A, 0x00, 0x00, 0x40])
        self.maxs = np.array([0xB2, 0xE9, 0xD1, 0xF0, 0x80])

        self.size = self.maxs - self.mins
        self.size = self.size + self.divs
        self.size = self.size / self.divs

        self.state_size = self.mins.size
        self.state_mins = (np.zeros(self.size.shape)).astype(np.int64)
        self.state_maxs = (self.size - np.ones(self.size.shape)).astype(np.int64)

        self.transform_class = None

        # self.maxx = 0x00
        # self.maxy = 0x00
        # self.minx = 0xFF
        # self.miny = 0xFF

    def set_transform_class(self, transform_class):
        self.transform_class = transform_class

    def get_size_and_range(self):
        return (self.state_size, self.state_mins, self.state_maxs)

    def extract_state(self, ram):
        # ram values
        # 0x46 player_x position 00 to B2
        # 0x73 ball_x position  to
        # 0x75 ball_y position  to

        # player, ballx, bally, velx, vely
        state = np.array(ram[[0x46, 0x63, 0x65, 0x69, 0x6B]])


        # if state[1] > self.maxx:
        #     self.maxx = state[1]
        #
        # if state[1] != 0 and state[1] < self.minx:
        #     self.minx = state[1]
        #
        # if state[2] > self.maxy:
        #     self.maxy = state[2]
        # if state[2] != 0 and state[2] < self.miny:
        #     self.miny = state[2]
        #
        # print "x: {} {} y: {} {}".format(self.minx, self.maxx, self.miny, self.maxy)

        state = state - self.mins
        state = state / self.divs

        vel_y_index = 4

        if state[vel_y_index] == -2:
            state[vel_y_index] = 1
        elif state[vel_y_index] == 2:
            state[vel_y_index] = 1
        return state


if __name__ == '__main__':
    pass
