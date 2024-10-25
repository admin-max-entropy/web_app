"""home layout"""
import dash
from dash import html
import interface.interface_callback
dash.register_page(__name__)

layout = html.Div([
    html.Div(html.H5("Money Market Monitors"), className="row"),
    html.Div(children=[interface.interface_callback.rrp_panel()], className="row"),
    html.Div(children=[interface.interface_callback.foreign_rrp_panel()], className="row"),
    html.Div(children=[interface.interface_callback.reserve_panel()], className="row"),
    html.Div(children=[interface.interface_callback.tga_panel()], className="row"),
    html.Div(children=[interface.interface_callback.sofr_panel()], className="row"),
], className="row")
