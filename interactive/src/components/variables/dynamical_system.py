
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
        return np.einsum('ij, ij -> i', alpha, np.sin(y[:, None] - y))
    
class SusceptibleInfectedSusceptible(DisorderedDynamicalSystem):
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return - y + (1 - y) * alpha@y
    
class NeuralNetwork(DisorderedDynamicalSystem):
    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return -y + alpha@self.sigmoid_function(y)


class AvailableSystem(IntEnum):
    GENERALISED_LOTKA_VOLTERRA = 0
    KURAMOTO = 1
    SUSCEPTIBLE_INFECTED_SUSCEPTIBLE = 2
    NEURAL_NETWORK = 3

dynamical_system_dropdown = dcc.Dropdown(
    options=[
        {'label': 'Generalised Lotka-Volterra', 'value': AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value},
        {'label': 'Kuramoto', 'value': AvailableSystem.KURAMOTO.value},
        {'label': 'Susceptible-Infected-Susceptible', 'value': AvailableSystem.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE.value},
        {'label': 'Neural Network', 'value': AvailableSystem.NEURAL_NETWORK.value}
    ],
    id=ids.dynamical_system_dropdown, 
    value=AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value,
    style=style.SIDEBAR_DROPDOWN
)

# TODO: make a better way to add kwargs specifically for the dynamical system of interest
def id_to_dynamical_system(id: int, **kwargs) -> DisorderedDynamicalSystem:

    if id == AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value:
        return GeneralisedLotkaVolterra(**kwargs)
    elif id == AvailableSystem.KURAMOTO.value:
        return Kuramoto(**kwargs)
    elif id == AvailableSystem.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE.value:
        return SusceptibleInfectedSusceptible(**kwargs)
    elif id == AvailableSystem.NEURAL_NETWORK.value:
        return NeuralNetwork(**kwargs)
    

def render(app: Dash, div_style: str | None = None) -> html.Div:

    return html.Div([dynamical_system_dropdown], style=div_style)