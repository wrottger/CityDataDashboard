import pandas  # DO NOT REMOVE IMPORT
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from collections import deque

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "https://fonts.googleapis.com/css?family=Noto+Sans"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="City Data Dashboard", update_title=False)

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


@app.callback(
    Output("sound-gauge", "figure"),
    Input("fast-interval", "n_intervals"))
def display_area(y):
    with open("data/loudness", 'r') as f:
        decibel = int(float(f.readline()))
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=decibel,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Lärmpegel"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "rgb(25, 55, 89)"},
               'steps': [
                   {'range': [0, 65], 'color': "rgb(193,205,13)"},
                   {'range': [65, 80], 'color': "orange"},
                   {'range': [80, 100], 'color': "red"}]}
    ))
    fig.update_layout(
        margin=dict(l=40, r=40)
    )
    return fig


@app.callback(
    Output("sound-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    with open("data/loudness", 'r') as f:
        decibel = int(float(f.readline())) / 100
    historic_sound.append(decibel)
    fig = px.line(list(historic_sound), labels=None, title='<br>          Historischer Lärmpegel')
    fig.update_layout(
        margin=dict(l=20, r=10),
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        yaxis_tickformat=',.0%',
        plot_bgcolor='rgb(255,255,255)')
    fig.update_yaxes(
        showgrid=True,
        range=[0, 1],
        gridcolor="rgb(240,240,240)")
    fig.update_traces(line_color='rgb(25, 55, 89)')
    return fig


@app.callback(
    Output("traffic-graph", "figure"),
    Input("graph-interval", "n_intervals"))
def display_area(y):
    with open("data/traffic_volume", 'r') as f:
        traffic = int(float(f.readline()))
    historic_traffic.append(traffic)
    fig = px.line(list(historic_traffic), labels=None, title='<br>          Verkehrsaufkommen')
    fig.update_layout(
        margin=dict(l=20, r=10),
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        plot_bgcolor='rgb(255,255,255)'
    )
    fig.update_yaxes(
        showgrid=True,
        range=[0, 6],
        gridcolor="rgb(240,240,240)"
    )
    fig.update_xaxes(showgrid=False)
    fig.update_traces(line_color='rgb(25, 55, 89)')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
