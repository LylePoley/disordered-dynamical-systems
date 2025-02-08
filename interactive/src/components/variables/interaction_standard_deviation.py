from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

interaction_standard_deviation_store = dcc.Store(
    id=ids.interaction_standard_deviation,
    data=initial_values.interaction_standard_deviation
)

interaction_standard_deviation_input = dcc.Input(
    id=ids.interaction_standard_deviation_input,
    type='number',
    value=initial_values.interaction_standard_deviation,
    style=style.SIDEBAR_SLIDER
)

interaction_standard_deviation_button = dbc.Button(
    'Update standard deviation',
    id=ids.interaction_standard_deviation_button,
    color='primary',
    size='sm',
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.interaction_standard_deviation, 'data'),
        Input(ids.interaction_standard_deviation_button, 'n_clicks'),
        State(ids.interaction_standard_deviation_input, 'value'),
        prevent_initial_call=True
    )
    def update_interaction_standard_deviation(n_clicks, interaction_standard_deviation):
        return interaction_standard_deviation

    return html.Div([
        interaction_standard_deviation_input,
        interaction_standard_deviation_button,
        interaction_standard_deviation_store],
        style=div_style
    )
