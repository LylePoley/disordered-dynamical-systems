import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
from collections import deque
from scipy.integrate import solve_ivp
from streamlit import session_state as state
from utility import CircularBuffer
import plotly.graph_objects as go

''' TODO:   only have the integrator work if the plot needs more data to show
            add button to restart integration (DONE)
            add button to perturb the system
            ability to change the dynamical system
            log scale on the y-axis
            change the integration period
            dropdown box for the number of species 
            abundance distribution
            heatmap of alpha which is modifiable
            replace mu and sigma sliders with input boxes 
'''

def add_to_session_state(name, value):
    if name not in state:
        state[name] = value

add_to_session_state("N", 50)
add_to_session_state("mu", 0.0)
add_to_session_state("sigma", 1.0)
add_to_session_state("z", np.random.normal(0, 1, (state.N, state.N)))
add_to_session_state("t", CircularBuffer((100, )))
add_to_session_state("y", CircularBuffer((100, state.N)))
add_to_session_state("alpha", np.random.normal(0, 1/np.sqrt(state.N), (state.N, state.N)))
add_to_session_state("stream", False)

# intialise t and y
if state.t.filled_values == 0:
    state.t.append(0.0)
if state.y.filled_values == 0:
    state.y.append(np.random.uniform(0, 1, state.N))

def glv(t, y, alpha):
    return y*(1 - y + alpha@y)

@st.fragment
def update_alpha(regenerate_z=False):
    if regenerate_z:
        state.z = np.random.normal(0, 1, (state.N, state.N))
    state.alpha = state.mu/state.N + state.sigma*state.z/np.sqrt(state.N)

def reset_integration_state():
    state.t = CircularBuffer((100, ))
    state.y = CircularBuffer((100, state.N))
    state.t.append(0.0)
    state.y.append(np.random.uniform(0, 1, state.N))

def toggle_streaming():
    state.stream = not state.stream


st.title("Data feed")
st.sidebar.slider("Update every: (seconds)", 0.1, 2.0, value=1.0, key="run_every")

st.sidebar.button("Start integration", disabled=state.stream, on_click=toggle_streaming)
st.sidebar.button("Stop integration", disabled=not state.stream, on_click=toggle_streaming)
st.sidebar.button("Regenerate z", on_click=lambda: update_alpha(True))
st.sidebar.button("Reset integration state", on_click=reset_integration_state)

st.sidebar.number_input("mu", -100.0, 100.0, value=0.0, step=0.1, key="mu", on_change=update_alpha)
st.sidebar.number_input("sigma", 0.0, 100.0, value=1.0, step=0.1, key="sigma", on_change=update_alpha)

if state.stream:
    run_every = state.run_every
else:
    run_every = None

@st.fragment(run_every=run_every)
def update_trajectories():
    solution = solve_ivp(glv, [state.t.end(), state.t.end() + 1], 
                         state.y.end(), args=(state.alpha,), 
                         rtol=1e-5, atol=1e-8, t_eval=np.linspace(state.t.end(), state.t.end() + 1, 10))
    # solution.y.shape
    for t_new, y_new in zip(solution.t, solution.y.T):
        state.t.append(t_new)
        state.y.append(y_new)

    fig = go.Figure(layout_width=800, layout_height=500, layout_xaxis_range=[state.t.start()+1, state.t.end()-1])
    for i in range(state.N):
        fig.add_trace(go.Scatter(x=state.t.get(), y=state.y.get()[:, i], mode='lines', showlegend=False))

    st.plotly_chart(fig)

if state.stream:
    update_trajectories()