integration = r"""Integrates the dynamics in the range $0<t<T$. Note that the
            plot will not change if none of the interaction matrix, initial
            condition, or dynamical system are changed."""

time_final = r"""The dynamics are integrated from $t=0$ to $t=T$.
                  Larger values of $T$ will lead to longer integration
                  times."""

number_of_agents = r"""The number of agents in the simulation. Whilst analysis
                  of large disordered dynamical systems tend to assume that
                  $N\to\infty$, the behaviour of the model for $N\approx50$
                  to $100$ is qualitatively similar. Larger values fo $N$
                  will result in longer waiting times for the integration
                  to complete."""

interaction_standard_deviation = (
    r"""$\frac{\sigma^2}{N}$ is the variance of the
    distribution from which the elements of
    $\underline{\underline{\alpha}}$ are generated. For large
    enough $N$, we have""",

    r"""$$\sigma^2 = \frac{1}{N}\sum_{ij}\left(\alpha_{ij}
    - \frac{\mu}{N}\right)^2.$$"""
)

interaction_noise = r"""Re-generates the interaction coefficients $\alpha_{ij}$
                from a Gaussian distribution with mean $\frac{\mu}{N}$ and
                variance $\frac{\sigma^2}{N}$. Below is a heatmap of the
                interaction matrix."""

interaction_mean = (
    r"""$\frac{\mu}{N}$ is the mean value of the distribution
    from which the elements of $\underline{\underline{\alpha}}$
    are generated. For large enough $N$, we have""",

    r"""$$\mu = \frac{1}{N}\sum_{ij}\alpha_{ij}.$$"""
)

initial_condition = r"""Re-generates the initial condition $y_i(0)$. Each $y_i(0)$ is
            drawn from a uniform distribution in the range $[0, 1]$."""

dynamical_system = """Select which dynamical system to integrate.
    On pressing the 'integrate' button, the selected
    dynamical system will be integrated and the results displayed."""