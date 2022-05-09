from dash import html, dcc
from dash.dependencies import Output, Input
import plotly.express as px

from app import (
    BODY_BGCOLOR,
    PERC_PRESC_MINMAX,
    PLOT_FONT,
    PLOT_TXTCOLOR,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    app,
    pres_df,
    year_choices
)

layout = html.Div(
    children=[
        dcc.Dropdown(
            id="selected-year",
            options=[{"label": str(x), "value": x} for x in year_choices],
            multi=False,
            value=year_choices[0],
            className="input"
        ),
        dcc.Graph(
            id='prescriptions-bar',
            figure={}
        ),
    ],
    className="barplot-container"
)

@app.callback(
    [
        Output(
            component_id="prescriptions-bar", 
            component_property="figure"
        ),
    ],
    [
        Input(
            component_id='selected-year', 
            component_property='value'
        ),
    ]
)
def update_prescriptions_barplot(year):
    yearview_df = pres_df.loc[pres_df.year == year, ['municipality', 'girls_perc', 'boys_perc']]
    yearview_df.rename(
        {'girls_perc': 'Flickor', 'boys_perc': 'Pojkar'},
        axis=1,
        inplace=True
    )
    yv_melted = yearview_df.melt(id_vars=['municipality'])

    # print(yearview_df.head())
    print(yv_melted.head())

    fig = px.histogram(
        yv_melted,
        x="value",
        color="variable",
        labels={
            'value': 'Andel som hämtade ut ADHD-medicin'
        },
        color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR],
        opacity=0.8,
        range_x=PERC_PRESC_MINMAX,
        title="Kommuner uppdelade utifrån andel barn som hämtade ut ADHD-medicin",
        barmode="overlay"
    )

    fig.update_layout(
        paper_bgcolor=BODY_BGCOLOR,
        plot_bgcolor=BODY_BGCOLOR,
        yaxis_title="Antal kommuner",
        legend=dict(
            font=PLOT_FONT,
            title="Kön"
        ),
        title=dict(
            font=dict(
                color=PLOT_FONT['color'],
                family=PLOT_FONT['family'],
                size=int(PLOT_FONT['size'] * 1.3)
            )
        )
    )
    fig.update_xaxes(
        title_font=PLOT_FONT,
        tickcolor=PLOT_TXTCOLOR,
        tickfont=PLOT_FONT
    )
    fig.update_yaxes(
        title_font=PLOT_FONT,
        tickcolor=PLOT_TXTCOLOR,
        tickfont=PLOT_FONT
    )

    fig.update_traces(
        hovertemplate='Andel som hämtade ut ADHD-medicin: %{x}%',
    )

    return fig,