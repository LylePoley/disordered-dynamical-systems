from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

interaction_standard_deviation_input = dcc.Input(
    id=ids.interaction_standard_deviation_input,
    type='number',
    value=initial_values.interaction_standard_deviation,
    style=style.SIDEBAR_SLIDER
)


def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Interaction standard deviation $\sigma$:', mathjax=True),
        interaction_standard_deviation_input
    ], style=style
    )
