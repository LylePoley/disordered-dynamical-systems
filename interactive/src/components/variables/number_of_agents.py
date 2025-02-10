from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

number_of_agents_input = dcc.Input(
    id=ids.number_of_agents_input,
    type='number',
    value=initial_values.number_of_agents,
    style=style.SIDEBAR_SLIDER
)


def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Number of agents $N$:', mathjax=True),
        number_of_agents_input
    ], style=style
    )
