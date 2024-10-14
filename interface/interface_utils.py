
def format_figure(figure):
    figure = figure.update_layout(
        {
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(showgrid=False, zeroline=False)
    figure.update_layout(font=dict(color="white"))
    return figure