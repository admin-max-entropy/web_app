
"""home layout"""
import dash
from dash import html, Output, callback, Input
import dash_mantine_components as dmc
import pages.config
from interface import interface_utils

dash.register_page(__name__)

layout =  dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
    },
    children=[
    html.Div(
    [
    html.Div(html.H5("Central Bank Information Feeds"), className="row"),

    html.Div(children=[
        html.Div(html.H6("Speeches"), className="row"),

    html.Div(
    [
        dmc.MultiSelect(
            id=pages.config.APP_ID_SPEECHES,
            value=list(map(lambda x: x["value"],
                           interface_utils.fed_rss_tags(interface_utils.fed_central_bankers()))),
            data=interface_utils.fed_rss_tags(interface_utils.fed_central_bankers()),
            searchable=True,
            persistence=True,
            persistence_type="local"
        ),
    ], className="row", style={"paddingBottom": "10px"}),

        html.Div(children=[], id=pages.config.APP_ID_SPEECH_CARDS, className="row")],

        className="four columns", style={"paddingLeft": "0px"}),

    html.Div(children=[
        html.Div(html.H6("Policy Updates"), className="row"),
        html.Div(
            [
                dmc.MultiSelect(
                    id=pages.config.APP_ID_POLICY,
                    value=list(map(lambda x: x["value"], interface_utils.fed_rss_tags(interface_utils.fed_cb_policy()))),
                    data=interface_utils.fed_rss_tags(interface_utils.fed_cb_policy()),
                    searchable=True,
                    persistence=True,
                    persistence_type="local"
                ),
            ], className="row", style={"paddingBottom": "10px"}),

        html.Div(id=pages.config.APP_ID_POLICY_CARDS, className="row")],
        className="four columns", style={"paddingLeft": "0px"}),

    html.Div(children=[
        html.Div(html.H6("Researches"), className="row"),
        html.Div(
            [
                dmc.MultiSelect(
                    id=pages.config.APP_ID_RESEARCH,
                    value=list(
                        map(lambda x: x["value"], interface_utils.fed_rss_tags(interface_utils.fed_research_feeds()))),
                    data=interface_utils.fed_rss_tags(interface_utils.fed_research_feeds()),
                    searchable=True,
                    persistence=True,
                    persistence_type="local"
                ),
            ], className="row", style={"paddingBottom": "10px"}),

        html.Div(id=pages.config.APP_ID_RESEARCH_CARDS, className="row")],
        className="four columns", style={"paddingLeft": "0px"}),

], className="row")])
