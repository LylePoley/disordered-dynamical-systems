from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from constants import ids, initial_values

from text.tooltips import number_of_agents as tooltip_text

number_of_agents_input = dcc.Input(
    id=ids.number_of_agents_input,
    type='number',
    value=initial_values.number_of_agents
)

number_of_agents_tooltip = dbc.Tooltip(
    [dcc.Markdown(tooltip_text,
                  mathjax=True)],
    target=ids.number_of_agents_input,
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Number of agents $N$:', mathjax=True),
        number_of_agents_input,
        number_of_agents_tooltip
    ], className=class_name
    )
