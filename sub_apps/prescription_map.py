from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px

from app import (
    BODY_BGCOLOR,
    PERC_PRESC_MINMAX,
    PLOT_FONT,
    app,
    pres_df,
    year_choices
)

layout = html.Div(
    [
        dcc.Dropdown(
            id="selected-year",
            options=[{"label": str(x), "value": x} for x in year_choices],
            multi=False,
            value=year_choices[0],
            className="input"
        ),

        dcc.Dropdown(
            id="selected-gender",
            options=[
                {"label": "Pojkar", "value": "boys_perc"},
                {"label": "Flickor", "value": "girls_perc"},
            ],
            multi=False,
            value="boys_perc",
            className="input"
        ),

        dcc.Graph(
                id='adhd-prescriptions-map',
                figure={},
                className="col-2-span justify-self-center",
                style={'width': '100vw', 'height': '80vh'}
        ),
    ],
    className="app-container"
)

@app.callback(
    [
        Output(
            component_id="adhd-prescriptions-map", 
            component_property="figure"
        )
    ],
    [
        Input(
            component_id='selected-year', 
            component_property='value'
        ),
        Input(
            'selected-gender', 
            component_property='options'
        ),
        Input(
            'selected-gender', 
            component_property='value'
        )
    ]
)
def update_map(year, g_opt, gender_coln):
    gender_label = [x['label'] for x in g_opt if x['value'] == gender_coln][0]
    
    title_str = (
        f'Andel {gender_label.lower()} som hämtade ut '
        f'ADHD-medicin år {year}'
    )

    yearview_df = pres_df[pres_df.year == year]
    yearview_df = yearview_df.dropna()

    fig = px.scatter_mapbox(
        yearview_df,
        lat='latitude',
        lon='longitude',
        size='pop_2020',
        color=gender_coln,
        range_color=PERC_PRESC_MINMAX,
        hover_name='municipality',
        hover_data={
            'longitude': False,
            'latitude': False,
        },
        labels={gender_coln: f'Andel (%)'},
        center=dict(lat=61, lon=14),
        zoom=4,
        mapbox_style="carto-darkmatter",
        color_continuous_scale='oryel',
        title=title_str
    )

    fig.update_traces(
        hovertemplate=(
            '<b>%{hovertext} </b><br>Andel '
            f'{gender_label.lower()}'
            ' som hämtade ut ADHD-medicin: %{marker.color}%'
        )
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=BODY_BGCOLOR,
        coloraxis=dict(
            colorbar=dict(
                outlinewidth=0,
                lenmode='fraction',
                len=0.5,
                thickness=15,
                orientation='h',
                tickfont=PLOT_FONT,
                ticksuffix="%",
                title=dict(
                    text="Andel",
                    font=PLOT_FONT
                )
            )
        ),
        title=dict(
            font=dict(
                color=PLOT_FONT['color'],
                family=PLOT_FONT['family'],
                size=int(PLOT_FONT['size'] * 1.3)
            )
        )
    )

    fig['layout']['uirevision'] = True

    return fig,