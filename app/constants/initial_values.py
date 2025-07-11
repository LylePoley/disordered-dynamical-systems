import numpy as np

number_of_agents = 50

# default interaction matrix statistics
interaction_standard_deviation = 1.0
interaction_mean = 0.0
interaction_noise = np.random.normal(0.0, 1.0, (number_of_agents, number_of_agents))
interaction_matrix = interaction_mean/number_of_agents + \
    interaction_standard_deviation*interaction_noise/np.sqrt(number_of_agents)

time_final = 50.0
y0 = np.random.uniform(0, 1, number_of_agents)  # initial condition

time = np.zeros(1)
y = np.zeros((number_of_agents, 1))
time[0] = 0.0
y[:, 0] = y0
