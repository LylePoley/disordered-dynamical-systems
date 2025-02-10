from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import constants, ids, initial_values
from src.components import style

time_final_input = dcc.Input(
    id=ids.time_final_input, 
    type='number', 
    value=initial_values.time_final, 
    style=style.SIDEBAR_SLIDER
)


def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Integrate up to time $T$:', mathjax=True),
        time_final_input
    ], style=style
    )

