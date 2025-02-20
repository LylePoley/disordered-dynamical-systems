# Disordered dynamical system explorer
## Purpose
This is a dash app which is intended to help get an intuition for the behaviour of large disordered dynamical systems. Each system which can be selected from the dropdown menu exhibits different dynamical behaviours depending on the interaction coefficients $\alpha_{ij}$. Generally speaking, if the variance of the interaction coefficients ($\sigma$) is small and the mean value ($\mu$) is negative, then the dynamics are likely to settle into a steady state. Increasing the variance of interactions can result in chaotic or oscillatory dynamics. Increasing the mean interaction strength to positive values can cause the dynamics to diverge in some cases. 

For example, the Generalised Lotka-Volterra equations can exhibit the following three dynamical behaviours. 
1. Setting $\mu=0$ and $\sigma=0.5$ is very likely to lead to dynamics which eventually settle into a steady state. Further, if the initial condition is re-drawn *without* redrawing the interaction matrix, then the corresponding dynamics will settle into the same steady state. In other words, the steady state is independent of the initial conditions. 
2. Setting $\mu=-20$ and $\sigma=3$ is likely to produce dynamical systems which will either not settle into a steady state, or tha will settle into a steady state that *does* depend on the initial condition. 
3. Setting $\mu=2$ and $\sigma=1$ is likely to produce dynamics which diverge. That is, the values of $y_i$ will eventually blow up to $\infty$.

## Running the applet
This is a python only project and will run in a python environment meeting the requirements listed in the .toml file. You can install the dependencies to a python environment yourself, and run main.py. Alternatively, you could use poetry to make the environment and install the necessary dependencies for you.