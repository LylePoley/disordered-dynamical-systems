from dash import dcc, html

class ButtonDiv(html.Div):
    '''
    A convenience slider class with common attributes.
    '''
    def __init__(self, *, id: float, label: float, n_clicks: int=0, style: dict={'margin' : '10px'}):

        button = html.Button(id=id, n_clicks=n_clicks, style=style)
        
        super().__init__([dcc.Markdown(label, mathjax=True), button])

