from dash import Dash, html, dcc, Output, Input, State
from src.components import style
from src.components.registers import ids, initial_values
from src.components.variables.dynamical_system import id_to_dynamical_system

def render(app: Dash, style: dict[str, str]) -> html.Div:

    @app.callback(
        Output(ids.display_equation_latex_title, 'children'),
        Output(ids.display_equation_description_title, 'children'),
        Input(ids.integrate_button, 'n_clicks'),
        State(ids.dynamical_system_dropdown, 'value'),
    )
    def update_display_equation(n_clicks: int, dynamical_system_id: str) -> str:
        dynamical_system = id_to_dynamical_system(dynamical_system_id)

        # display_title.children = dynamical_system.latex_equation
        return dynamical_system.latex_equation + ",", f"Currently displaying {dynamical_system.id} equations:"

    title = html.Div([
        html.H1("Disordered dynamical systems explorer"),
        html.Hr(),
        dcc.Markdown(r"""
        This is an interactive tool to explore the dynamics of disordered dynamical systems with pairwise interactions. The $N \times N$ matrix $\underline{\underline{\alpha}}$ encodes the interactions between the different agents in the model. $\underline{\underline{\alpha}}$ is a random matrix whose elements are drawn identically and independently from a Gaussian distribution with mean $\mu$ and variance $\sigma^2$. The 'Re-draw noise' button re-draws these random interaction coefficients.""", mathjax=True),
        html.Hr(),
        html.P("""
        Currently displaying Generalised Lotka-Volterra equations:""", id=ids.display_equation_description_title),
        dcc.Markdown(r"""
                    $$\frac{dy_i}{dt} = y_i\left(1 - xyi + \sum_j \alpha_{ij}y_j\right),$$
                     """, mathjax=True, style={'text-align': 'center'}, id=ids.display_equation_latex_title),
        dcc.Markdown(r"""
        where $y_i$ is the state of agent $i$ and $\alpha_{ij}$ is the interaction strength between agents $i$ and $j$. The plot shows all trajectories $y_i$ through time. """, mathjax=True)
    ], style=style)

    return title