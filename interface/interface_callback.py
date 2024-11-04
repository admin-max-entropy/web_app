"""callback functions"""

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc, Output, callback, Input
import feedparser
from dash_iconify import DashIconify
import interface.config as interface_config
import src.liquidity_monitor
import src.data_utils
from src import config as src_config
from interface import interface_utils
from interface.interface_utils import fed_cb_policy, fed_research_feeds, fed_research_color
import pages.config

def __get_researches(values):

    names_map = fed_research_feeds()
    color_map = fed_research_color()

    links = {}

    for name, url in names_map.items():

        if name not in values:
            continue

        feed = feedparser.parse(url)

        for entry in feed.entries:

            date_eastern = interface_utils.convert_fed_rss_time(entry.published)
            card = dmc.TimelineItem(title= date_eastern.strftime("%a, %d %b %Y %H:%M"),
            children=[
                dmc.Group(
                    [
                        dmc.Badge(name, color=color_map[name], radius="xl", size="sm"),
                        dmc.Text(entry.title, fw=500),
                    ],
                    mt="md",
                    mb="xs",
                ),
                dmc.Text(
                    interface_utils.get_text_content(entry),
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
        )
            links[date_eastern] = card

        links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))


def __get_policy_updates(values):

    names_map = fed_cb_policy()
    color_map = interface_utils.fed_cb_policy_color()
    links = {}

    for name, url in names_map.items():

        if name not in values:
            continue

        feed = feedparser.parse(url)

        for entry in feed.entries:

            date_eastern = interface_utils.convert_fed_rss_time(entry.published)
            card = dmc.TimelineItem(title=date_eastern.strftime("%a, %d %b %Y %H:%M"),
                                    children=[
                                        dmc.Group(
                                            [
                                                dmc.Badge(name, color=color_map[name],
                                                          radius="xl", size="sm",
                                                         variant="filled"),
                                                dmc.Text(entry.title, fw=500),
                                            ],
                                            mt="md",
                                            mb="xs",
                                        ),
                                        # dmc.Text(
                                        #     entry.description,
                                        #     size="sm",
                                        #     c="dimmed",
                                        # ),
                                        html.Div(
                                            children=[
                                                html.Div(dmc.Anchor(
                                                    dmc.Button(
                                                        "",
                                                        variant="subtle",
                                                        leftIcon=
                                                        DashIconify(icon="flat-color-icons:link",
                                                                    width=20),
                                                        color="blue",
                                                        size="sm", fullWidth=True,
                                                    ), href=entry.link, target="_blank"),
                                                    className="two columns")],
                                            className="row"),
                                    ],
                                    )
            links[date_eastern] = card

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))

def __get_speeches(values):

    names_map = interface_utils.fed_central_bankers()
    images = interface_utils.fed_cb_images()
    links = {}
    ai_collection = src.data_utils.fed_speech_collection()

    for name, _ in names_map.items():

        if name not in values:
            continue

        content = ai_collection.find({'author': name})

        for entry in content:

            card = dmc.TimelineItem(title= entry["date"].strftime("%a, %d %b %Y %H:%M"),

            children=[
                dmc.Group(
                    [
                        dmc.Avatar(src=images[name],
                                   color="cyan", radius="xl", size="sm"),
                        dmc.Text(entry["title"], fw=500),
                    ],
                    mt="md",
                    mb="xs",
                ),
                dmc.Text(
                    entry["description"], #interface_utils.get_text_content(entry),
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
                ), href=entry["url"], target="_blank"), className="two columns"),
                        html.Div(dmc.HoverCard(
                            withArrow=True,
                            width=500,
                            shadow="md",
                            children=[
                                dmc.HoverCardTarget(dmc.Button("",
                                                               leftIcon=
                                                               DashIconify(icon="ri:openai-fill",
                                                                           width=20,
                                                                           color="teal"),
                                                               color="teal",
                                                               size="sm",
                                                               variant="subtle",
                                                               )),
                                dmc.HoverCardDropdown(
                                    dmc.Text(
                                        entry["summary"],
                                        size="sm",
                                    )
                                ),
                            ],
                        ), className="two columns"),
                    ], className="row"),
            ],
        )
            links[entry["date"]] = card

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    return dmc.Timeline(children=list(links.values()))

@callback(
    Output(component_id=pages.config.APP_ID_SPEECH_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_SPEECHES, component_property='value')
)
def update_output_speech(input_value):
    """
    :param input_value:
    :return:
    """
    return __get_speeches(input_value)

@callback(
    Output(component_id=pages.config.APP_ID_POLICY_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_POLICY, component_property='value')
)
def update_output_policy(input_value):
    """
    :param input_value:
    :return:
    """
    return __get_policy_updates(input_value)

@callback(
    Output(component_id=pages.config.APP_ID_RESEARCH_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_RESEARCH, component_property='value')
)
def update_output_div(input_value):
    """
    :param input_value:
    :return:
    """
    return __get_researches(input_value)

def __overdraft_figure(is_average):
    color_map = {"Total": "#ad0034", "Collateralized": "#4BAAC8", "Funds":  "#C0C0C0",
                 "Book-Entry": "#7FFFD4"}
    data_set = src.liquidity_monitor.daylight_overdraft(is_average)
    figure = go.Figure()
    end_date = None
    start_date = None
    ts_tmp = None
    for key, ts in data_set.items():
        figure.add_trace(go.Scatter(x=list(ts.keys()), y=list(ts.values()), name=key,
                                    line={'color': color_map[key], 'width': 1.2},
                                    text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                                  list(ts.keys()))),
                                    hovertemplate=
                                    '%{y:.0f} Million ($) <br>' +
                                    '%{text}',
                                    ))
        end_date = list(ts.keys())[-1]
        start_date = list(ts.keys())[0]
        ts_tmp = ts

    __add_qt_regime(figure, start_date, end_date)
    figure.update_yaxes(title_text="Million ($)")
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure.add_trace(go.Scatter(x=list(ts_tmp.keys()), y=len(list(ts_tmp.values())) * [0],
                                line={'color': "grey", 'width': 0.5}, showlegend=False, name=""))
    figure.update_layout(title=f"Intraday {'Peak' if not is_average else 'Average'} "
                               f"Overdrafts of Deposit Institutions")
    figure = interface_utils.format_figure(figure)
    return figure

def __elasticity_figure():
    start_date = src_config.TS_START_DATE
    data_set = src.liquidity_monitor.get_elasticity_data(start_date)
    color_map = {"50th % (main)": "#ad0034", "2.5th %": "#4BAAC8", "97.5th %": "#4BAAC8",
                 "16th %": "#C0C0C0", "84th %": "#C0C0C0"}
    figure = go.Figure()
    end_date = None
    ts_tmp = None
    for key, ts in data_set.items():
        figure.add_trace(go.Scatter(x=list(ts.keys()), y=list(ts.values()), name=key,
                                    line={'color': color_map[key], 'width': 1.2},
                                    text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                                  list(ts.keys()))),
                                    hovertemplate=
                                    '%{y:.3f} bps/% <br>' +
                                    '%{text}',
                                    ))
        end_date = list(ts.keys())[-1]
        ts_tmp = ts

    __add_qt_regime(figure, start_date, end_date)
    figure.update_yaxes(title_text="Bps/%")
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure.add_trace(go.Scatter(x=list(ts_tmp.keys()), y=len(list(ts_tmp.values())) * [0],
                                line={'color': "grey", 'width': 0.5}, showlegend=False, name=""))
    figure.update_layout(title="Reserve Demand Elasticity")
    figure = interface_utils.format_figure(figure)
    return figure


def __add_qt_regime(figure, start_date, end_date, add_regime=True, cap=None, floor=None):
    if add_regime:
        figure.add_vrect(x0=max(start_date, src_config.PREV_QT_START), x1=src_config.PREV_QT_END,
                         annotation_text=f"QT: {src_config.PREV_QT_START.strftime('%Y.%m.%d')}"
                                         f" - {src_config.PREV_QT_END.strftime('%Y.%m.%d')}",
                         annotation_position="top left",
                         fillcolor="#536878", opacity=0.25, line_width=0)

        ed_str = src_config.QT_END.strftime('%Y.%m.%d') \
            if src_config.QT_END is not None else 'Present'
        figure.add_vrect(x0=src_config.QT_START, x1=src_config.QT_END
        if src_config.QT_END is not None else end_date,
                         annotation_text=f"QT: {src_config.QT_START.strftime('%Y.%m.%d')}"
                                         f" - {ed_str}",
                         annotation_position="top left",
                         fillcolor="#536878", opacity=0.25, line_width=0)
    note = f'Last Update: {end_date.strftime("%Y.%m.%d")}'
    if cap is not None and floor is not None:
        note += f". Spread is capped at {cap} bps and floored at {floor} bps."

    figure.add_annotation(
        showarrow=False,
        text=note,
        font={'size': 10},
        xref='x domain',
        x=0,
        yref='y domain',
        y=-0.2
    )
    return figure

def __color_map():
    color_map = {"": "#ad0034", " 1%": "#4BAAC8", " 99%": "#4BAAC8",
                 " 25%": "#C0C0C0", " 75%": "#C0C0C0"}
    return color_map

def __repo_volum_color_map():
    color_map = {"sofr": interface_config.LINE_COLOR,
                 "tgcr": "#FF6347",
                 "bgcr": "#3CB371",
                 "effr": "#ad0034",
                 "obfr": "#FFFF99"}

    return color_map

def __secured_repo_volume_figure(is_repo):

    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date().replace(tzinfo=None)
    time_series_set =  src.liquidity_monitor.repo_volume_ts(start_date, end_date, is_repo=is_repo)

    figure = go.Figure()

    for key, time_series in time_series_set.items():
        figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.2f} BN($) <br>' +
                                '%{text}',
                                line={'color': __repo_volum_color_map()[key],
                                      'width': interface_config.LINE_WIDTH},
                                name=key.upper(), showlegend=True))
    last_date = end_date
    figure.update_layout(title="Repo Market Volumes" if is_repo else "Unsecured Volumes")
    figure.update_yaxes(title_text="Billion ($)")
    __add_qt_regime(figure, start_date, last_date, add_regime=True, cap=None, floor=None)
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure = interface_utils.format_figure(figure)
    return figure

def __rate_to_iorb_figure(key_input):
    end_date = interface_utils.end_date()
    start_date = src_config.TS_START_DATE_L
    cap = 80
    floor = -20
    if key_input == "tgcr":
        time_series_set = src.liquidity_monitor.iorb_tgcr_spread(start_date, end_date, cap, floor)
    elif key_input == "sofr":
        time_series_set = src.liquidity_monitor.iorb_sofr_spread(start_date, end_date, cap, floor)
    elif key_input == "bgcr":
        time_series_set = src.liquidity_monitor.iorb_bgcr_spread(start_date, end_date, cap, floor)
    elif key_input == "effr":
        time_series_set = src.liquidity_monitor.iorb_fedfund_spread(start_date,
                                                                    end_date, cap, floor)
    elif key_input == "obfr":
        time_series_set = src.liquidity_monitor.iorb_obfr_spread(start_date, end_date, cap, floor)

    else:
        raise RuntimeError("unsupported key"
                           )
    figure = go.Figure()

    last_date = None
    time_series = None

    for key, time_series in time_series_set.items():
        color_key = __color_map()[interface_utils.rename_key(key).replace(key_input.upper(), "")]
        figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                    text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                                  list(time_series.keys()))),
                                    hovertemplate=
                                    '%{y:.0f} bps <br>' +
                                    '%{text}',
                                    line={'color': color_key,
                                          'width': interface_config.LINE_WIDTH},
                                    name=interface_utils.rename_key(key)))
        last_date = list(time_series.keys())[-1]

    rrp_spread = src.liquidity_monitor.iorb_rrp_spread(start_date, end_date)
    upper_spread = src.liquidity_monitor.iorb_upper_spread(start_date, end_date)
    lower_spread = src.liquidity_monitor.iorb_lower_spread(start_date, end_date)

    figure.add_trace(go.Scatter(x=list(lower_spread.keys()), y=list(lower_spread.values()),
                                line={'color': "#00A86B", 'width': 0.8, "dash": "dot"},
                                name="LB"))
    figure.add_trace(go.Scatter(x=list(rrp_spread.keys()), y=list(rrp_spread.values()),
                                line={'color': "#FF7F50", 'width': 0.8, "dash": "dot"},
                                name="RRP"))
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=len(list(time_series.values())) * [0],
                                line={'color': "#FF7F50", 'width': 0.8, "dash": "dot"},
                                name="IORB"))
    figure.add_trace(go.Scatter(x=list(upper_spread.keys()), y=list(upper_spread.values()),
                                line={'color': "#00A86B", 'width': 0.8, "dash": "dot"},
                                name="UB"))
    figure.add_trace(go.Scatter(x=list(time_series.keys()),
                                y=len(list(time_series.values())) * [cap],
                                line={'color': "grey", 'width': 0.3},
                                showlegend=False, name=""))
    figure.add_trace(go.Scatter(x=list(time_series.keys()),
                                y=len(list(time_series.values())) * [floor],
                                line={'color': "grey", 'width': 0.3},
                                showlegend=False, name=""))
    figure.update_layout(title=f"{key_input.upper()}-IORB Spread")
    figure.update_yaxes(title_text="Bps")
    __add_qt_regime(figure, start_date, last_date, add_regime=True, cap=cap, floor=floor)
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure = interface_utils.format_figure(figure)
    return figure


def __iorb_figure():
    start_date = src_config.TS_START_DATE
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.iorb_effr_spread(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} bps <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=len(list(time_series.values())) * [0],
                                line={'color': "grey", 'width': 0.5}, showlegend=False, name=""))
    figure.update_layout(title="EFFR-IORB Spread")
    figure.update_yaxes(title_text="Bps")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __reserve_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.reserve_balance_data(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} BN($) <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.update_layout(title="Reserve Balances with Federal Reserve Banks: Week Average")
    figure.update_yaxes(title_text="Billions of U.S. Dollars")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __foreign_rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, "WLRRAFOIAL")
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()),
                                y=list(map(lambda x: x/1e3, list(time_series.values()))),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} BN($) <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.update_layout(title="Reverse Repurchase Agreements: Foreign Official and"
                               " International Accounts: Wednesday Level")
    figure.update_yaxes(title_text="Billions of U.S. Dollars")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, "RRPONTSYD")
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} BN($) <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.update_layout(title="Overnight Reverse Repurchase Agreements")
    figure.update_yaxes(title_text="Billions of U.S. Dollars")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __tga_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.tga_balances(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} BN($) <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.update_layout(title="U.S. Treasury, General Account")
    figure.update_yaxes(title_text="Billions of U.S. Dollars")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __fedfund_figure():
    start_date = src_config.TS_START_DATE
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.fedfund_volume_decomposition(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.2f} % <br>' +
                                '%{text}',
                                line={'color': interface_config.LINE_COLOR,
                                      'width': interface_config.LINE_WIDTH},
                                name="",
                                showlegend=False))
    figure.update_layout(title="Domestic Bank Share of Federal Funds Borrowed")
    figure.update_yaxes(title_text="Percent")
    __add_qt_regime(figure, start_date, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def iorb_effr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __iorb_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * When reserves become less abundant, the cost to borrow federal funds tends to increase relative to IORB.
        * Recent references: 
            - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and 
            Understanding Repo Market Pressures, 09/24/2024](https://www.newyorkfed.org/newsevents/speeches/2024/per240926)
            - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
''',   link_target="_blank"), className="row")],
            className="four columns",
            style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def iorb_bgcr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __rate_to_iorb_figure("bgcr")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"), className="row")],
            className="four columns",
            style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def iorb_tgcr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __rate_to_iorb_figure("tgcr")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * Weather the money market rates trade below IOER is a sign of liquidity condition.
        * The tri-party general collateral rate (TGCR) are repos secured by Treasury securities.
        * Reserves and Treasury repos are both essentially risk-free overnight assets, but the reserves are more liquid.
        * The spread of IORB over TGCR indicates reserves remain in relatively excess supply compared with other liquid assets.
        * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"), className="row")],
            className="four columns",
            style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")


def volume_repo_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __secured_repo_volume_figure(is_repo=True)
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
''',   link_target="_blank"), className="row")],
            className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def volume_unsecured_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __secured_repo_volume_figure(is_repo=False)
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
''',   link_target="_blank"), className="row")],
            className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")


def iorb_sofr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __rate_to_iorb_figure("sofr")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * The secured overnight financing rate (SOFR) includes a broader set of Treasury repo transactions than TGCR.
        * Some SOFR transactions include compensation for intermediating funds from the triparty segment to cash borrowers who lack direct access to that segment.
        * Hence, the TGCR-IOER spread could be a cleaner read of on the liquidity conditions in the secured market.
        * This widening of SOFR and TGCR at month-end is resulted from the limited balance sheet availability at dealers that intermediate between the triparty and centrally cleared market segments.
         * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"),className="row")
                          ], className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def iorb_obfr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __rate_to_iorb_figure("obfr")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
         * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"),className="row")
                          ], className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def iorb_fedfund_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __rate_to_iorb_figure("effr")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
         * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"),className="row")
                          ], className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def elasticity_panel():
    """
    :return: panel for elasticity monitor
    """
    figure = __elasticity_figure()
    link = ("https://libertystreeteconomics.newyorkfed.org/2024/10/tracking-"
            "reserve-ampleness-in-real-time-using-reserve-demand-elasticity/")
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown(f'''
        * When reserves become less abundant, the elasticity of the federal funds rate to reserve changes could 
        be negative and statistically different from zero.
        * Recent references: 
            - [Gara Afonso, Domenico Giannone, Gabriele La Spada, and John C. Williams, “Tracking Reserve Ampleness 
            in Real Time Using Reserve Demand Elasticity,” Federal Reserve Bank of New York Liberty Street Economics, 
            10/17/2024]({link})
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def overdraft_panel(is_average):
    """
    :return: panel for elasticity monitor
    """
    figure = __overdraft_figure(is_average)
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown('''
        * Daylight overdrafts occur when short-term shifts in payment activity result in a temporarily negative balance in a bank’s reserve account.
        * Higher average overdrafts are an indication that reserves are harder to come by in amounts needed to facilitate payments without intraday credit from the Federal Reserve.
        * Average overdrafts are much more informative for our purposes because they abstract from idiosyncratic factors that may affect individual institutions.
        * Recent references: 
            - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"
                 ),
    ], shadow="xs", bg="black")

def fedfund_panel():
    """
    :return: panel for elasticity monitor
    """
    figure = __fedfund_figure()
    link = "https://www.newyorkfed.org/newsevents/speeches/2024/per240926/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown(f'''
        * Domestic banks tend to borrow federal funds when they need liquidity, increased activity on their part would be a sign of reserves becoming less abundant
        * Recent references: 
            - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/24/2024]({link})
            - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def rrp_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __rrp_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(
                               children=[
                                   html.Div(dmc.Badge("Liability",
                                                      variant="filled", color="yellow"),
                                            className="row"),
                               html.Div(dcc.Markdown('''
            * Currently, RRP is used as a tool to help keep the federal funds rate in the target range established by the FOMC.
            * We tend to see RRP balances increase over quarter-end, due to the banks refrain from intermediations on 
            repo trades with Money Market Funds at quarter ends.
            * Recent references: 
                - [Kansas City Fed, Rapid Declines in the Fed’s Overnight Reverse Repurchase (ON RRP) Facility May Start to Slow, 11/10/2023]({link})
    ''', link_target="_blank", ), className="row")],
                               className="four columns",
                               style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def foreign_rrp_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __foreign_rrp_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(
                               children=[
                                   html.Div(
                                       dmc.Badge("Liability",
                                                 variant="filled", color="yellow"),
                                       className="row"),
                                   html.Div(dcc.Markdown('''
            * Federal Reserve conducts overnight reverse repos with foreign official and international institutions, including foreign central banks. 
    ''', link_target="_blank", ), className="row")],
                               className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def reserve_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __reserve_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(children=[
                               html.Div(
                                   dmc.Badge("Liability",
                                             variant="filled", color="yellow"), className="row"),
                               html.Div(dcc.Markdown('''
            * More than 5,000 depository institutions maintain accounts at the Federal Reserve Banks.
            * When the Federal Reserve buys securities, either outright or via a repurchase agreement (repo), the level of deposits increases.
            * When the Federal Reserve lends, the level of deposits increases as the amount the institution borrows is credited to its Federal Reserve Accounts.
    ''', link_target="_blank", ), className="row")],
                               className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

def tga_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __tga_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(children=[
                               html.Div(dmc.Badge(
                                   "Liability",
                                   variant="filled", color="yellow"), className="row"),
                               html.Div(dcc.Markdown('''
            * Major outlays of the Treasury are paid from the Treasury's general account at the Federal Reserve.
            * A decline in the balances held in the TGA results in an increase in the deposits 
              of depository institutions, all else being equal. 
            * Conversely, funds that flow into the TGA, such as from a tax payment, 
              drain balances from the deposits of depository institutions. 
    ''', link_target="_blank", ), className="row")],
                               className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")
