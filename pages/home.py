import datetime
import dash
from dash import html, dcc, callback, Input, Output
import src.liquidity_monitor
import src.liquidity_monitor
import plotly.graph_objects as go
import interface.interface_utils
import dash_mantine_components as dmc
import interface.config as interface_config
dash.register_page(__name__, path="/")

def iorb_effr_panel():
    start_date = datetime.datetime(2017, 1, 1)
    end_date = datetime.datetime.today()
    time_series = src.liquidity_monitor.iorb_effr_spread(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                     line=dict(color=interface_config.LINE_COLOR, width=interface_config.LINE_WIDTH),
                                showlegend=False))
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=len(list(time_series.values()))*[0],
                                line=dict(color="grey", width=0.5), showlegend=False))
    figure.update_layout(title="EFFR-IORB Spread")
    figure.update_yaxes(title_text="Bps")
    figure = interface.interface_utils.format_figure(figure)
    return dmc.Paper(children=[html.Div(dcc.Graph(figure=figure))], shadow="xs")

layout = html.Div([
    html.Div(children=[iorb_effr_panel()])
])
