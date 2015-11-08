#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
import numpy as np

from ale_python_interface import ALEInterface

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)
ale.setInt("frame_skip",4)
ale.setBool('color_averaging', False)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = True
screen = None
if USE_SDL:
  print 'a'
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', False)
  import pygame
  pygame.init()
  screen = pygame.display.set_mode((500,500))
  pygame.display.set_caption("Arcade Learning Environment Agent Display")
  #ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM('/home/erdem/Desktop/Arcade-Learning-Environment-0.5.1/roms/pong.bin')

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

# Play 10 episodes
for episode in xrange(10):
  total_reward = 0
  while not ale.game_over():
    a = legal_actions[randrange(len(legal_actions))]
    # Apply an action and get the resulting reward
    (screen_width,screen_height) = ale.getScreenDims()
    game_surface = pygame.Surface((screen_width,screen_height))
    screen.fill((0,0,0))
    #numpy_surface = np.frombuffer(game_surface.get_buffer(),dtype=np.uint8)
    #ale.getScreenRGB(numpy_surface)
    #del numpy_surface

    scr = ale.getScreenRGB()
    game_surface = pygame.surfarray.make_surface(scr)
    game_surface = pygame.transform.rotate(game_surface, 90)
    game_surface = pygame.transform.flip(game_surface, False,True)

    # numpy_surface = np.empty((screen_height,screen_width,3), dtype=np.uint8)
    # numpy_surface = ale.getScreenRGB(numpy_surface)

    # self.game_surface. blit(numpy_surface,(0,0))
    screen.blit(pygame.transform.scale(game_surface,(game_surface.get_width()*3,game_surface.get_height()*3)),(0,0))
    pygame.display.flip()
    reward = ale.act(a)
    total_reward += reward
    print reward, 'of action', a
  print 'Episode', episode, 'ended with score:', total_reward
  ale.reset_game()
