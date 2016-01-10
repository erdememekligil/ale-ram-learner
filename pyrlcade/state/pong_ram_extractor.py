#this class implements a tabular storage for a Qsa table
import numpy as np

class pong_ram_extractor(object):
    def __init__(self,tabular):
        if(tabular):
            self.divs = np.array([33,5,1,1,5])
            # self.divs = np.array([33,5,5])
        else:
            print('not tabular')
            self.divs = np.array([1,1,1,1,1])
            # self.divs = np.array([1,1,1])
        self.mins = np.array([0x32,0x26,9,7,0x26])
        self.maxs = np.array([0xCD,0xCB,11,13,0xCB])
        # self.mins = np.array([0x32,0x26,0x26])
        # self.maxs = np.array([0xCD,0xCB,0xCB])

        self.size = self.maxs - self.mins
        self.size = self.size + self.divs
        self.size = self.size/self.divs

        self.state_size = self.mins.size
        self.state_mins = (np.zeros(self.size.shape)).astype(np.int64)
        self.state_maxs = (self.size - np.ones(self.size.shape)).astype(np.int64)

        self.transform_class=None

    def set_transform_class(self,transform_class):
        self.transform_class = transform_class

    def get_size_and_range(self):
        return (self.state_size,self.state_mins,self.state_maxs)

    def extract_state(self,ram):
        #ram values
        #0x31 ball x position 32-CD
        #0x36 ball y position (player's was 26-cB)
        #0x3A ball x velocity 9 to 11
        #0x38 ball y velocity 8 to 12
        #0x3c or 0x33 player y 26-CB
        #0x32 computer y
        #state: ball x,ball y, velo y, velo x, player y
        state = np.array(ram[[0x31,0x36,0x3A,0x38,0x3C]])
        # state = np.array(ram[[0x31,0x36,0x3C]])
        #temp = state
        #these are signed bytes
        state[2] += 10
        state[3] += 10
        state = state - self.mins
        state = state/self.divs

        if state[0] < 0:
            state[0] = 0
        if state[1] < 0:
            state[1] = 0
        if state[2] < 0:
            state[2] = 0

        #print 'old {0} new {1}.'.format(temp,state)
        #print('state_2: ' + str(state[2]))
        #print('state_dtype: ' + str(state.dtype))
        if(self.transform_class is None):
            return state
        else:
            return self.transform_class.transform(state)

    #def no_normalize(self,state):
    #    return state

    #def normalize_state(self,state):
    #    s = state.astype(np.float32)
    #    s = np.minimum(s,self.arr_maxs)
    #    s = np.maximum(s,self.arr_mins)
    #    s = s/(self.arr_maxs)
    #    s = s*(self.s_maxs-self.s_mins) + self.s_mins
    #    #s = s-0.5
    #    #s = s*2.25
    #    return s

    def isBallExists(self, state):
        return state[1] >= 0


if __name__ == '__main__':
    pass
