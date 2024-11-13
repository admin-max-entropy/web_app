"""callback functions"""
import dash
import dash_mantine_components as dmc
from dash import html, dcc, Output, callback, Input
from interface import interface_utils
import pages.config


@callback(
    Output(component_id=pages.config.APP_ID_SPEECH_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_SPEECHES, component_property='value'),
    Input(component_id=pages.config.APP_ID_SPEECH_TAGS, component_property='value'),
    prevent_initial_call=False
)
def update_output_speech(input_value, tags):
    """
    :param input_value:
    :return:
    """
    return interface_utils.get_speeches(input_value, tags)

@callback(
    Output(component_id=pages.config.APP_ID_POLICY_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_POLICY, component_property='value'),
    prevent_initial_call=False
)
def update_output_policy(input_value):
    """
    :param input_value:
    :return:
    """
    return interface_utils.get_policy_updates(input_value)

@callback(
    Output(component_id=pages.config.APP_ID_RESEARCH_CARDS, component_property='children'),
    Input(component_id=pages.config.APP_ID_RESEARCH, component_property='value'),
    prevent_initial_call=False
)
def update_output_div(input_value):
    """
    :param input_value:
    :return:
    """
    return interface_utils.get_researches(input_value)

@callback(
    Output(component_id=pages.config.APP_ID_IORB_EFFR, component_property='children'),
    Input(component_id=pages.config.APP_ID_IORB_EFFR, component_property='id'),
    prevent_initial_call=False
)
def iorb_effr_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    figure = interface_utils.iorb_figure()
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_BGCR_IORB, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def iorb_bgcr_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.rate_to_iorb_figure("bgcr")
    return [dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * Recent references:
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"), className="row")],
            className="four columns",
            style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def iorb_tgcr_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update

    figure = interface_utils.rate_to_iorb_figure("tgcr")
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]


@callback(
    Output(component_id=pages.config.APP_ID_REPO_VOLUME, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def volume_repo_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update

    figure = interface_utils.secured_repo_volume_figure(is_repo=True)
    link = "https://www.financialresearch.gov/short-term-funding-monitor/market-digests/volume/chart-30/"

    return [dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown(f'''
        * TGCR: covers specific-counterparty tri-party general collateral repo transactions
        * BGCR: covers trades included in the TGCR & blind-brokered general collateral trades in the GCF Repo Service offered by the FICC
        * SOFR: covers trades in the BGCR & bilateral repo transactions cleared through the DVP Service offered by FICC, 
        filtered to remove a portion of transactions considered “specials.”
        * Recent references: 
            - [OFR Short-term Funding Monitor - Market Digests]({link})
''',   link_target="_blank"), className="row")],
            className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_UNSECURED_VOLUME, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def volume_unsecured_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.secured_repo_volume_figure(is_repo=False)
    link_1 = "https://www.financialresearch.gov/short-term-funding-monitor/market-digests/volume/chart-30/"
    link_2 = "https://libertystreeteconomics.newyorkfed.org/2017/08/regulatory-incentives-and-quarter-end-dynamics-in-the-repo-market/"
    return dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown(f'''
        * EFFR: based on data on overnight federal funds transactions provided by domestic banks and U.S. branches and agencies of foreign banks
        * OBFR: based on data on EFFR & Eurodollar transactions and certain domestic deposits
        * Recent references: 
            - [OFR Short-term Funding Monitor - Market Digests]({link_1})
            - [Regulatory Incentives and Quarter‑End Dynamics in the Repo Market]({link_2})
''',   link_target="_blank"), className="row")],
            className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")

@callback(
    Output(component_id=pages.config.APP_ID_SOFR_IORB, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def iorb_sofr_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.rate_to_iorb_figure("sofr")
    return [dmc.Paper(children=[
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
                 className="row")
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_OBFR_IORB, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def iorb_obfr_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.rate_to_iorb_figure("obfr")
    return [dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
         * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
''',   link_target="_blank"),className="row")
                          ], className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_EFFR_IORB, component_property='children'),
    Input(component_id=pages.config.APP_ID_TGCR_IORB, component_property='children'),
    prevent_initial_call=False
)
def iorb_fedfund_panel(dummy):
    """
    :return: panel for effr-iorb spread
    """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.rate_to_iorb_figure("effr")
    return [dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
        html.Div(children=[
            html.Div(dcc.Markdown('''
        * When reserves become less abundant, the cost to borrow federal funds tends to increase relative to IORB.
        * Currently, EFFR has a persistent -7 bps spread to IOER. 
        * However, should keep an eye on the EFFR at 99% to IOER spread as well. 
        be negative and statistically different from zero.
         * Recent references: 
            - [Lorie Logan, Normalizing the FOMC’s monetary policy tools, 10/21/2024](https://www.dallasfed.org/news/speeches/logan/2024/lkl241021)
            - [Roberto Perli, Balance Sheet Normalization: Monitoring Reserve Conditions and Understanding Repo Market Pressures, 09/26/2024](https://www.newyorkfed.org/newsevents/speeches/2024/per240926)
''',   link_target="_blank"),className="row")
                          ], className="four columns", style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_ELASTICITY, component_property='children'),
    Input(component_id=pages.config.APP_ID_ELASTICITY, component_property='id'),
    prevent_initial_call=False
)
def elasticity_panel(dummy):
    """
    :return: panel for elasticity monitor
    """
    figure = interface_utils.elasticity_figure()
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

@callback(
    Output(component_id=pages.config.APP_ID_OVERDRAFT_AVERAGE, component_property='children'),
    Input(component_id=pages.config.APP_ID_OVERDRAFT_AVERAGE, component_property='id'),
    prevent_initial_call=False
)
def overdraft_panel(dummy):
    """
    :return: panel for elasticity monitor
    """
    figure = interface_utils.overdraft_figure(is_average=True)
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_OVERDRAFT_PEAK, component_property='children'),
    Input(component_id=pages.config.APP_ID_OVERDRAFT_AVERAGE, component_property='children'),
    prevent_initial_call=False
)
def overdraft_panel(dummy):
    if dummy is None:
        return dash.no_update
    """
    :return: panel for elasticity monitor
    """
    figure = interface_utils.overdraft_figure(is_average=False)
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_FF_VOLUME, component_property='children'),
    Input(component_id=pages.config.APP_ID_FF_VOLUME, component_property='id'),
    prevent_initial_call=False
)
def fedfund_panel(dummy):
    """
    :return: panel for elasticity monitor
    """
    figure = interface_utils.fedfund_figure()
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

@callback(
    Output(component_id=pages.config.APP_ID_RRP_PANEL, component_property='children'),
    Input(component_id=pages.config.APP_ID_RRP_PANEL, component_property='id'),
    prevent_initial_call=False
)
def rrp_panel(dummy):
    """
       :return: panel for elasticity monitor
       """
    figure = interface_utils.rrp_figure()
    link = ("https://www.kansascityfed.org/research/economic-bulletin/rapid-declines-in-the-feds-"
            "overnight-reverse-repurchase-on-rrp-facility-may-start-to-slow")
    return [dmc.Paper(children=[
        html.Div(children=[html.Div(dcc.Graph(figure=figure), className="eight columns"),
                           html.Div(
                               children=[
                                   html.Div(dmc.Badge("Liability",
                                                      variant="filled", color="yellow"),
                                            className="row"),
                               html.Div(dcc.Markdown(f'''
            * Currently, RRP is used as a tool to help keep the federal funds rate in the target range established by the FOMC.
            * We tend to see RRP balances increase over quarter-end, due to the banks refrain from intermediations on 
            repo trades with Money Market Funds at quarter ends.
            * Recent references: 
                - [Kansas City Fed, Rapid Declines in the Fed’s Overnight Reverse Repurchase (ON RRP) Facility May Start to Slow, 11/10/2023]({link})
    ''', link_target="_blank", ), className="row")],
                               className="four columns",
                               style={"padding-top": "20px"})],
                 className="row"),
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_FOREIGN_RRP_PANEL, component_property='children'),
    Input(component_id=pages.config.APP_ID_RRP_PANEL, component_property='children'),
    prevent_initial_call=False
)
def foreign_rrp_panel(dummy):
    """
       :return: panel for elasticity monitor
       """
    if dummy is None:
        return dash.no_update
    figure = interface_utils.foreign_rrp_figure()
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_RESERVE_PANEL, component_property='children'),
    Input(component_id=pages.config.APP_ID_RRP_PANEL, component_property='children'),
    prevent_initial_call=False
)
def reserve_panel(dummy):
    """
       :return: panel for elasticity monitor
       """
    if dummy is None:
        return dash.no_update

    figure = interface_utils.reserve_figure()
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]

@callback(
    Output(component_id=pages.config.APP_ID_TGA_PANEL, component_property='children'),
    Input(component_id=pages.config.APP_ID_RRP_PANEL, component_property='children'),
    prevent_initial_call=False
)
def tga_panel(dummy):
    """
       :return: panel for elasticity monitor
       """
    if dummy is None:
        return dash.no_update

    figure = interface_utils.tga_figure()
    return [dmc.Paper(children=[
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
    ], shadow="xs", bg="black")]
