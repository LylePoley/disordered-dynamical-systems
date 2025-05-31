from dash import Dash, html, dcc, Output, Input, State
from constants import ids
from components.variables.dynamical_system import id_to_dynamical_system, GeneralisedLotkaVolterra


def render(app: Dash, class_name: str | None = None) -> html.Div:

    @app.callback(
        Output(ids.display_equation_latex, 'children'),
        Output(ids.display_equation_description, 'children'),
        Input(ids.integrate_button, 'n_clicks'),
        State(ids.dynamical_system_dropdown, 'value'),
    )
    def update_display_equation(n_clicks: int, dynamical_system_id: str) -> str:
        dynamical_system = id_to_dynamical_system(dynamical_system_id)

        return (dynamical_system.latex_equation + ",",
        f"Currently displaying solutions to {dynamical_system.id} equations:")

    title = "Disordered dynamical systems explorer"

    explanatory_text = [
        r"""
        This is an interactive tool to explore the dynamics of disordered
        dynamical systems with pairwise interactions. It includes The
        $N \times N$ matrix $\underline{\underline{\alpha}}$ encodes the
        interactions between the different agents in the model.
        $\underline{\underline{\alpha}}$ is a random matrix whose elements
        are drawn identically and independently from a Gaussian distribution
        with mean $\frac{\mu}{N}$ and variance $\frac{\sigma^2}{N}$. The
        'Re-draw noise' button re-generates these random interaction
        coefficients.""",
        f"""
        Currently displaying solutions to {GeneralisedLotkaVolterra.id} equations:""",
        f"{GeneralisedLotkaVolterra.latex_equation}, ",

        r"""
        where $y_i$ is the state of agent $i$ and $\alpha_{ij}$ is the
        interaction strength between agents $i$ and $j$. The plot shows all
        trajectories $y_i$ through time."""
    ]

    title = html.Div([
        html.H1(title, className="title"),
        html.Hr(),
        dcc.Markdown(explanatory_text[0], mathjax=True, className="text"),
        html.Hr(),
        dcc.Markdown(explanatory_text[1], id=ids.display_equation_description,
                     mathjax=True, className="text"),
        dcc.Markdown(explanatory_text[2], mathjax=True, className="display-equation", id=ids.display_equation_latex),
        dcc.Markdown(explanatory_text[3], mathjax=True, className="text"),
    ], className=class_name)

    return title
