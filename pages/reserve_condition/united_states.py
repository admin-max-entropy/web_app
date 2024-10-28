"""home layout"""
import dash
from dash import html
import interface.interface_callback
dash.register_page(__name__)


layout = html.Div([
    html.Div(html.H5("Reserve Conditions Indicators"), className="row"),
    html.Div(children=[interface.interface_callback.iorb_effr_panel()], className="row"),
    #html.Div(children=[interface.interface_callback.iorb_tgcr_panel()], className="row"),
    html.Div(children=[interface.interface_callback.elasticity_panel()], className="row"),
    html.Div(children=[interface.interface_callback.overdraft_panel(is_average=True)], className="row"),
    html.Div(children=[interface.interface_callback.overdraft_panel(is_average=False)], className="row"),
    html.Div(children=[interface.interface_callback.fedfund_panel()], className="row")
], className="row")
