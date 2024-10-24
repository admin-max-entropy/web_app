"""interface utils"""
from datetime import datetime, tzinfo
import pytz

def format_figure(figure):
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
    figure.update_layout(font={'color': "#E0E0E0"}, margin={'l': 60, 'r': 0})
    return figure

def end_date():
    return datetime(2024, 10 ,23, tzinfo=pytz.timezone('US/Eastern'))
