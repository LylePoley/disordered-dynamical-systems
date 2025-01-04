
from typing import Callable, Protocol
import numpy as np
from .. import ids

from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components import style, ids, initial_values

from enum import IntEnum

# TODO: add more dynamical systems

class DisorderedDynamicalSystem(Protocol):
    """ dynamical_system(t, y, alpha) -> dy/dt """
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        ...


class GeneralisedLotkaVolterra(DisorderedDynamicalSystem):
    def __init__(self, r: np.ndarray | float = 1.0):
        self.r = r

    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return y*(self.r - y + alpha@y)
    
class Kuramoto(DisorderedDynamicalSystem):
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return alpha@np.sin(y[:, None] - y) # this is wrong
    
class SusceptibleInfectedSusceptible(DisorderedDynamicalSystem):
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return - y + (1 - y) * alpha@y
    
class NeuralNetwork(DisorderedDynamicalSystem):
    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return -y + alpha@self.sigmoid_function(y)


class AvailableSystems(IntEnum):
    GENERALISED_LOTKA_VOLTERRA = 0
    KURAMOTO = 1
    SUSCEPTIBLE_INFECTED_SUSCEPTIBLE = 2
    NEURAL_NETWORK = 3


dynamical_system_id = dcc.Store(
    id=ids.dynamical_system_id, 
    data=AvailableSystems.GENERALISED_LOTKA_VOLTERRA
)

dynamical_system_dropdown = dcc.Dropdown(
    options=[
        {'label': 'Generalised Lotka-Volterra', 'value': AvailableSystems.GENERALISED_LOTKA_VOLTERRA},
        {'label': 'Kuramoto', 'value': AvailableSystems.KURAMOTO},
        {'label': 'Susceptible-Infected-Susceptible', 'value': AvailableSystems.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE},
        {'label': 'Neural Network', 'value': AvailableSystems.NEURAL_NETWORK}
    ],
    id=ids.dynamical_system_dropdown, 
    value=AvailableSystems.GENERALISED_LOTKA_VOLTERRA,
    style=style.SIDEBAR_DROPDOWN
)

# TODO: make a better way to add kwargs specifically for the dynamical system of interest
def id_to_dynamical_system(id: int, **kwargs) -> DisorderedDynamicalSystem:

    if AvailableSystems(id) == AvailableSystems.GENERALISED_LOTKA_VOLTERRA:
        return GeneralisedLotkaVolterra(**kwargs)
    elif AvailableSystems(id) == AvailableSystems.KURAMOTO:
        return Kuramoto(**kwargs)
    elif AvailableSystems(id) == AvailableSystems.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE:
        return SusceptibleInfectedSusceptible(**kwargs)
    elif AvailableSystems(id) == AvailableSystems.NEURAL_NETWORK:
        return NeuralNetwork(**kwargs)
    

def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.dynamical_system_id, 'data'),
        Input(ids.dynamical_system_dropdown, 'value')
    )
    def update_dynamical_system_dropdown(dynamical_system_id):
        return dynamical_system_id
    
    return html.Div([dynamical_system_dropdown, dynamical_system_id], style=div_style)