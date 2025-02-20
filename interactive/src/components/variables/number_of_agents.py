from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values

number_of_agents_input = dcc.Input(
    id=ids.number_of_agents_input,
    type='number',
    value=initial_values.number_of_agents
)

number_of_agents_tooltip = dbc.Tooltip(
    [dcc.Markdown(r"""The number of agents in the simulation. Whilst analysis of large disordered dynamical systems tend to assume that $N\to\infty$, the behaviour of the model for $N\approx50$ to $100$ is qualitatively similar. Larger values fo $N$ will result in longer waiting times for the integration to complete.""", mathjax=True)],
    target=ids.number_of_agents_input,
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Number of agents $N$:', mathjax=True),
        number_of_agents_input,
        number_of_agents_tooltip
    ], className=class_name
    )
