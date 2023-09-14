import dash
import pandas as pd
import json
import dash_daq as daq
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from collections import deque

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sound_gauge = daq.Gauge(
    color={"gradient": True, "ranges": {"green": [0, 60], "yellow": [60, 80], "red": [80, 100]}},
    value=50,
    label='Lärmpegel',
    max=100,
    min=0,
    id='sound-gauge'
)

sound_graph = dcc.Graph(
    figure={
        'layout': {
            'title': 'Tages Lärmpegel'
        }
    },
    config={
        'displayModeBar': False
    },
    id='sound-graph',
    responsive=True,
)

traffic_volume = dcc.Graph(
    figure={
        'layout': {
            'title': 'Verkehrsaufkommen'
        }
    },
    config={
        'displayModeBar': False
    },
    id='traffic-volume-graph',
    responsive=True,
)

app.layout = html.Div([
    html.H3('City Data Dashboard'),
    html.Div([
        html.Div([
            sound_gauge
        ], className="four columns"),
        html.Div([
            sound_graph
        ], className="four columns"),
        html.Div([
            traffic_volume
        ], className="four columns"),
    ], className="row"),
    dcc.Interval(
        id='interval-component',
        interval=600,  # in milliseconds
        n_intervals=0
    ),
])


@app.callback(
    Output("sound-gauge", "figure"),
    Input("interval-component", "n_intervals"))
def display_area(y):
    fig = daq.Gauge()


@app.callback(
    Output("sound-graph", "figure"),
    Input("interval-component", "n_intervals"))
def display_area(y):
    pass


if __name__ == '__main__':
    app.run_server(debug=True)
