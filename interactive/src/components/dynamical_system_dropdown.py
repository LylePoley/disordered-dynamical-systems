# from dash import Dash, Input, Output, State, html, dcc
# import dash_bootstrap_components as dbc

# from src.components import style, ids, initial_values


# dynamical_system_dropdown = dcc.Dropdown(
#     options=[
#         {'label': dynamical_system.value, 'value': dynamical_system.name}
#           for dynamical_system in DisorderedDynamicalSystems], 
#         id=ids.dynamical_system_dropdown, 
#         value=DisorderedDynamicalSystems.GENERALISED_LOTKA_VOLTERRA.name, 
#         style=style.SIDEBAR_DROPDOWN)


# def render(app: Dash, div_style: str | None = None) -> html.Div:
#     @app.callback(
#         Output(ids.sigma, 'data'),
#         Input(ids.sigma_button, 'n_clicks'),
#         State(ids.sigma_input, 'value'),
#         prevent_initial_call=True
#     )
#     def update_sigma(n_clicks, sigma):
#         return sigma
    
#     return html.Div([sigma_input, sigma_button, sigma_store], style=div_style)


    