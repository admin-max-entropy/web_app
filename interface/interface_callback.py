import datetime
import interface.config as interface_config
import src.liquidity_monitor
import plotly.graph_objects as go
import interface.interface_utils
import dash_mantine_components as dmc
from dash import html, dcc
import src.config as src_config

def __iorb_figure():
    start_date = datetime.datetime(2017, 1, 1)
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
    note = f'Last Update: {list(time_series.keys())[-1].strftime("%Y.%m.%d")}'
    figure.add_annotation(
        showarrow=False,
        text=note,
        font=dict(size=10),
        xref='x domain',
        x=0,
        yref='y domain',
        y=-0.2
    )
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
