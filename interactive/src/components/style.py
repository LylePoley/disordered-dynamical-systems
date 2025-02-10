""" This file contains the CSS styles for the components in the app. """

SIDEBAR_WIDTH = 20

TITLE = {
    'text-align': 'center',
    'font-size': '2rem',
    'font-weight': 'bold',
    'margin-bottom': '2rem'
}

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
    'width': f'{0.9*SIDEBAR_WIDTH}rem',
    'align': 'center',
}

SIDEBAR_LABELLED_INPUT = {
    'flex': '1',
    'flex-direction': 'column',
    'width': f'{0.85*SIDEBAR_WIDTH}rem',
    'align': 'center',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem"
}


TITLE_DIV = {
    "margin-left": f"{10 + SIDEBAR_WIDTH}rem",
    "margin-right": "10rem",
    "margin-top": "5rem",
    # "padding": "2rem 1rem",
}


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT = {
    "margin-left": f"{3 + SIDEBAR_WIDTH}rem",
    "margin-right": "3rem",
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
    'width': f'{0.85*SIDEBAR_WIDTH}rem'
}

