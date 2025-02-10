from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

interaction_mean_input = dcc.Input(
    id=ids.interaction_mean_input,
    type='number',
    value=initial_values.interaction_mean,
    style=style.SIDEBAR_SLIDER,
    step=0.1
)

def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Mean interaction strength $\mu$:', mathjax=True),
        interaction_mean_input
    ], style=style
    )
