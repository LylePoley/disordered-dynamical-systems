import numpy as np
from .constants import BUFFER_SIZE, N

t0_index = 0 # zero point of the updating plot

sigma = 1.0
mu = 0.0
z = np.random.normal(0.0, 1.0, (N, N))
alpha = mu/N + sigma*z/np.sqrt(N)
t0 = 0.0
y0 = np.random.uniform(0, 1, N)

t = np.zeros(BUFFER_SIZE)
y = np.zeros((N, BUFFER_SIZE))
t[0] = t0
y[:, 0] = y0