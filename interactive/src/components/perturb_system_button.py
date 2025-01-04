# from dash import Dash, Input, Output, html, ctx
# import dash_bootstrap_components as dbc

# from src.components import style, ids

# perturb_system_button = dbc.Button('Pause', id=ids.perturb_system_button, color='primary', style=style.SIDEBAR_BUTTON)


# def render(app: Dash, div_style: str | None = None) -> html.Div:
#     @app.callback(
#         Output(ids.plot_updater, 'disabled'),
#         Output(ids.play_button, 'disabled'),
#         Output(ids.pause_button, 'disabled'),
#         Input(ids.play_button, 'n_clicks'),
#         Input(ids.pause_button, 'n_clicks'),
#     )
#     def play_pause_buttons(play_clicks: int, pause_clicks: int) -> bool:
#         if ctx.triggered_id == ids.play_button:
#             return False, True, False
        
#         return True, False, True
    
#     return html.Div([play_button, pause_button], style=div_style)
