from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import constants, ids, initial_values
from src.components import style

time_final_store = dcc.Store(
    id=ids.time_final, 
    data=initial_values.time_final
)

time_final_input = dcc.Input(
    id=ids.time_final_input, 
    type='number', 
    value=initial_values.time_final, 
    style=style.SIDEBAR_SLIDER
)
time_final_button = dbc.Button(
    'Update final time', 
    id=ids.time_final_button, 
    color='primary', 
    size='sm', 
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.time_final, 'data'),
        Input(ids.time_final_button, 'n_clicks'),
        State(ids.time_final_input, 'value'),
        prevent_initial_call=True
    )
    def update_time_final(n_clicks, time_final):
        return time_final
    
    return html.Div([
        time_final_input, 
        time_final_button, 
        time_final_store], 
        style=div_style
    )

