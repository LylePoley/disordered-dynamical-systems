from dash import Dash, Input, Output, State, html, dcc

from src.components import ids, initial_values, constants

t0_index_store = dcc.Store(id=ids.t0_index, data=initial_values.t0_index)


def render(app: Dash) -> html.Div:
    @app.callback(
            Output(ids.t0_index, 'data', allow_duplicate=True),
            Input(ids.plot_updater, 'n_intervals'),
            State(ids.t0_index, 'data'),
            prevent_initial_call=True
    )
    def update_t0_index(n_intervals: int, t0_index):
        return t0_index + constants.TIME_STEPS_UNTIL_NEXT_REFRESH

    
    return html.Div([t0_index_store])
