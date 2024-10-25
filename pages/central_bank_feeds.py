
"""home layout"""
from datetime import datetime

import dash
from dash import html
import dash_mantine_components as dmc
import feedparser
from dash_iconify import DashIconify
import pytz

gmt = pytz.timezone('GMT')
eastern = pytz.timezone('US/Eastern')

dash.register_page(__name__)

def __convert_time(input_time):
    date = datetime.strptime(input_time, "%a, %d %b %Y %H:%M:%S GMT")
    date_gmt = gmt.localize(date)
    date_eastern = date_gmt.astimezone(eastern)
    return date_eastern

def __get_policy_updates():

    names_map = dict(MP="https://www.federalreserve.gov/feeds/press_monetary.xml")
    links = {}

    for name, url in names_map.items():

        feed = feedparser.parse(url)

        for entry in feed.entries:
            date_eastern = __convert_time(entry.published)
            card = dmc.TimelineItem(title=date_eastern.strftime("%a, %d %b %Y %H:%M"),
                                    children=[
                                        dmc.Group(
                                            [
                                                dmc.Avatar(name, color="cyan", radius="xl", size="sm"),
                                                dmc.Text(entry.title, fw=500),
                                            ],
                                            mt="md",
                                            mb="xs",
                                        ),
                                        dmc.Text(
                                            entry.description,
                                            size="sm",
                                            c="dimmed",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(dmc.Anchor(
                                                    dmc.Button(
                                                        "",
                                                        variant="subtle",
                                                        leftIcon=DashIconify(icon="flat-color-icons:link", width=20),
                                                        color="blue",
                                                        size="sm", fullWidth=True,
                                                    ), href=entry.link, target="_blank"), className="two columns")],
                                            className="row"),
                                    ],
                                    w=700,
                                    )
            links[date_eastern] = card

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))


def __get_researches():

    names_map = dict(JP="https://www.federalreserve.gov/feeds/feds_notes.xml",
                     LC="https://www.federalreserve.gov/feeds/feds.xml",
                     CW="https://www.federalreserve.gov/feeds/working_papers.xml")
    links = {}

    for name, url in names_map.items():

        feed = feedparser.parse(url)

        for entry in feed.entries:
            date_eastern = __convert_time(entry.published)
            card = dmc.TimelineItem(title= date_eastern.strftime("%a, %d %b %Y %H:%M"),

            children=[
                dmc.Group(
                    [
                        dmc.Avatar(name, color="cyan", radius="xl", size="sm"),
                        dmc.Text(entry.title, fw=500),
                    ],
                    mt="md",
                    mb="xs",
                ),
                dmc.Text(
                    entry.description,
                    size="sm",
                    c="dimmed",
                ),
                html.Div(
                    children=[
                html.Div(dmc.Anchor(
                    dmc.Button(
                    "",
                    variant="subtle",
                    leftIcon=DashIconify(icon="flat-color-icons:link", width=20),
                    color="blue",
                    size="sm", fullWidth=True,
                ), href=entry.link, target="_blank"), className="two columns")], className="row"),
            ],
            w=700,
        )
            links[date_eastern] = card

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))


def __get_speeches():
    names_map = dict(JP="https://www.federalreserve.gov/feeds/s_t_powell.xml",
                     MSB="https://www.federalreserve.gov/feeds/s_t_barr.xml",
                     CW="https://www.federalreserve.gov/feeds/s_t_waller.xml",
                     PJ="https://www.federalreserve.gov/feeds/s_t_jefferson.xml",
                     MWB="https://www.federalreserve.gov/feeds/m_w_Bowman.xml",
                     LC="https://www.federalreserve.gov/feeds/m_w_Bowman.xml",
                     AK="https://www.federalreserve.gov/feeds/s_t_kugler.xml"
                     )
    links = {}

    for name, url in names_map.items():

        feed = feedparser.parse(url)

        for entry in feed.entries:
            date_eastern = __convert_time(entry.published)
            card = dmc.TimelineItem(title= date_eastern.strftime("%a, %d %b %Y %H:%M"),

            children=[
                dmc.Group(
                    [
                        dmc.Avatar(name, color="cyan", radius="xl", size="sm"),
                        dmc.Text(entry.title, fw=500),
                    ],
                    mt="md",
                    mb="xs",
                ),
                dmc.Text(
                    entry.description,
                    size="sm",
                    c="dimmed",
                ),
                html.Div(
                    children=[
                html.Div(dmc.Anchor(
                    dmc.Button(
                    "",
                    variant="subtle",
                    leftIcon=DashIconify(icon="flat-color-icons:link", width=20),
                    color="blue",
                    size="sm", fullWidth=True,
                ), href=entry.link, target="_blank"), className="two columns")], className="row"),
            ],
            w=700,
        )
            links[date_eastern] = card

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))

layout = html.Div(
    [

    html.Div(html.H5("Central Bank Information Feeds"), className="row"),

    html.Div(children=[
        html.Div(html.H6("Speeches"), className="row"),
        html.Div(__get_speeches(), className="row")],
        className="four columns", style={"paddingLeft": "0px"}),

    html.Div(children=[
        html.Div(html.H6("Policy Updates"), className="row"),
        html.Div(__get_policy_updates(), className="row")],
        className="four columns", style={"paddingLeft": "0px"}),

    html.Div(children=[
        html.Div(html.H6("Researches"), className="row"),
        html.Div(__get_researches(), className="row")],
        className="four columns", style={"paddingLeft": "0px"}),

], className="row")
