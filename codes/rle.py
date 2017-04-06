from rle_python_interface import RLEInterface
from random import randrange
import numpy as np

class actionSet:
    def __init__(self, rle): 
        self.minimal_actions = rle.getMinimalActionSet()
        self.n = len(self.minimal_actions)
    
    def sample(self):
        return randrange(len(self.minimal_actions))
    
class rle:
    def __init__(self, rom, core = 'snes', skip_mean = 7):
        self.rle = RLEInterface()
        self.rle.loadROM(rom, core)
        self.action_space = actionSet(self.rle)
        self.skip_mean = skip_mean

    def reset(self):
        self.rle.reset_game()
        state =  np.squeeze(self.rle.getScreenGrayscale(), axis=2)
        return state

    def step(self, action_ix):
        action = self.action_space.minimal_actions[action_ix]
        reward = 0
        for i in range(randrange(self.skip_mean-1, self.skip_mean+2)):
            reward += self.rle.act(action)
            done = self.rle.game_over()
            if done:
                break
        next_state =  np.squeeze(self.rle.getScreenGrayscale(), axis=2)
        return next_state, reward, done, ''

    def seed(self, s):
        self.rle.setInt('random_seed', s)

    
