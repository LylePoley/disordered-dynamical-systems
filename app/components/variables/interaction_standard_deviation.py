from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from constants import ids, initial_values

interaction_standard_deviation_input = dcc.Input(
    id=ids.interaction_standard_deviation_input,
    type='number',
    value=initial_values.interaction_standard_deviation
)

interaction_standard_deviation_tooltip = dbc.Tooltip(
    [dcc.Markdown(r"""$\frac{\sigma^2}{N}$ is the variance of the
                  distribution from which the elements of
                  $\underline{\underline{\alpha}}$ are generated. For large
                  enough $N$, we have""",
                  mathjax=True),
     dcc.Markdown(r"""$$\sigma^2 = \frac{1}{N}\sum_{ij}\left(\alpha_{ij}
                   - \frac{\mu}{N}\right)^2.$$""", mathjax=True)],
    target=ids.interaction_standard_deviation_input,
)


def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown(r'Interaction standard deviation $\sigma$:', mathjax=True),
        interaction_standard_deviation_input,
        interaction_standard_deviation_tooltip
    ], className=class_name
    )
