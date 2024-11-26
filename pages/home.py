"""home layout"""
import dash
from dash import html
dash.register_page(__name__, path="/",
    title = "Max Entropy",
    image = "logo.png",
    description='Financial Indicators & AI Insights on Central Bank Speeches',
    order=1
)

layout = html.Div([
], className="row")
