from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from src.components.registers import ids, initial_values, types
from src.components import style

z_store = dcc.Store(
    id=ids.interaction_noise,
    data=initial_values.interaction_noise
)

z_reset_button = dbc.Button(
    'Reset z',
    id=ids.interaction_noise_reset_button,
    color='primary',
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.interaction_noise, 'data'),
        Input(ids.interaction_noise_reset_button, 'n_clicks'),
        State(ids.number_of_agents, 'data'),
        prevent_initial_call=True
    )
    def reset_interaction_noise(n_clicks: int, number_of_agents: int) -> types.Matrix:
        return np.random.normal(0, 1, (number_of_agents, number_of_agents))

    return html.Div([z_reset_button, z_store], style=div_style)
