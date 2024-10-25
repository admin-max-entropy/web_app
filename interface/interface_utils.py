"""interface utils"""
from datetime import datetime
import pytz

def rename_key(key):
    key = key.replace("FNYR-", "")
    key = key.replace("Pctl", "%")
    key = key.replace("-A", "")
    key = key.replace("_", " ")
    return key

def line_style_from_key(key):
    if "1%" in key or "99%" in key:
        return "lightblue", "dot"
    elif "25%" in key or "75%" in key:
        return "green", "dot"
    else:
        return "crimson", "solid"

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
    """
    :return: return data in EST
    """
    return datetime(2024, 10 ,23, tzinfo=pytz.timezone('US/Eastern'))
