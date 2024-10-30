"""home layout"""
import dash
from dash import html

import interface.interface_callback
dash.register_page(__name__)

layout = html.Div([
    html.Div(html.H5("Federal Reserve Balance Sheet"), className="row"),
    html.Div(children=[interface.interface_callback.iorb_tgcr_panel()], className="row"),
    html.Div(children=[interface.interface_callback.iorb_sofr_panel()], className="row"),
    html.Div(children=[interface.interface_callback.iorb_bgcr_panel()], className="row"),
    html.Div(children=[interface.interface_callback.iorb_fedfund_panel()], className="row"),
    html.Div(children=[interface.interface_callback.iorb_obfr_panel()], className="row"),
], className="row")
