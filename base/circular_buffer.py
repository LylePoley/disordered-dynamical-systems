'''
    Simple circular buffer implementation

'''
import numpy as np

class CircularBuffer: 
    def __init__(self, size): 
        self.size = size 
        self.buffer = np.zeros(size) 
        self.index = 0 

    def append(self, value): 
        self.buffer[self.index] = value 
        self.index = (self.index + 1) % self.size 
        
    def get(self): 
        return np.roll(self.buffer, -self.index)
    

