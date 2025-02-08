from dash import Dash, html, dcc
from src.components import style
from src.components.registers import ids, initial_values

def render(app: Dash) -> html.Div:

    title = html.Div([
        html.H1("Disordered dynamical systems explorer", style=style.TITLE),
        dcc.Markdown("""
        This is an interactive tool to explore the dynamics of disordered dynamical systems with pairwise interactions. The \[N\times N\] matrix \[\boldsymbol{\alpha}\] encodes the interactions between the different agents in the model.""")
    ])

    return title