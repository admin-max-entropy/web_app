import datetime
import interface.config as interface_config
import src.liquidity_monitor
import plotly.graph_objects as go
import interface.interface_utils
import dash_mantine_components as dmc
from dash import html, dcc
import src.config as src_config


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
                                    line=dict(color=color_map[key], width=1.2),
                                    text=list(map(lambda x: x.strftime("%Y-%m-%d"), list(ts.keys()))),
                                    hovertemplate=
                                    '%{y:.3f} bps/% <br>' +
                                    '%{text}',
                                    ))
        end_date = list(ts.keys())[-1]
        ts_tmp = ts

    __add_qt_regime(figure, end_date)
    figure.update_yaxes(title_text="Bps/%")
    figure.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    figure.add_trace(go.Scatter(x=list(ts_tmp.keys()), y=len(list(ts_tmp.values())) * [0],
                                line=dict(color="grey", width=0.5), showlegend=False, name=""))
    figure.update_layout(title="Reserve Demand Elasticity")
    figure = interface.interface_utils.format_figure(figure)
    return figure


def __add_qt_regime(figure, end_date):
    figure.add_vrect(x0=src_config.PREV_QT_START, x1=src.config.PREV_QT_END,
                     annotation_text=f"QT: {src_config.PREV_QT_START.strftime('%Y.%m.%d')}"
                                     f" - {src.config.PREV_QT_END.strftime('%Y.%m.%d')}",
                     annotation_position="top left",
                     fillcolor="#536878", opacity=0.25, line_width=0)

    figure.add_vrect(x0=src_config.QT_START, x1=src.config.QT_END if src.config.QT_END is not None else end_date,
                     annotation_text=f"QT: {src_config.QT_START.strftime('%Y.%m.%d')}"
                                     f" - {src.config.QT_END.strftime('%Y.%m.%d') if src.config.QT_END is not None else 'Present'}",
                     annotation_position="top left",
                     fillcolor="#536878", opacity=0.25, line_width=0)
    note = f'Last Update: {end_date.strftime("%Y.%m.%d")}'
    figure.add_annotation(
        showarrow=False,
        text=note,
        font=dict(size=10),
        xref='x domain',
        x=0,
        yref='y domain',
        y=-0.2
    )
    return figure

def __iorb_figure():
    start_date = src.config.TS_START_DATE
    end_date = datetime.datetime.today()
    time_series = src.liquidity_monitor.iorb_effr_spread(start_date, end_date)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=list(time_series.values()),
                                text=list(map(lambda x: x.strftime("%Y-%m-%d"), list(time_series.keys()))),
                                hovertemplate=
                                '%{y:.0f} bps <br>' +
                                '%{text}',
                                line=dict(color=interface_config.LINE_COLOR, width=interface_config.LINE_WIDTH),
                                name="",
                                showlegend=False))
    figure.add_trace(go.Scatter(x=list(time_series.keys()), y=len(list(time_series.values())) * [0],
                                line=dict(color="grey", width=0.5), showlegend=False, name=""))
    figure.update_layout(title="EFFR-IORB Spread")
    figure.update_yaxes(title_text="Bps")
    __add_qt_regime(figure, list(time_series.keys())[-1])
    figure = interface.interface_utils.format_figure(figure)
    return figure

def iorb_effr_panel():
    figure = __iorb_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown('''
        * When reserves become less abundant, the cost to borrow federal funds tends to increase relative to IORB.
        * Recent references: 
            - [Perli: 2024/9/26](https://www.newyorkfed.org/newsevents/speeches/2024/per240926)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")

def elasticity_panel():
    figure = __elasticity_figure()
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(dcc.Markdown('''
        * When reserves become less abundant, the elasticity of the federal funds rate to reserve changes could 
        be negative and statistically different from zero.
        * Recent references: 
            - [Gara Afonso, Domenico Giannone, Gabriele La Spada, and John C. Williams, “Tracking Reserve Ampleness 
            in Real Time Using Reserve Demand Elasticity,” Federal Reserve Bank of New York Liberty Street Economics, 
            October 17, 2024](https://libertystreeteconomics.newyorkfed.org/2024/10/tracking-reserve-ampleness-in-real-
            time-using-reserve-demand-elasticity/)
''',   link_target="_blank",), className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs")