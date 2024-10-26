"""interface utils"""
from datetime import datetime
from tkinter.font import names

import pytz
import pages.config


def rename_key(key):
    """
    :param key:
    :return: renamed key for data from OFR
    """
    key = key.replace("FNYR-", "")
    key = key.replace("Pctl", "%")
    key = key.replace("-A", "")
    key = key.replace("_", " ")
    return key

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
    return datetime.now(pytz.timezone("America/New_York")).replace(hour=0, minute=0, second=0, microsecond=0)

def fed_rss_tags(names_map):
    data = []
    for key in names_map:
        data.append(dict(value=key, label=key))
    return data

def fed_central_bankers():
    names_map = {pages.config.JPOW: "https://www.federalreserve.gov/feeds/s_t_powell.xml",
                 pages.config.MBARR: "https://www.federalreserve.gov/feeds/s_t_barr.xml",
                 pages.config.CWALLER: "https://www.federalreserve.gov/feeds/s_t_waller.xml",
                 pages.config.PJEFF: "https://www.federalreserve.gov/feeds/s_t_jefferson.xml",
                 pages.config.MBOW: "https://www.federalreserve.gov/feeds/m_w_Bowman.xml",
                 pages.config.AKUGLER: "https://www.federalreserve.gov/feeds/s_t_kugler.xml",
                 pages.config.LCOOK: "https://www.federalreserve.gov/feeds/s_t_cook.xml"}
    return names_map

def fed_cb_images():
    names_map = {pages.config.JPOW: "https://www.federalreservehistory.org/-/media/images/powell_jerome.jpg",
                 pages.config.MBARR: "https://www.federalreservehistory.org/-/media/images/Barr_Michael.jpg",
                 pages.config.CWALLER: "https://www.federalreservehistory.org/-/media/images/waller_christopher.jpg",
                 pages.config.PJEFF: "https://www.federalreservehistory.org/-/media/images/Jefferson_Phillip.jpg",
                 pages.config.MBOW: "https://www.federalreservehistory.org/-/media/images/bowman_michelle.jpg",
                 pages.config.AKUGLER: "https://www.federalreservehistory.org/-/media/images/Kugler_Adriana.jpg",
                 pages.config.LCOOK: "https://www.federalreservehistory.org/-/media/images/Cook_Lisa.jpg"
                 }
    return names_map


def fed_research_feeds():
    names_map = {pages.config.FEDS_NOTES: "https://www.federalreserve.gov/feeds/feds_notes.xml",
                 pages.config.FINANCE_AND_ECONOMICS_DISCUSSION: "https://www.federalreserve.gov/feeds/feds.xml",
                 pages.config.FRB_WORKING_PAPER: "https://www.federalreserve.gov/feeds/working_papers.xml"
                 }
    return names_map

def fed_research_color():
    names_map = {pages.config.FEDS_NOTES: "cyan",
                 pages.config.FINANCE_AND_ECONOMICS_DISCUSSION: "pink",
                 pages.config.FRB_WORKING_PAPER: "blue"
                 }
    return names_map

def fed_cb_policy():
    names_map = {pages.config.MONETARY_POLICY: "https://federalreserve.gov/feeds/press_monetary.xml",
                 pages.config.BANKING_REGULATION: "https://www.federalreserve.gov/feeds/press_bcreg.xml"
                 }
    return names_map

def fed_cb_policy_color():
    names_map = {pages.config.MONETARY_POLICY: "teal",
                 pages.config.BANKING_REGULATION: "pink"
                 }
    return names_map


def convert_fed_rss_time(input_time):
    gmt = pytz.timezone('GMT')
    eastern = pytz.timezone('US/Eastern')
    date = datetime.strptime(input_time, "%a, %d %b %Y %H:%M:%S GMT")
    date_gmt = gmt.localize(date)
    date_eastern = date_gmt.astimezone(eastern)
    return date_eastern
