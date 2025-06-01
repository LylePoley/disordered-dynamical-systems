import dash_bootstrap_components as dbc
from dash import Dash, html

from components.variables import (
    dynamical_system,
    initial_condition,
    interaction_matrix,
    interaction_mean,
    interaction_noise,
    interaction_standard_deviation,
    number_of_agents,
    time_final,
    time,
    y,
)

from components.plots import (
    trajectories,
)

from components import (
    integration,
    title,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.H3(
            "Options", className="display-4"
        ),
        html.Hr(),
        html.P(
            "Select options for the integration.", className="lead"
        ),
        html.Hr(),
        interaction_noise.render(app, class_name="sidebar-button"),
        integration.render(app, class_name="sidebar-button"),
        initial_condition.render(app, class_name="sidebar-button"),


        html.Hr(),
        dynamical_system.render(
            app, class_name="sidebar-dropdown"
        ),
        html.Hr(),

        interaction_mean.render(
            app, class_name="sidebar-input"
        ),

        html.Hr(),
        interaction_standard_deviation.render(
            app, class_name = "sidebar-input"
        ),

        html.Hr(),
        number_of_agents.render(
            app, class_name="sidebar-input"
        ),

        html.Hr(),
        time_final.render(
            app, class_name="sidebar-input"
        ),
    ],
    className="sidebar"
)

main_content = html.Div([
    title.render(app),
    trajectories.render(app, class_name="figure"),
],
className = "main-content"
)

app.layout = html.Div([
    sidebar,
    main_content,

    # invisible components
    interaction_matrix.render(app),
    time.render(),
    y.render()
])

if __name__ == "__main__":
    app.run(port=8050, host='0.0.0.0')
