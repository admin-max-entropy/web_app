"""home layout"""
import dash
from dash import html
import interface.interface_callback
dash.register_page(__name__, path="/")

layout = html.Div([
    html.Div(html.H5("Reserve Conditions Indicators"), className="row"),
    html.Div(children=[interface.interface_callback.iorb_effr_panel()], className="row"),
    html.Div(children=[interface.interface_callback.elasticity_panel()], className="row"),
    html.Div(children=[interface.interface_callback.overdraft_panel()], className="row")
], style={"padding-left": "10px", "padding-right": "10px"})
