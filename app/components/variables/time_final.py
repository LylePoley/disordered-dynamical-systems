from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from constants import ids, initial_values

from text.tooltips import time_final as tooltip_text

time_final_input = dcc.Input(
    id=ids.time_final_input,
    type='number',
    value=initial_values.time_final
)

time_final_tooltip = dbc.Tooltip(
    [dcc.Markdown(tooltip_text, mathjax=True)],
    target=ids.time_final_input,
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Integrate up to time $T$:', mathjax=True),
        time_final_input,
        time_final_tooltip
    ], className=class_name
    )

