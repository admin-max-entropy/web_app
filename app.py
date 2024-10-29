"""app.py"""
from dash import Dash, html, page_registry, page_container
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__, title="Max Entropy", update_title=None, use_pages=True)
server = app.server

def get_icon(name):
    icon_map = {"home": "bi:house-door-fill", "reserve condition": "tdesign:dam-2",
                "money market": "fluent-mdl2:money",
                "central bank feeds": "jam:rss-feed",
                "united states": "twemoji:flag-united-states"}
    return DashIconify(icon=icon_map[name.lower()], height=16)

def __create_page_structure():
    result = {}
    for page in list(page_registry.values()):
        path = page["path"]
        sub_path = path.split("/")
        assert(len(sub_path) in [2, 3])
        root = sub_path[1]
        if len(sub_path) == 2:
            result[root] = []
        else:
            if root not in result:
                result[root] = []
            result[root] += [page]
    return result

def create_sidebar():

    children = []
    page_structure = __create_page_structure()

    for page in list(page_registry.values()):
        path = page["path"]
        sub_path = path.split("/")
        root = sub_path[1]
        data = page_structure[root]

        if len(data) > 0:
            page_children = []
            for sub_page in data:
                page_children += [dmc.NavLink(
                    label=sub_page["name"].title(),
                    href=sub_page["path"],
                    icon=get_icon(sub_page["name"]))]

            component = html.Div(
                dmc.NavLink(
                label=root.replace("-", " ").title(),
                icon=get_icon(root.replace("-", " ")),
                children=page_children,
                opened=True,
            ))
            children.append(component)
        elif len(data) == 0:
            component = html.Div(dmc.NavLink(
                label=page["name"].title(),
                href=path,
                icon=get_icon(page["name"]),
                ), className="row")
            children.append(component)
        else:
            raise RuntimeError("unsupported page type")
    return html.Div(children=children, className="twelve columns")


app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
    },
    children=[
    html.Div(
        children=[
            html.Div(
                children=[
                    create_sidebar()
                ], className="one columns", style={"paddingLeft": "30px", "paddingRight": "10px"}),

            html.Div(
                children= [html.Div(dmc.Affix(
    dmc.Group(children=[DashIconify(icon="mdi-light:email", width=25,
                                    color="#90d5ff"), dmc.Text("admin@max-entropy.com",
                                                                                color="#90d5ff", variant="transit")]),
                    position={"top": 0, "right": 40}),
                    className="eleven columns", style={"paddingLeft": "0px", "paddingRight": "10px"}
)]+[
                    page_container
                ], className="eleven columns", style={"paddingLeft": "0px", "paddingRight": "10px"})
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
