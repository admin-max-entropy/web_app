"""home layout"""
import dash
from dash import html
import pages.config
dash.register_page(__name__, order=2)

layout = html.Div([
    html.Div(html.H5("U.S. Overnight Funding Market"), className="row"),
    html.Div(id=pages.config.APP_ID_TGCR_IORB, children=[], className="row"),
    html.Div(id = pages.config.APP_ID_SOFR_IORB, className="row"),
    html.Div(id = pages.config.APP_ID_BGCR_IORB, className="row"),
    html.Div(id=pages.config.APP_ID_EFFR_IORB, className="row"),
    html.Div(id=pages.config.APP_ID_OBFR_IORB, className="row"),
    html.Div(id=pages.config.APP_ID_REPO_VOLUME, className="row"),
    html.Div(id=pages.config.APP_ID_UNSECURED_VOLUME, className="row"),
], className="row")
#mysql.connector.errors.ProgrammingError: 2055: Cursor is not connected