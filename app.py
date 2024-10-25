"""app.py"""
from dash import Dash, html, dcc, page_registry, page_container
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__, title="Max Entropy", update_title=None, use_pages=True)
server = app.server


def get_icon(name):
    icon_map = {"home": "bi:house-door-fill", "reserve condition": "tdesign:dam-2",
                "money market": "fluent-mdl2:money",
                "central bank feeds": "jam:rss-feed"}
    return DashIconify(icon=icon_map[name.lower()], height=16)


sidebar = html.Div(
            children=[
                html.Div(dmc.NavLink(
                label=page["name"],
                href=page["path"],
                icon=get_icon(page["name"]),
                ), className="row")
                for page in page_registry.values()
            ], className="twelve columns",   style={"width": 240},
)

app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
    },
    children=[
    html.Div(
        children=[
            html.Div(
                children=[
                    sidebar
                ], className="one columns", style={"paddingLeft": "10px", "paddingRight": "10px"}),

            html.Div(
                children=[
                    page_container
                ], className="eleven columns", style={"paddingLeft": "0px", "paddingRight": "10px"})
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
