#!/usr/bin/env python
import numpy as np

import pygame
from ale_python_interface import ALEInterface


class visualize_sdl(object):
    def init_vis(self,p):
        pygame.init()
        (display_width,display_height) = (1280,720)
        self.screen = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption("Arcade Learning Environment Agent Display")
        self.game_surface = None

        self.clock = pygame.time.Clock()
        self.delay = p['fps']
        self.framenum = 0

    #call this every iteration to slow down to real time
    def delay_vis(self):
        if(self.delay >= 0):
            self.clock.tick(self.delay)

    #call this to update the visualization event loop
    #return True if the user wants to exit. return False otherwise
    def update_vis(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True;
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True;
        return False

    def get_keys(self):
        keys = [];
        pressed = pygame.key.get_pressed()
        keys.append(pressed[pygame.K_z])
        keys.append(pressed[pygame.K_LEFT])
        keys.append(pressed[pygame.K_RIGHT])
        keys.append(pressed[pygame.K_UP])
        keys.append(pressed[pygame.K_DOWN])
        return keys

    #call this before calling update vis
    def draw_pyrlcade(self,ale,stats):
        #Init game surface here to avoid needing game screen dims in the init function
        if(self.game_surface is None):
            (screen_width,screen_height) = ale.getScreenDims()
            self.game_surface = pygame.Surface((screen_width,screen_height))

        #clear screen
        self.screen.fill((0,0,0))

        #get atari screen pixels and blit them
        #numpy_surface = np.frombuffer(self.game_surface.get_buffer(),dtype=np.uint32)
        #ale.getScreenRGB(numpy_surface)
        #del numpy_surface

        screen_surface = pygame.surfarray.make_surface(ale.getScreenRGB())
        screen_surface = pygame.transform.rotate(screen_surface, 90)
        screen_surface = pygame.transform.flip(screen_surface, False,True)
        self.game_surface = screen_surface

        # self.game_surface. blit(numpy_surface,(0,0))
        self.screen.blit(pygame.transform.scale(self.game_surface,(self.game_surface.get_width()*3,self.game_surface.get_height()*3)),(0,0))

        #get RAM
        ram_size = ale.getRAMSize()
        ram = np.zeros((ram_size),dtype=np.uint8)
        ale.getRAM(ram)

        #Display ram bytes
        font = pygame.font.SysFont("Ubuntu Mono",32)
        text = font.render("RAM: " ,1,(255,208,208))
        self.screen.blit(text,(490,10))

        font = pygame.font.SysFont("Ubuntu Mono",25)
        height = font.get_height()*1.2

        line_pos = 40
        ram_pos = 0
        while(ram_pos < 128):
            ram_string = ''.join(["%02X "%ram[x] for x in range(ram_pos,min(ram_pos+16,128))])
            text = font.render(ram_string,1,(255,255,255))
            self.screen.blit(text,(500,line_pos))
            line_pos += height
            ram_pos +=16
        
        #display current action
        if(stats is not None):
            font = pygame.font.SysFont("Ubuntu Mono",32)
            text = font.render("Current Action: " + str(stats['action']) ,1,(208,208,255))
            height = font.get_height()*1.2
            self.screen.blit(text,(490,line_pos))
            line_pos += height

            #display reward
            font = pygame.font.SysFont("Ubuntu Mono",30)
            text = font.render("Total Reward: " + str(stats['total_reward']) ,1,(208,255,255))
            self.screen.blit(text,(490,line_pos))
            line_pos += height

            #display state
            font = pygame.font.SysFont("Ubuntu Mono",20)
            state = stats['state'][0:20]
            if(stats['state'].dtype == np.int64):
                text_str = "State: " + ''.join(["%02d "%x for x in state])
            else:
                text_str = "State: " + ''.join(["%8.4f "%x for x in state])
            text = font.render(text_str,1,(208,208,255))
            self.screen.blit(text,(490,line_pos))

            #display episodes below game
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Episode: " + str(stats['episode']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #alpha
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Average Reward: " + str(stats['r_sum_avg']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #alpha
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Learning Rate: " + str(stats['learning_rate']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #gamma
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Gamma: " + str(stats['gamma']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #current epsilon
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Epsilon: " + str(stats['epsilon']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #min epsilon
            line_pos += height
            font = pygame.font.SysFont("Ubuntu Mono",25)
            text = font.render("Epsilon Minimum: " + str(stats['epsilon_min']) ,1,(255,255,255))
            self.screen.blit(text,(490,line_pos))

            #display nnet state
            if(stats.has_key('nnet_state')):
                font = pygame.font.SysFont("Ubuntu Mono",20)
                line_pos=640
                state_pos=0
                state = stats['nnet_state']
                state_size = state.size
                join_str = "NNet State "
                while(state_pos < state_size):
                    text_str = join_str + ''.join(["%3.3f "%state[x] for x in range(state_pos,min(state_pos+18,state_size))])
                    text = font.render(text_str,1,(208,208,255))
                    if(line_pos > self.game_surface.get_height):
                        break
                    self.screen.blit(text,(18,line_pos))
                    join_str = ''
                    line_pos += font.get_height()
                    state_pos += 18



            if(stats['fast_forward']):
                line_pos=30
                font = pygame.font.SysFont("Ubuntu",100)
                text = font.render(("FAST FORWARD"),1,(255,64,64))
                self.screen.blit(text,(300,300))
            elif(stats['save_images']):
                pygame.image.save(self.screen,stats['image_save_dir'] + "frame_" + str(self.framenum) + ".png")
                self.framenum = self.framenum + 1           

        pygame.display.flip()


#this runs a simple keyboard driven test, with no simulator for the cart-pole
if __name__ == '__main__':
    import sys
    key_action_tform_table = (
    0, #00000 none
    2, #00001 up
    5, #00010 down
    2, #00011 up/down (invalid)
    4, #00100 left
    7, #00101 up/left
    9, #00110 down/left
    7, #00111 up/down/left (invalid)
    3, #01000 right
    6, #01001 up/right
    8, #01010 down/right
    6, #01011 up/down/right (invalid)
    3, #01100 left/right (invalid)
    6, #01101 left/right/up (invalid)
    8, #01110 left/right/down (invalid)
    6, #01111 up/down/left/right (invalid)
    1, #10000 fire
    10, #10001 fire up
    13, #10010 fire down
    10, #10011 fire up/down (invalid)
    12, #10100 fire left
    15, #10101 fire up/left
    17, #10110 fire down/left
    15, #10111 fire up/down/left (invalid)
    11, #11000 fire right
    14, #11001 fire up/right
    16, #11010 fire down/right
    14, #11011 fire up/down/right (invalid)
    11, #11100 fire left/right (invalid)
    14, #11101 fire left/right/up (invalid)
    16, #11110 fire left/right/down (invalid)
    14  #11111 fire up/down/left/right (invalid)
    )
    ale = ALEInterface()

    v = visualize_sdl()

    p = {}
    p['fps'] = 60
    v.init_vis(p)
    ale.loadROM(sys.argv[1])
    while 1:
        v.delay_vis()
        pressed = v.get_keys()
        keys = 0
        keys |= pressed[3]
        keys |= pressed[4]  << 1
        keys |= pressed[1]  << 2
        keys |= pressed[2]  << 3
        keys |= pressed[0]  << 4
        a = key_action_tform_table[keys]

        reward = ale.act(a);

        v.draw_pyrlcade(ale,None)
        exit = v.update_vis()
        if(ale.game_over()):
            exit = True
        if(exit):
            break

