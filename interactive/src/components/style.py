
SIDEBAR_WIDTH = 20
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": f"{SIDEBAR_WIDTH}rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_DIV = {
    'display': 'flex', 
    'flex-direction': 'row', 
    'width':'10rem'
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
SIDEBAR_BUTTON = {
    'flex': '1',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem",
    'width': f'{0.2*SIDEBAR_WIDTH}rem'
}
SIDEBAR_SLIDER = {
    'flex': '1',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem",
    'width': f'{0.6*SIDEBAR_WIDTH}rem'
}
SIDEBAR_DROPDOWN = {
    'flex': '1',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem",
    'width': f'{0.6*SIDEBAR_WIDTH}rem'
}
HEATMAP = {
    'width': '40rem',
    'height': '40rem',
    'margin-left': '50rem'
}
