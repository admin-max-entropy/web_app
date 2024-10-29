"""interface utils"""
from datetime import datetime, timedelta
import pytz
import pages.config
import bs4


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
    figure.update_layout(font={'color': "#E0E0E0"}, margin={'l': 60, 'r': 20, "t": 50,'b': 40}, title_x=0)
    figure.update_layout(height=297)
    if show_x_range:
        figure.update_layout(xaxis=dict(rangeslider = dict(
            visible=True
        )))
    return figure

def end_date():
    """
    :return: return data in EST
    """
    current_time = datetime.now(pytz.timezone("America/New_York")).replace(hour=0, minute=0, second=0, microsecond=0)
    if current_time <= current_time.replace(hour=6):
        return current_time + timedelta(days=-1)
    return current_time

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
                 pages.config.LCOOK: "https://www.federalreserve.gov/feeds/s_t_cook.xml",
                 pages.config.LOGAN: "https://www.dallasfed.org/rss/speeches.xml",
                 pages.config.JWILLAIM: ""
                 }
    return names_map

def get_text_content(entry):
    soup = bs4.BeautifulSoup(entry.summary, features="html.parser")
    text = ""
    for tag in soup.find_all("br"):
        for row in tag.next_siblings:
            text += row.get_text()
        return text



def fed_cb_images():
    names_map = {pages.config.JPOW: "https://www.federalreservehistory.org/-/media/images/powell_jerome.jpg",
                 pages.config.MBARR: "https://www.federalreservehistory.org/-/media/images/Barr_Michael.jpg",
                 pages.config.CWALLER: "https://www.federalreservehistory.org/-/media/images/waller_christopher.jpg",
                 pages.config.PJEFF: "https://www.federalreservehistory.org/-/media/images/Jefferson_Phillip.jpg",
                 pages.config.MBOW: "https://www.federalreservehistory.org/-/media/images/bowman_michelle.jpg",
                 pages.config.AKUGLER: "https://www.federalreservehistory.org/-/media/images/Kugler_Adriana.jpg",
                 pages.config.LCOOK: "https://www.federalreservehistory.org/-/media/images/Cook_Lisa.jpg",
                 pages.config.LOGAN: "https://www.federalreservehistory.org/-/media/images/Logan_Lorie.jpg",
                 pages.config.JWILLAIM: "https://www.federalreservehistory.org/-/media/images/williams_john_c.jpg"
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
