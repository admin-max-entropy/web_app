from dash import Dash, html, dcc, page_registry, page_container
import dash_mantine_components as dmc

app = Dash(__name__, title="Liquidity Monitor", update_title=None, use_pages=True)
server = app.server

app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
    },
    children=[html.Div([
    html.Div([
        html.Div(
            #dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            dcc.Link("", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),
    page_container
])])

if __name__ == '__main__':
    (app.
     run(debug=True))