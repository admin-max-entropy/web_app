"""home layout"""
import dash
from dash import html

import interface.interface_callback
import pages.config

dash.register_page(__name__, order=4)

layout = html.Div([
    html.Div(html.H5("Federal Reserve Balance Sheet"), className="row"),
    html.Div(id=pages.config.APP_ID_RRP_PANEL, className="row"),
    html.Div(id=pages.config.APP_ID_FOREIGN_RRP_PANEL, className="row"),
    html.Div(id=pages.config.APP_ID_RESERVE_PANEL, className="row"),
    html.Div(id=pages.config.APP_ID_TGA_PANEL, className="row"),
], className="row")
