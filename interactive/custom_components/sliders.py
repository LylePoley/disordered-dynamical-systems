from dash import dcc, html
from numpy import linspace

class SliderDiv(html.Div):
    '''
    A convenience slider class with common attributes.
    '''
    def __init__(self, id: float, label: float, min: float, max: float, step: float, value: float, number_of_marks: int=21, 
                 tooltip: dict={"placement": "bottom", "always_visible": True}, 
                 style: dict={'margin': '10px', 'margin-bottom': '25px'}):

        slider = dcc.Slider(id=id, min=min, max=max, step=step, value=value, 
                            marks={i: f'{i:.2f}' for i in linspace(min, max, number_of_marks)},
                            tooltip=tooltip)
        
        super().__init__([dcc.Markdown(label, mathjax=True), slider],
                            style=style)

