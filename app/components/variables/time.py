from dash import dcc, html

from constants import ids, initial_values

time_store = dcc.Store(
    id=ids.time,
    data=initial_values.time
)


def render() -> html.Div:

    return html.Div([
        time_store
    ]
    )
