import dash

import pandas as pd

BODY_BGCOLOR = 'rgba(0,0,0,255)'
PLOT_TXTCOLOR = '#FCC'
PLOT_FONT = dict(
    color=PLOT_TXTCOLOR,
    family='Arial',
    size=16
)
PRIMARY_COLOR = 'rgba(243, 173, 106, 1)'
SECONDARY_COLOR = 'rgba(255, 90, 90, 1)'
PERC_PRESC_MINMAX = (0, 17)

pres_df = pd.read_csv('./swe_adhdmed_geo_pop.csv')

year_choices = pres_df.year.unique()

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
