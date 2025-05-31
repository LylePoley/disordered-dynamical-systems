from dash import Dash, html, dcc, Output, Input, State
from constants import ids
from components.variables.dynamical_system import id_to_dynamical_system, GeneralisedLotkaVolterra
from text.title import text

def render(app: Dash, class_name: str | None = None) -> html.Div:

    @app.callback(
        Output(ids.display_equation_latex, 'children'),
        Output(ids.display_equation_description, 'children'),
        Input(ids.integrate_button, 'n_clicks'),
        State(ids.dynamical_system_dropdown, 'value'),
    )
    def update_display_equation(n_clicks: int, dynamical_system_id: str) -> str:
        dynamical_system = id_to_dynamical_system(dynamical_system_id)

        return (dynamical_system.latex_equation + ",",
        f"Currently displaying solutions to {dynamical_system.id} equations:")

    title = html.Div([
        html.H1(text[0], className="title"),
        html.Hr(),
        dcc.Markdown(text[1], mathjax=True, className="text"),
        html.Hr(),
        dcc.Markdown(text[2], id=ids.display_equation_description,
                     mathjax=True, className="text"),
        dcc.Markdown(text[3], mathjax=True, className="display-equation", id=ids.display_equation_latex),
        dcc.Markdown(text[4], mathjax=True, className="text"),
    ], className=class_name)

    return title
