from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from constants import ids, initial_values

from text.tooltips import interaction_mean as tooltip_text

interaction_mean_input = dcc.Input(
    id=ids.interaction_mean_input,
    type='number',
    value=initial_values.interaction_mean,
    step=0.1
)

interaction_mean_tooltip = dbc.Tooltip(
    [dcc.Markdown(tooltip_text[0],
                  mathjax=True),
     dcc.Markdown(tooltip_text[1], mathjax=True)],
    target=ids.interaction_mean_input,
)


def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown(r'Mean interaction strength $\mu$:', mathjax=True),
        interaction_mean_input,
        interaction_mean_tooltip
    ], className=class_name
    )
