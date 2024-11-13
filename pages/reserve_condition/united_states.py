"""home layout"""
import dash
from dash import html
import interface.interface_callback
import pages.config

dash.register_page(__name__, order=3)

layout = html.Div([
    html.Div(html.H5("Reserve Conditions Indicators"), className="row"),
    html.Div(id=pages.config.APP_ID_IORB_EFFR, className="row"),
    html.Div(id=pages.config.APP_ID_ELASTICITY, className="row"),
    html.Div(id=pages.config.APP_ID_OVERDRAFT_AVERAGE, className="row"),
    html.Div(id=pages.config.APP_ID_OVERDRAFT_PEAK, className="row"),
    html.Div(id=pages.config.APP_ID_FF_VOLUME, className="row")
], className="row")
