from dash import Dash, dcc, html

from src.components.registers import ids, initial_values

y_store = dcc.Store(
    id=ids.y,
    data=initial_values.y
)


def render() -> html.Div:

    return html.Div([
        y_store
    ]
    )
