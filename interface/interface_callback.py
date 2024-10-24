"""callback functions"""
import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
import interface.config as interface_config
import src.liquidity_monitor
from interface import interface_utils
from src import config as src_config


def __overdraft_figure(is_average):
    color_map = {"Total": "#DC143C", "Collateralized": "#4BAAC8", "Funds":  "#C0C0C0",
                 "Book-Entry": "#7FFFD4"}
    data_set = src.liquidity_monitor.daylight_overdraft(is_average)
    figure = go.Figure()
    end_date = None
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
        ts_tmp = ts

    __add_qt_regime(figure, end_date)
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
    color_map = {"50th % (main)": "#DC143C", "2.5th %": "#4BAAC8", "97.5th %": "#4BAAC8",
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

    __add_qt_regime(figure, end_date)
    figure.update_yaxes(title_text="Bps/%")
    figure.update_layout(legend={'orientation': "h", 'yanchor': "bottom",
                                 'y': 1.02, 'xanchor': "right", 'x': 1})
    figure.add_trace(go.Scatter(x=list(ts_tmp.keys()), y=len(list(ts_tmp.values())) * [0],
                                line={'color': "grey", 'width': 0.5}, showlegend=False, name=""))
    figure.update_layout(title="Reserve Demand Elasticity")
    figure = interface_utils.format_figure(figure)
    return figure


def __add_qt_regime(figure, end_date):
    figure.add_vrect(x0=src_config.PREV_QT_START, x1=src_config.PREV_QT_END,
                     annotation_text=f"QT: {src_config.PREV_QT_START.strftime('%Y.%m.%d')}"
                                     f" - {src_config.PREV_QT_END.strftime('%Y.%m.%d')}",
                     annotation_position="top left",
                     fillcolor="#536878", opacity=0.25, line_width=0)

    ed_str = src_config.QT_END.strftime('%Y.%m.%d') if src_config.QT_END is not None else 'Present'
    figure.add_vrect(x0=src_config.QT_START, x1=src_config.QT_END
    if src_config.QT_END is not None else end_date,
                     annotation_text=f"QT: {src_config.QT_START.strftime('%Y.%m.%d')}"
                                     f" - {ed_str}",
                     annotation_position="top left",
                     fillcolor="#536878", opacity=0.25, line_width=0)
    note = f'Last Update: {end_date.strftime("%Y.%m.%d")}'
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
    __add_qt_regime(figure, list(time_series.keys())[-1])
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
    __add_qt_regime(figure, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def __rrp_figure():
    start_date = src_config.TS_START_DATE_L
    end_date = interface_utils.end_date()
    time_series = src.liquidity_monitor.rrp_data(start_date, end_date)
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
    __add_qt_regime(figure, list(time_series.keys())[-1])
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
    __add_qt_regime(figure, list(time_series.keys())[-1])
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
    __add_qt_regime(figure, list(time_series.keys())[-1])
    figure = interface_utils.format_figure(figure)
    return figure

def iorb_effr_panel():
    """
    :return: panel for effr-iorb spread
    """
    figure = __iorb_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown('''
        * When reserves become less abundant, the cost to borrow federal funds tends to increase relative to IORB.
        * Recent references: 
            - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and 
            Understanding Repo Market Pressures, 09/24/2024](https://www.newyorkfed.org/newsevents/speeches/2024/per240926)
            - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")

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
    ], shadow="xs")

def overdraft_panel(is_average):
    """
    :return: panel for elasticity monitor
    """
    figure = __overdraft_figure(is_average)
    link = "https://www.newyorkfed.org/newsevents/speeches/2024/per240926/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown(f'''
        * Daylight overdrafts occur when short-term shifts in payment activity result in a temporarily negative balance in a bank’s reserve account.
        * Higher average overdrafts are an indication that reserves are harder to come by in amounts needed to facilitate payments without intraday credit from the Federal Reserve.
        * Average overdrafts are much more informative for our purposes because they abstract from idiosyncratic factors that may affect individual institutions.
        * Recent references: 
            - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/24/2024]({link})
            - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")

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
    ], shadow="xs")

def rrp_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __rrp_figure()
    link = "https://www.newyorkfed.org/newsevents/speeches/2024/per240926/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(dcc.Markdown(f'''
            * Domestic banks tend to borrow federal funds when they need liquidity, increased activity on their part would be a sign of reserves becoming less abundant
            * Recent references: 
                - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/24/2024]({link})
                - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
    ''', link_target="_blank", ), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")

def reserve_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __reserve_figure()
    link = "https://www.newyorkfed.org/newsevents/speeches/2024/per240926/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(dcc.Markdown(f'''
            * Domestic banks tend to borrow federal funds when they need liquidity, increased activity on their part would be a sign of reserves becoming less abundant
            * Recent references: 
                - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/24/2024]({link})
                - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
    ''', link_target="_blank", ), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")

def tga_panel():
    """
       :return: panel for elasticity monitor
       """
    figure = __tga_figure()
    link = "https://www.newyorkfed.org/newsevents/speeches/2024/per240926/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(dcc.Markdown(f'''
            * Domestic banks tend to borrow federal funds when they need liquidity, increased activity on their part would be a sign of reserves becoming less abundant
            * Recent references: 
                - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/24/2024]({link})
                - [Gara Afonso, Kevin Clark, Brian Gowen, Gabriele La Spada, JC Martinez, Jason Miu, and Will Riordan, "New Set of Indicators of Reserve Ampleness,” Federal Reserve Bank of New York Liberty Street Economics, 08/14/2024](https://libertystreeteconomics.newyorkfed.org/2024/08/a-new-set-of-indicators-of-reserve-ampleness/)
    ''', link_target="_blank", ), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")
