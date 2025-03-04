from dash import Dash, dcc, html

from src.components.registers import ids, initial_values

time_store = dcc.Store(
    id=ids.time,
    data=initial_values.time
)


def render() -> html.Div:

    return html.Div([
        time_store
    ]
    )
