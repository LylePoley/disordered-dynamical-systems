from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

interaction_mean_store = dcc.Store(
    id=ids.interaction_mean, data=initial_values.interaction_mean)

interaction_mean_input = dcc.Input(
    id=ids.interaction_mean_input,
    type='number',
    value=initial_values.interaction_mean,
    style=style.SIDEBAR_SLIDER,
    step=0.1
)
interaction_mean_button = dbc.Button(
    'Update mean',
    id=ids.interaction_mean_button,
    color='primary',
    size='sm',
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.interaction_mean, 'data'),
        Input(ids.interaction_mean_button, 'n_clicks'),
        State(ids.interaction_mean_input, 'value'),
        prevent_initial_call=True
    )
    def update_mu(n_clicks: int, interaction_mean: float) -> float:
        return interaction_mean



    return html.Div([
        html.Div([dcc.Markdown('Mean interaction strength $\mu$', mathjax=True)], style=div_style),
        html.Div([interaction_mean_input,
        # interaction_mean_button,
        interaction_mean_store],
        style=div_style)]
    )
