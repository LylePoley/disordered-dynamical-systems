import dash
import plotly.express as px
from dash import html, dcc
from dash_extensions.enrich import ServersideOutputTransform, Serverside, DashProxy, Output, Input, State

# Initialize the app with DashProxy
app = DashProxy(__name__, transforms=[ServersideOutputTransform()])

initial_data = Serverside(px.data.gapminder())

app.layout = html.Div([
    html.Button("Query data", id="btn"),
    dcc.Dropdown(id="dd"),
    dcc.Graph(id="graph"),
    dcc.Store(id="store", data=initial_data)
])

@app.callback(
    Output("store", "data"),
    # Input("btn", "n_clicks"),
    # prevent_initial_call=True
)
def query_data():
    import time
    time.sleep(3)  # Emulate slow database operation
    return Serverside(px.data.gapminder())  # No JSON serialization here

@app.callback(
    [Output("dd", "options"), Output("dd", "value")],
    Input("store", "data"),
    prevent_initial_call=True
)
def update_dd(df):
    options = [{"label": column, "value": column} for column in df["year"]]
    return options, options[0]["value"]

@app.callback(
    Output("graph", "figure"),
    Input("dd", "value"),
    State("store", "data"),
    prevent_initial_call=True
)
def update_graph(value, df):
    df = df.query("year == {}".format(value))
    return px.sunburst(df, path=["continent", "country"], values="pop", color="lifeExp", hover_data=["iso_alpha"])

if __name__ == "__main__":
    app.run_server(debug=True)
