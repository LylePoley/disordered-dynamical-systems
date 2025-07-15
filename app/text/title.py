from components.variables.dynamical_system import GeneralisedLotkaVolterra

text = []
text.append(
    "Disordered dynamical systems explorer"
)
text.append(
        r"""
        This is an interactive tool to explore the dynamics of disordered
        dynamical systems with pairwise interactions. For each of the dynamical systems available, there are $N$ agents,
        and $\underline{\underline{\alpha}}$ is a matrix containing their pairwise interaction strengths ($\alpha_{ij}$
        encodes the effect of agent $j$ on agent $i$). Each coefficient of the interaction matrix $\underline{\underline{\alpha}}$ is
        drawn independently at random from a Gaussian distribution with mean $\frac{\mu}{N}$ and variance $\frac{\sigma^2}{N}$.
        The options in the sidebar allow you to modify the mean and variance of the interaction statistics ($\mu$ and $\sigma$),
        the number of agents ($N$), as well as the maximum time to integrate the dynamics up to $(T)$. The 'Re-draw noise'
        button re-generates $\underline{\underline{\alpha}}$ with the current parameters, the 'Re-draw initial condition' button
        re-generates the initial conditions for the agents, which are drawn from a uniform distribution in the interval $[0, 1]$.
        No integration is performed until the 'Integrate dynamics' button is pressed.
        """
)
text.append(
        f"""
        Currently displaying solutions to {GeneralisedLotkaVolterra.id} equations:"""
)
text.append(
        f"{GeneralisedLotkaVolterra.latex_equation}, "
)
text.append(
        r"""
        where $y_i$ is the state of agent $i$ and $\alpha_{ij}$ is the
        interaction strength between agents $i$ and $j$. The plot shows all
        trajectories $y_i$ through time."""
)



