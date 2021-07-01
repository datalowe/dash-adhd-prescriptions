import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

df = pd.read_csv('swe_adhd_prescription_combined.csv')

year_choices = df.year.unique()

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

app.layout = html.Div(
    [
        html.H1(
            "Förskrivning av ADHD-medicin till 0-17-åringar i Sverige", 
            className="col-2-span banner"
        ),

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
                style={'width': '100vw', 'height': '100vh'}
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
        f'ADHD-medicin {year}'
    )

    df_yearview = df[df.year == year]
    df_yearview = df_yearview[df_yearview.notna()]

    fig = px.density_mapbox(
        df_yearview,
        lat='latitude',
        lon='longitude',
        z=df_yearview[gender_coln],
        range_color=[0, 16],
        hover_name='municipality',
        hover_data={
            'longitude': False,
            'latitude': False, 
        },
        labels={gender_coln: 'Andel (%)'},
        radius=8,
        center=dict(lat=61, lon=14),
        zoom=4,
        mapbox_style="stamen-terrain"
    )

    fig.update_traces(
        hovertemplate='<b>%{hovertext} </b><br>Andel(%): %{z}%'
    )

    return fig,

app.run_server(debug=True)