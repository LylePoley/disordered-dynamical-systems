from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values

interaction_mean_input = dcc.Input(
    id=ids.interaction_mean_input,
    type='number',
    value=initial_values.interaction_mean,
    step=0.1
)

interaction_mean_tooltip = dbc.Tooltip(
    [dcc.Markdown(r"""$\frac{\mu}{N}$ is the mean value of the distribution from which the elements of $\underline{\underline{\alpha}}$ are generated. For large enough $N$, we have""", mathjax=True),
     dcc.Markdown(r"""$$\mu = \frac{1}{N}\sum_{ij}\alpha_{ij}.$$""", mathjax=True)],
    target=ids.interaction_mean_input,
)


def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown(r'Mean interaction strength $\mu$:', mathjax=True),
        interaction_mean_input,
        interaction_mean_tooltip
    ], className=class_name
    )
