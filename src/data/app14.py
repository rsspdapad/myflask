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
            {"label": "KARCHAKHPYUR", "value": "KARC"},
            {"label": "ASHOTSK", "value": "ASHO"},
            {"label": "IJEVAN", "value": "IJEV"},
            {"label": "NOYEMBERYAN", "value": "NOEM"},
            {"label": "SHIRAKAMUT", "value": "SHIR"},
            {"label": "GORIS", "value": "GORS"},
            {"label": "KUCHAK", "value": "KUCH"},
            {"label": "DZORAKHBYUR", "value": "DZOR"},
            {"label": "EGHEGNADZOR", "value": "EKHG"},
            {"label": "SEVAN", "value": "SEVN"},
            {"label": "METSAMOR", "value": "METS"},
            {"label": "AMASIA", "value": "AMAS"}
        ],
        value='ARTA'
    ),

    html.Label("Select the second station (either WAT or RAD parameters):"),
    dcc.Dropdown(
        id='station-dropdown-2',
        options=[
            {"label": "ARTASHAT (WAT)", "value": "ARTA_WAT"},
            {"label": "KARCHAKHPYUR (WAT)", "value": "KARC_WAT"},
            {"label": "ASHOTSK (WAT)", "value": "ASHO_WAT"},
            {"label": "IJEVAN (WAT)", "value": "IJEV_WAT"},
            {"label": "NOYEMBERYAN (WAT)", "value": "NOEM_WAT"},
            {"label": "SHIRAKAMUT (WAT)", "value": "SHIR_WAT"},
            {"label": "GORIS (WAT)", "value": "GORS_WAT"},
            {"label": "KUCHAK (WAT)", "value": "KUCH_WAT"},
            {"label": "DZORAKHBYUR (WAT)", "value": "DZOR_WAT"},
            {"label": "EGHEGNADZOR (WAT)", "value": "EKHG_WAT"},
            {"label": "SEVAN (WAT)", "value": "SEVN_WAT"},
            {"label": "METSAMOR (WAT)", "value": "METS_WAT"},
            {"label": "AMASIA (WAT)", "value": "AMAS_WAT"},
            {'label': 'PARAKAR (RAD)', 'value': 'PARA_RAD'},
            {'label': 'AZATAN (RAD)', 'value': 'AZAT_RAD'},
            {'label': 'ARTIK (RAD)', 'value': 'ARTK_RAD'},
            {'label': 'BAVRA (RAD)', 'value': 'BAVR_RAD'},
            {'label': 'VANADZOR (RAD)', 'value': 'VANA_RAD'},
            {'label': 'KOGHB (RAD)', 'value': 'KOXB_RAD'},
            {'label': 'STEPANAVAN (RAD)', 'value': 'STEP_RAD'},
            {'label': 'SHIRAKAMUT (RAD)', 'value': 'SHIR_RAD'},
            {'label': 'GORIS (RAD)', 'value': 'GORS_RAD'},
            {'label': 'SISIAN (RAD)', 'value': 'SISN_RAD'},
            {'label': 'KADJARAN (RAD)', 'value': 'KADJ_RAD'},
            {'label': 'ARUCH (RAD)', 'value': 'ARUC_RAD'},
            {'label': 'JERMUK (RAD)', 'value': 'JERM_RAD'},
            {'label': 'NOEMBERYAN (RAD)', 'value': 'NOEM_RAD'},
            {'label': 'EGHEGNADZOR (RAD)', 'value': 'EKHG_RAD'},
            {'label': 'VARDENIS (RAD)', 'value': 'VARD_RAD'},
            {'label': 'KARCHAGHBYUR (RAD)', 'value': 'KARC_RAD'},
            {'label': 'METSAMOR (RAD)', 'value': 'METS_RAD'},
        
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
    trace1 = go.Scatter(x=wat_data_1['date'], y=wat_data_1['value'], mode='lines', name=f'{wat_value_1}23.WAT')
    trace2 = go.Scatter(x=data_2['date'], y=data_2['value'], mode='lines', name=f'{station_name_2}23.{station_type_2}')
    layout = go.Layout(title=f'Data Visualization for Year 2023', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    figure = {'data': [trace1, trace2], 'layout': layout}
    
    return f'Correlation Value: {correlation_value}', figure

if __name__ == '__main__':
    app.run_server(debug=True)
