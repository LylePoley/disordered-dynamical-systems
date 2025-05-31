from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from constants import ids, initial_values

from text.tooltips import interaction_standard_deviation as tooltip_text

interaction_standard_deviation_input = dcc.Input(
    id=ids.interaction_standard_deviation_input,
    type='number',
    value=initial_values.interaction_standard_deviation
)

interaction_standard_deviation_tooltip = dbc.Tooltip(
    [dcc.Markdown(tooltip_text[0],
                  mathjax=True),
     dcc.Markdown(tooltip_text[1], mathjax=True)],
    target=ids.interaction_standard_deviation_input,
)


def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown(r'Interaction standard deviation $\sigma$:', mathjax=True),
        interaction_standard_deviation_input,
        interaction_standard_deviation_tooltip
    ], className=class_name
    )
