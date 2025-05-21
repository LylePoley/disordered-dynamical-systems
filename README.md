# Disordered dynamical system explorer
## Installation
If you already have poetry installed on your system:
1. Clone the repository to a local directory.
2. Open a terminal inside the directory and run `poetry install`. This will create a virtual environment with the required dependencies.
3. Activate the virtual environment by running `poetry env activate` in the terminal.

If you don't have poetry, you can follow the instructions to install it [here](https://github.com/python-poetry/install.python-poetry.org).

Alternatively, you can read the dependencies off from `pyproject.toml`.

## Running the app
To run the app, run `./interactive/main.py` and copy the address from the output in the terminal into a browser.

## Purpose
This is a dash app which is intended to help get an intuition for the behaviour of large disordered dynamical systems. Specifically, disordered dynamical systems which are composed of $N$ interacting agents $x_i(t)$ following dynamics of the form
$$
\dot x_i = f\left(x_i, \sum_{j\neq i}\alpha_{ij}x_j\right),
$$
where $\alpha_{ij}$ dictates the influence of agent $j$ on agent $i$.

Each system which can be selected from the dropdown menu exhibits different dynamical behaviours depending on the interaction coefficients $\alpha_{ij}$. Generally speaking, if the variance of the interaction coefficients ($\sigma$) is small and the mean value ($\mu$) is negative, then the dynamics are likely to settle into a steady state. Increasing the variance of interactions can result in chaotic or oscillatory dynamics. Increasing the mean interaction strength to positive values can cause the dynamics to diverge in some cases.

For example, the Generalised Lotka-Volterra equations can exhibit the following three dynamical behaviours.
1. Setting $\mu=0$ and $\sigma=0.5$ is very likely to lead to dynamics which eventually settle into a steady state. Further, if the initial condition is re-drawn *without* redrawing the interaction matrix, then the corresponding dynamics will settle into the same steady state. In other words, the steady state is independent of the initial conditions.
2. Setting $\mu=-20$ and $\sigma=3$ is likely to produce dynamical systems which will either not settle into a steady state, or tha will settle into a steady state that *does* depend on the initial condition.
3. Setting $\mu=2$ and $\sigma=1$ is likely to produce dynamics which diverge. That is, the values of $y_i$ will eventually blow up to $\infty$.
