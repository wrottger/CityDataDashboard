import random
import dash
import json
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
        interval=100,
        n_intervals=0
    ),
    dcc.Interval(
        id='graph-interval',
        interval=3000,
        n_intervals=0
    ),
])

historic_sound = deque(maxlen=200)
historic_traffic = deque(maxlen=200)
decibel = 50


@app.callback(
    Output("sound-gauge", "figure"),
    Input("fast-interval", "n_intervals"))
def display_area(y):
    global decibel
    decibel += random.randint(-5, 5)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=decibel,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Lärmpegel"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 65], 'color': "green"},
                   {'range': [65, 80], 'color': "orange"},
                   {'range': [80, 100], 'color': "red"}]}
    ))
    return fig


@app.callback(
    Output("sound-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    historic_sound.append(random.randint(1, 100))
    fig = px.area(list(historic_sound), labels=None, title='<br>          Historischer Lärmpegel')
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    return fig


@app.callback(
    Output("traffic-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    historic_traffic.append(random.randint(1, 100))
    fig = px.area(list(historic_traffic), labels=None, title='<br>          Verkehrsaufkommen')
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
