from dash import Dash, dcc, html, Input, Output, ctx

import plotly.express as px
import pandas as pd
import load

app = Dash(__name__)

current_metric = 'None'

app.layout = html.Div([
    html.H4('Country information'),
    html.Button('Reset Data', id='reset', n_clicks=0),
    html.P("Select a metric:"),
    dcc.Dropdown(
        id='metric',
        options=['Number of Languages Spoken',
       'Landlocked', 'Number of Borders', 'Area', 'Population', 'GINI',
       'Drives on Right', 'Life Expectancy (2007)',
       'GDP Per Capita (2007)'],
    ),
    dcc.Graph(id="map"),
])

@app.callback(
    Output('map', 'figure'), 
    Input('metric', 'value'),
    Input('reset', 'n_clicks')
)
def display_choropleth(metric, n_clicks):
    global current_metric
    triggered_id = ctx.triggered_id

    if triggered_id == 'reset':
        load.upload()
        metric = current_metric
    else:
        current_metric = metric
    countries = load.download()

    df = pd.DataFrame(countries)
    
    fig = px.choropleth(
        df,
        locations = 'ISO',
        color = metric,
        hover_name = 'Name',
        height=700
        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

app.run_server(debug=True)