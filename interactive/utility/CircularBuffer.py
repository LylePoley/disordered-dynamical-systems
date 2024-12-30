'''
    Simple circular buffer implementation

'''
import numpy as np


class CircularBuffer: 
    def __init__(self, shape, fill_value=None, **buffer_kwargs): 
        self.shape = shape
        if isinstance(shape, int): 
            self.principal_length = shape
        elif isinstance(shape, tuple): 
            self.principal_length = shape[0]
        else:
            raise ValueError("shape must be an int or a tuple")
            
        self.buffer = np.full(shape, fill_value=fill_value, **buffer_kwargs) 
        self.index = 0 
        self.filled_values = 0

    def end(self):
        return self.buffer[self.index - 1]
    
    def start(self):
        if self.index == -1:
            return self.buffer[-1]
        return self.buffer[(self.index - self.filled_values) % self.principal_length]

    def shape(self):
        return self.buffer.shape

    def append(self, value): 
        self.filled_values = min(self.filled_values + 1, self.principal_length)
        self.buffer[self.index] = value 
        self.index = (self.index + 1) % self.principal_length
        
    def get(self): 
        return np.r_[self.buffer[self.index:], self.buffer[:self.index]]
        # return np.roll(self.buffer, -self.index)
    
    def __repr__(self):
        return str(self.get())

