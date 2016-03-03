from math import exp, log
#cartpole_default_params
from pyrlcade.state.breakout_custom_reward import breakout_custom_reward

runtype='sarsa'

#A handy name for this run. The data file will be given this name as
#<resultsdir><simname><version>.h5py
simname = 'breakout_test'
version = '11'
results_dir = '/home/erdem/Desktop/pyrlcade-master/results/'

rom_file='/home/erdem/Desktop/Arcade-Learning-Environment-0.5.1/roms/breakout.bin'

custom_reward_class = breakout_custom_reward()

#if load_name is set, then the simulation will load this file and resume from there, this is useful for watching the behavior of a trained agent
#load_name = '../results/cartpole_sarsa_test1.1.h5py'

data_dir = '/home/erdem/Desktop/pyrlcade-master/data/'
save_interval = 60*60

#run for a total number of episodes
train_episodes=40000
max_steps=40000

use_float32=True

random_seed = 4
initial_r_sum_avg=-40

reward_multiplier=1.0

#learning_rate = 0.4
learning_rate = 0.6
learning_rate_decay_type='geometric'
learning_rate_decay=0.99997
learning_rate_min=0.01

save_images=False
image_save_dir="/home/erdem/Desktop/pyrlcade-master/images/" #I Guess that underutilized windows partitition with all that storage is good for something...

qsa_type='tabular'

#decay_type can be 'geometric' or 'linear'
decay_type='geometric'
epsilon=0.4
epsilon_min=0.015
#epsilon_decay=exp((log(epsilon_min) - log(epsilon))/10000.0)
#print("epsilon_decay: " + str(epsilon_decay))
epsilon_decay=0.9998
#epsilon_decay = (epsilon - epsilon_min)/10000
gamma=0.999

epsilon_reset_count = 1

action_type='e_greedy'

rl_algo='sarsa'

#If defined, will print the state variables on every frame
print_state_debug=True

#in sarsa mode, this tells if the SDL display should be enabled. Set to False if the machine does not have pygame installed
vis_type='pyrlcade'

#in sarsa mode, this tells how often to display, -1 for none
showevery=100
fastforwardskip=10

#these affect the display. They tell the size in pixels of the display, the axis size, and how many frames to skip
display_width=1280
display_height=720
axis_x_min=-10.0
axis_x_max=10.0
axis_y_min=-5.5
axis_y_max=5.5
fps=60
ale_frame_skip=4
