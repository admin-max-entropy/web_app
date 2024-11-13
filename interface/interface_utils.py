"""interface utils"""
from datetime import datetime, timedelta
import pytz
import bs4
import pages.config
import src.liquidity_monitor
import plotly.graph_objects as go
from src import config as src_config
from interface import config as interface_config
import feedparser
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
import functools
import src.data_utils


@functools.lru_cache(maxsize=None)
def __get_speech_data():
    ai_collection = src.data_utils.fed_speech_collection()
    result = {}
    for document in ai_collection.find():
        author = document["author"]
        if author not in result:
            result[author] = []
        result[author].append(document)
    return result

@functools.lru_cache()
def __get_speech_summary():
    ai_collection = src.data_utils.fed_speech_structured_output()
    result = {}
    for document in ai_collection.find():
        url = document["url"]
        result[url] = document
    return result

def get_speeches(values, tags_input):

    cutoff = 15
    names_map = fed_central_bankers()
    images = fed_cb_images()
    links = {}
    ai_collection = __get_speech_data()
    ai_summary = __get_speech_summary()

    for name, _ in names_map.items():

        if name not in values:
            continue

        content = ai_collection[name]
        content = sorted(content, key=lambda x: x['date'], reverse=False)
        content = content[-cutoff:] if len(content) > cutoff else content

        for entry in content:

            url = entry["url"]
            ai_summary_ = ai_summary[url]["views"]
            summary_list = []
            tags = []
            for key in ai_summary_:
                text_list =  dmc.ListItem([dmc.Text([f"{reformat_key(key)}: "],
                                                      size="sm",
                                                      c="white"),
                                           dmc.Text([f"{ai_summary_[key]}"],
                                                                   size="sm",
                                                                   c="dimmed")])

                if len(ai_summary_[key]) > 1:
                    if tags_input is None or len(tags_input) == 0:# sometimes it returns "."
                        summary_list +=[text_list]
                    else:
                        low_tags = list(map(lambda x: x.lower(), tags_input))
                        format_key_ = reformat_key(key)
                        if format_key_.lower() in low_tags:
                            summary_list += [text_list]
                    tags += [key]
            chips = list(map(lambda x: dmc.Badge(x.replace("_", " "),
                                                 size="xs", color=color_map_labels()[x],
                                                 variant="filled"),
                             tags))
            card = dmc.TimelineItem(title= entry["date"].strftime("%a, %d %b %Y %H:%M"),

            children=[
                html.Div(children=[dmc.Group(
                    [
                        dmc.Avatar(src=images[name],
                                   color="cyan", radius="xl", size="sm"),
                        dmc.Text(entry["title"], fw=500),
                    ],
                    mt="md",
                    mb="xs",
                ),
                html.Div(dmc.Text(
                    entry["description"], #interface_utils.get_text_content(entry),
                    size="sm",
                    c="dimmed",
                ),style=({"display": "none"} if (tags_input is not None and len(tags_input)>0)
                else {})
                ),
                html.Div(
                    children=[
                html.Div(dmc.Anchor(
                    dmc.Button(
                    "",
                    variant="subtle",
                    leftIcon=DashIconify(icon="flat-color-icons:link", width=20),
                    color="blue",
                    size="sm",
                ), href=entry["url"], target="_blank"), className="two columns"),
                        html.Div(dmc.HoverCard(
                            withArrow=True,
                            width="100%",
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
                    ], className="row", style=({"display": "none"} if (tags_input is not None and len(tags_input)>0)
                else {})),
                html.Div(dmc.ChipGroup(chips), className="row", style=({"display": "none"} if (tags_input is not None and len(tags_input)>0)
                else {})),
                    html.Div(dmc.List(summary_list), className="eleven half columns", style={"paddingTop":"10px"})
                ],
                className="row"),
            ], className="row"
        )
            if tags_input is not  None and len(tags_input) != 0 and len(summary_list) == 0:
                continue
            if entry["date"] not in links:
                links[entry["date"]] = []
            links[entry["date"]] += [card]

    links = dict(sorted(links.items(), key=lambda x: x[0], reverse=True))
    final_items = []
    for date in links:
        final_items += links[date]
    return dmc.Timeline(children=final_items)


def get_policy_updates(values):

    names_map = fed_cb_policy()
    color_map = fed_cb_policy_color()
    links = {}

    for name, url in names_map.items():

        if name not in values:
            continue

        feed = feedparser.parse(url)

        for entry in feed.entries:

            date_eastern = convert_fed_rss_time(entry.published)
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

def get_researches(values):

    names_map = fed_research_feeds()
    color_map = fed_research_color()

    links = {}

    for name, url in names_map.items():

        if name not in values:
            continue

        feed = feedparser.parse(url)

        for entry in feed.entries:

            date_eastern = convert_fed_rss_time(entry.published)
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
                    get_text_content(entry),
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

def iorb_figure():
    start_date = src_config.TS_START_DATE
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, src_config.TABLE_RRP_VOLUME)
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
    figure = format_figure(figure)
    return figure

def tga_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def fedfund_figure():
    start_date = src_config.TS_START_DATE
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def reserve_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def __foreign_rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, src_config.TABLE_FOREIGN_RRP)
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
    figure = format_figure(figure)
    return figure

def __rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, src_config.TABLE_RRP_VOLUME)
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
    figure = format_figure(figure)
    return figure

def __tga_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def __fedfund_figure():
    start_date = src_config.TS_START_DATE
    end_date = get_end_date()
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
    figure = format_figure(figure)
    return figure

def __repo_volume_color_map():
    color_map = {"sofr": interface_config.LINE_COLOR,
                 "tgcr": "#FF6347",
                 "bgcr": "#3CB371",
                 "effr": "#ad0034",
                 "obfr": "#FFFF99"}
    return color_map


def __color_map():
    color_map = {"": "#ad0034", " 1%": "#4BAAC8", " 99%": "#4BAAC8",
                 " 25%": "#C0C0C0", " 75%": "#C0C0C0"}
    return color_map

def rate_to_iorb_figure(key_input):
    end_date = get_end_date()
    start_date = src_config.TS_START_DATE_L
    cap = 80
    floor = -20
    time_series_set = src.liquidity_monitor.iorb_key_spread(start_date,
                                                            end_date, key_input, cap, floor)
    figure = go.Figure()

    last_date = None
    time_series = None

    for key, time_series in time_series_set.items():
        color_key = __color_map()[rename_key(key).replace(key_input.upper(), "")]
        figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                    text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                                  list(time_series.keys()))),
                                    hovertemplate=
                                    '%{y:.0f} bps <br>' +
                                    '%{text}',
                                    line={'color': color_key,
                                          'width': interface_config.LINE_WIDTH},
                                    name=rename_key(key)))
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
    figure = format_figure(figure)
    return figure


def secured_repo_volume_figure(is_repo):

    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
    time_series_set =  src.liquidity_monitor.repo_volume_ts(start_date, end_date, is_repo=is_repo)

    figure = go.Figure()

    for key, time_series in time_series_set.items():
        figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"),
                                              list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.2f} BN($) <br>' +
                                '%{text}',
                                line={'color': __repo_volume_color_map()[key],
                                      'width': interface_config.LINE_WIDTH},
                                name=key.upper(), showlegend=True))
    last_date = end_date
    figure.update_layout(title="Volume of Transactions underlying Secured rates based on O/N Repo backed by Treasury securities"
    if is_repo else "Volume of Transactions underlying Unsecured rates")
    figure.update_yaxes(title_text="Billion ($)")
    __add_qt_regime(figure, start_date, last_date, add_regime=True, cap=None, floor=None)
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure = format_figure(figure)
    return figure

def elasticity_figure():
    start_date = src_config.TS_START_DATE
    data_set = src.liquidity_monitor.get_elasticity_data(start_date)
    color_map = {"50th": "#ad0034", "2.5th": "#4BAAC8", "97.5th": "#4BAAC8",
                 "16th": "#C0C0C0", "84th": "#C0C0C0"}
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
    figure = format_figure(figure)
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

def theme_colors():
    return {
        "light0": ["#003747"] * 10,
        "light1": ["#065465"] * 10,
        "light2": ["#06768d"] * 10,
        "light3": ["#4B9CAC"] * 10,
        "light4": ["#008080"] * 10,
        "light5": ["#cf9bc7"] * 10,
        "light6": ["#aa519c"] * 10,
        "light7": ["#bb73af"] * 10,
        "light8": ["#6D8D96"] * 10,
        "light9": ["#c249af"] * 10,
    }


def reformat_key(key):
    key = key.replace("_", " ")
    key = key.title()
    return key

def overdraft_figure(is_average):
    color_map = {"Total": "#ad0034", "Collateralized": "#4BAAC8", "Funds":  "#C0C0C0",
                 "Book Entry": "#7FFFD4"}
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
    figure = format_figure(figure)
    return figure

def color_map_labels():
    tmp = {"inflation": "light0",
           "labor_market": "light1",
           "economic_growth": "light2",
           "monetary_policy": "light4",
           "balance_sheet": "light5",
           "r_star": "light6",
           "banking_regulation": "light7",
           "policy_rate": "light9"}
    return tmp

def tags_chips():
    custom_css = """
    .mantine-Chip-input:checked + .mantine-Chip-label::after {
        content: '•'; /* Unicode dot character */
        font-size: 20px;
        color: black;
        display: inline-block;
        margin-left: 8px;
        position: relative;
        top: -1px;
    }
    """
    result = []
    for key, color in color_map_labels().items():
        key_ = key.replace("_", " ")
        key_ = key_.title()
        styles = {
            "label": {
                "&[data-checked]": {
                    "&, &:hover": {
                        "backgroundColor": theme_colors()[color][5],
                        "color": "white",
                        'borderColor': theme_colors()[color][4],
                    },
                },
            },
        }
        result += [dmc.Chip(key_, value=key_, styles=styles, size="xs", style={"checkIcon": None})]
    return result

def rename_key(key):
    """
    :param key:
    :return: renamed key for data from OFR
    """
    key = key.replace("FNYR", "")
    key = key.replace("Pctl", "%")
    key = key.replace("_", " ")
    if key.endswith("A"):
        key = key[:-1]
    return key

def format_figure(figure, show_x_range=False):
    """
    :param figure:
    :return: formatted figure
    """
    figure = figure.update_layout(
        {
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(showgrid=False, zeroline=False)
    figure.update_layout(font={'color': "#E0E0E0"},
                         margin={'l': 60, 'r': 20, "t": 50,'b': 40}, title_x=0)
    figure.update_layout(height=297)
    if show_x_range:
        figure.update_layout(xaxis={'rangeslider': {'visible': True}})
    return figure

def get_end_date():
    """
    :return: return data in EST
    """
    current_time = datetime.now()
    current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    if current_time <= current_time.replace(hour=6):
        return current_time + timedelta(days=-1)
    return current_time

def fed_rss_tags(names_map):
    """
    :param names_map:
    :return:
    """
    data = []
    for key in names_map:
        data.append({'value': key, 'label': key})
    return data

def fed_central_bankers():
    """
    :return:
    """
    names_map = {pages.config.JPOW:
                     "https://www.federalreserve.gov/feeds/s_t_powell.xml",
                 pages.config.MBARR:
                     "https://www.federalreserve.gov/feeds/s_t_barr.xml",
                 pages.config.CWALLER:
                     "https://www.federalreserve.gov/feeds/s_t_waller.xml",
                 pages.config.PJEFF:
                     "https://www.federalreserve.gov/feeds/s_t_jefferson.xml",
                 pages.config.MBOW:
                     "https://www.federalreserve.gov/feeds/m_w_Bowman.xml",
                 pages.config.AKUGLER:
                     "https://www.federalreserve.gov/feeds/s_t_kugler.xml",
                 pages.config.LCOOK:
                     "https://www.federalreserve.gov/feeds/s_t_cook.xml",
                 pages.config.LOGAN:
                     "https://www.dallasfed.org/rss/speeches.xml",
                 pages.config.JWILLAIM: "",
                 pages.config.RBOSTIC: "",
                 pages.config.MDALY: "",
                 pages.config.TBARKIN: ""
                 }
    return names_map

def get_text_content(entry):
    """
    :param entry:
    :return:
    """
    soup = bs4.BeautifulSoup(entry.summary, features="html.parser")
    text = ""
    for tag in soup.find_all("br"):
        for row in tag.next_siblings:
            text += row.get_text()
        return text


def fed_cb_images():
    """
    :return:
    """
    names_map = {pages.config.JPOW:
                     "https://www.federalreservehistory.org/-/media/images/powell_jerome.jpg",
                 pages.config.MBARR:
                     "https://www.federalreservehistory.org/-/media/images/Barr_Michael.jpg",
                 pages.config.CWALLER:
                     "https://www.federalreservehistory.org/-/media/images/waller_christopher.jpg",
                 pages.config.PJEFF:
                     "https://www.federalreservehistory.org/-/media/images/Jefferson_Phillip.jpg",
                 pages.config.MBOW:
                     "https://www.federalreservehistory.org/-/media/images/bowman_michelle.jpg",
                 pages.config.AKUGLER:
                     "https://www.federalreservehistory.org/-/media/images/Kugler_Adriana.jpg",
                 pages.config.LCOOK:
                     "https://www.federalreservehistory.org/-/media/images/Cook_Lisa.jpg",
                 pages.config.LOGAN:
                     "https://www.federalreservehistory.org/-/media/images/Logan_Lorie.jpg",
                 pages.config.JWILLAIM:
                     "https://www.federalreservehistory.org/-/media/images/williams_john_c.jpg",
                 pages.config.RBOSTIC:
                     "https://www.federalreservehistory.org/-/media/images/bostic_raphael.jpg",
                 pages.config.MDALY:
                     "https://www.federalreservehistory.org/-/media/images/daly-mary-2022.jpg",
                 pages.config.TBARKIN:
                     "https://www.federalreservehistory.org/-/media/images/barkin-tom.jpg"
                 }
    return names_map


def fed_research_feeds():
    """
    :return:
    """
    names_map = {pages.config.FEDS_NOTES:
                     "https://www.federalreserve.gov/feeds/feds_notes.xml",
                 pages.config.FINANCE_AND_ECONOMICS_DISCUSSION:
                     "https://www.federalreserve.gov/feeds/feds.xml",
                 pages.config.FRB_WORKING_PAPER:
                     "https://www.federalreserve.gov/feeds/working_papers.xml"
                 }
    return names_map

def fed_research_color():
    """
    :return:
    """
    names_map = {pages.config.FEDS_NOTES: "cyan",
                 pages.config.FINANCE_AND_ECONOMICS_DISCUSSION: "pink",
                 pages.config.FRB_WORKING_PAPER: "blue"
                 }
    return names_map

def fed_cb_policy():
    """
    :return:
    """
    names_map = {pages.config.MONETARY_POLICY:
                     "https://federalreserve.gov/feeds/press_monetary.xml",
                 pages.config.BANKING_REGULATION:
                     "https://www.federalreserve.gov/feeds/press_bcreg.xml"
                 }
    return names_map

def fed_cb_policy_color():
    """
    :return:
    """
    names_map = {pages.config.MONETARY_POLICY: "teal",
                 pages.config.BANKING_REGULATION: "pink"
                 }
    return names_map


def convert_fed_rss_time(input_time):
    """
    :param input_time:
    :return:
    """
    if "GMT" in input_time:
        tz_name = 'GMT'
        tz = pytz.timezone(tz_name)
    elif "CST" in input_time:
        tz_name = "CST"
        tz = pytz.timezone("US/Central")
    else:
        raise RuntimeError("unsupported time format")

    eastern = pytz.timezone('US/Eastern')
    date = datetime.strptime(input_time, f"%a, %d %b %Y %H:%M:%S {tz_name}")
    date_tz = tz.localize(date)
    date_eastern = date_tz.astimezone(eastern)
    return date_eastern

def foreign_rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = get_end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date, src_config.TABLE_FOREIGN_RRP)
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
    figure = format_figure(figure)
    return figure
