import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Define directory path
DATA_DIR = "/Users/tsoghikpetrosyan/Desktop/myflaskapp/"

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Correlation between Stations"),

    html.Label("Select the first station (WAT parameters):"),
    dcc.Dropdown(
        id='wat-dropdown-1',
        options=[
            {"label": "ARTASHAT", "value": "ARTA"},
            # ... [all other WAT labels you provided]
            {"label": "AMASIA", "value": "AMAS"}
        ],
        value='ARTA'
    ),

    html.Label("Select the second station (either WAT or RAD parameters):"),
    dcc.Dropdown(
        id='station-dropdown-2',
        options=[
            {"label": "ARTASHAT (WAT)", "value": "ARTA_WAT"},
            # ... [all other WAT labels you provided]
            {"label": "AMASIA (WAT)", "value": "AMAS_WAT"},
            {'label': 'PARAKAR (RAD)', 'value': 'PARA_RAD'},
            # ... [all other RAD labels you provided]
            {'label': 'METSAMOR (RAD)', 'value': 'METS_RAD'}
        ],
        value='PARA_RAD'
    ),

    html.Button('Calculate Correlation', id='calculate-btn', n_clicks=0),

    html.Div(id='correlation-output'),

    dcc.Graph(id='correlation-graph')
])

# Callback function for the button click
@app.callback(
    Output('correlation-output', 'children'),
    Output('correlation-graph', 'figure'),
    Input('calculate-btn', 'n_clicks'),
    Input('wat-dropdown-1', 'value'),
    Input('station-dropdown-2', 'value')
)
def update_output(n_clicks, wat_value_1, station_value_2):
    # Load the selected datasets from the specified directory
    wat_data_1 = pd.read_csv(f'{DATA_DIR}{wat_value_1}23_WAT.CSV')
    
    # Determine if the second dataset is WAT or RAD
    station_type_2 = station_value_2.split('_')[1]
    station_name_2 = station_value_2.split('_')[0]
    
    if station_type_2 == "WAT":
        data_2 = pd.read_csv(f'{DATA_DIR}{station_name_2}23_WAT.CSV')
    else:  # RAD
        data_2 = pd.read_csv(f'{DATA_DIR}{station_name_2}23_RAD.CSV')
    
    # Calculate correlation
    correlation_value = wat_data_1['value'].corr(data_2['value'])

    # Generate the graph
    trace1 = go.Scatter(x=wat_data_1['date'], y=wat_data_1['value'], mode='lines', name=wat_value_1)
    trace2 = go.Scatter(x=data_2['date'], y=data_2['value'], mode='lines', name=station_name_2)
    layout = go.Layout(title=f'Data Visualization for Year 2023', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    figure = {'data': [trace1, trace2], 'layout': layout}
    
    return f'Correlation Value: {correlation_value}', figure

if __name__ == '__main__':
    app.run_server(debug=True)
