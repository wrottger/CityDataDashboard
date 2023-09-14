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

app.layout = html.Div([
    html.H3('City Data Dashboard'),
    html.Div([
        html.Div([
            dcc.Graph(id="sound-gauge")
        ], className="four columns"),
        html.Div([
            dcc.Graph(id="sound-graph")
        ], className="four columns"),
        html.Div([
            dcc.Graph(id="traffic-graph")
        ], className="four columns"),
    ], className="row"),
    dcc.Interval(
        id='fast-interval',
        interval=300,
        n_intervals=0
    ),
    dcc.Interval(
        id='graph-interval',
        interval=1000,
        n_intervals=0
    ),
])


@app.callback(
    Output("sound-gauge", "figure"),
    Input("fast-interval", "n_intervals"))
def display_area(y):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=450,
        mode="gauge+number+delta",
        title={'text': "Speed"},
        delta={'reference': 380},
        gauge={'axis': {'range': [None, 500]},
               'steps': [
                   {'range': [0, 250], 'color': "lightgray"},
                   {'range': [250, 400], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))


@app.callback(
    Output("sound-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    pass


@app.callback(
    Output("traffic-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    pass


if __name__ == '__main__':
    app.run_server(debug=True)
