from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import constants, ids, initial_values

time_final_input = dcc.Input(
    id=ids.time_final_input, 
    type='number', 
    value=initial_values.time_final
)

time_final_tooltip = dbc.Tooltip(
    [dcc.Markdown(r"""The dynamics will be integrated from $t=0$ to $t=T$. Larger values of $T$ will lead to longer integration times.""", mathjax=True)],
    target=ids.time_final_input,
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Integrate up to time $T$:', mathjax=True),
        time_final_input,
        time_final_tooltip
    ], className=class_name
    )

