#this class implements a tabular storage for a Qsa table
import numpy as np

class boxing_ram_extractor(object):
    def __init__(self,tabular):
        # self.divs = np.array([4, 4, 4, 4, 48, 48, 48, 48])
        # self.localDivs = np.array([8, 8, 8, 8, 16, 16, 16, 16])
        self.localDivs = np.array([8, 8, 8, 8, 48, 48, 48, 48])
        self.divs = np.array([8, 8, 8, 8, 48, 48])

        self.mins = np.array([0x1E,0x03,0x1E,0x03,0x5F,0xBF])
        self.maxs = np.array([0x6D,0x57,0x6D,0x57,0x8F,0xEF])
        self.localMins = np.array([0x1E,0x03,0x1E,0x03,0x5F,0xBF,0x5F,0xBF])
        self.localMaxs = np.array([0x6D,0x57,0x6D,0x57,0x8F,0xEF,0x8F,0xEF])

        self.size = self.maxs - self.mins
        self.size = self.size + self.divs
        self.size = self.size/self.divs

        self.state_size = self.mins.size
        self.state_mins = (np.zeros(self.size.shape)).astype(np.int64)
        self.state_maxs = (self.size - np.ones(self.size.shape)).astype(np.int64)

    def get_size_and_range(self):
        return (self.state_size,self.state_mins,self.state_maxs)

    def extract_state(self,ram):
        #ram values
        #player_x 0x61 (1E - 6D)
        #player_y 0x41 (03 - 57)
        #computer_x 0x77 (1E - 6D)
        #computer_y 0x48 (03 - 57)
        #player_punch_top 0x49 (5F-8F)
        #player_punch_bot 0x4B (BF-EF)
        #computer_punch_top 0x4D (5F-8F)
        #computer_punch_bot 0x4F (BF-EF)
        state = np.array(ram[[0x61, 0x41, 0x77, 0x48, 0x49, 0x4B, 0x4D, 0x4F]])

        state = state - self.localMins
        state = state/self.localDivs

        # for i in xrange(4,8):
        #     if state[i] == 1:
        #         state[i] = 0
        #     elif state[i] > 1:
        #         state[i] = 1

        state[4] = state[4] | state[5]
        state[5] = state[6] | state[7]

        return state[0:6]

if __name__ == '__main__':
    pass
