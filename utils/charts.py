import plotly.express as px

def bar(df, x, y, title):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title
    )

    return fig
