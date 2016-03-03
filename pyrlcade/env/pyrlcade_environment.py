#!/usr/bin/env python
import numpy as np

from pyrlcade.env.ale_python_interface.ale_python_interface import ALEInterface

class pyrlcade_environment(object):
    def __init__(self,rom_file,ale_frame_skip, custom_reward_class):

        self.ale = ALEInterface()

        self.max_frames_per_episode = self.ale.getInt("max_num_frames_per_episode");
        self.ale.setInt("random_seed",123)
        self.ale.setBool("color_averaging",1)
        self.ale.setInt("frame_skip",ale_frame_skip)
        self.ale.setFloat("repeat_action_probability", 0.0)
        # self.ale.setBool('display_screen', True)

        self.ale.loadROM(rom_file)
        self.legal_actions = self.ale.getMinimalActionSet()
        ram_size = self.ale.getRAMSize()
        self.ram = np.zeros((ram_size),dtype=np.uint8)
        self.ale.getRAM(self.ram)

        self.state = self.ale.getRAM(self.ram)

        if custom_reward_class is None:
            self.custom_reward = None
            return
        else:
            self.custom_reward = custom_reward_class

    def reset_state(self):
        self.ale.reset_game()

    def set_action(self,a):
        self.action = a

    def step(self):
        self.reward = self.ale.act(self.action)

        if self.custom_reward is not None:
            self.reward += self.custom_reward.get_custom_reward(self.get_state())

        is_terminal = self.ale.game_over()
        return is_terminal

    def get_state(self):
        self.ale.getRAM(self.ram)
        return self.ram

    def get_reward(self):
        return self.reward

