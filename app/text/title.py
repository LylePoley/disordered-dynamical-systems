from components.variables.dynamical_system import GeneralisedLotkaVolterra

text = []
text.append(
    "Disordered dynamical systems explorer"
)
text.append(
        r"""
        This is an interactive tool to explore the dynamics of disordered
        dynamical systems with pairwise interactions. It includes The
        $N \times N$ matrix $\underline{\underline{\alpha}}$ encodes the
        interactions between the different agents in the model.
        $\underline{\underline{\alpha}}$ is a random matrix whose elements
        are drawn identically and independently from a Gaussian distribution
        with mean $\frac{\mu}{N}$ and variance $\frac{\sigma^2}{N}$. The
        'Re-draw noise' button re-generates these random interaction
        coefficients."""
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



