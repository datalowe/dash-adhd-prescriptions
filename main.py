from dash import html
from dash.dependencies import Input, Output

from app import app
from sub_apps import (
    main_layout,
    prescription_bar,
    prescription_map,
    start_page
)


APP_TITLE = 'ADHD-medicinering i Sverige'


app.title = APP_TITLE

# define routes/subpages
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/karta':
        return prescription_map.layout
    elif pathname == '/histogram':
        return prescription_bar.layout
    else:
        return start_page.layout


app.layout = main_layout.chief_div
app.validation_layout = html.Div([
    main_layout.chief_div,
    prescription_bar.layout,
    prescription_map.layout,
    start_page.layout
])

if __name__ == '__main__':
    app.run_server(debug=True)
