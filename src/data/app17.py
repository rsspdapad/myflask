import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

# Define directory path
DATA_DIR = "/Users/tsoghikpetrosyan/Desktop/myflaskapp/"

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout with Bootstrap components
app.layout = dbc.Container([
    html.H1("Correlation between Stations", className="text-center mt-4 mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Select WAT parameter:"),
            dcc.Dropdown(id='wat-dropdown', options=[
            {"label": "None", "value": "None"}, 
            {"label": "ARTASHAT", "value": "ARTA23_WAT"},
            {"label": "KARCHAKHPYUR", "value": "KARC23_WAT"},
            {"label": "ASHOTSK", "value": "ASHO23_WAT"},
            {"label": "IJEVAN", "value": "IJEV23_WAT"},
            {"label": "NOYEMBERYAN", "value": "NOEM23_WAT"},
            {"label": "SHIRAKAMUT", "value": "SHIR23_WAT"},
            {"label": "GORIS", "value": "GORS23_WAT"},
            {"label": "KUCHAK", "value": "KUCH23_WAT"},
            {"label": "DZORAKHBYUR", "value": "DZOR23_WAT"},
            {"label": "EGHEGNADZOR", "value": "EKHG23_WAT"},
            {"label": "SEVAN", "value": "SEVN23_WAT"},
            {"label": "METSAMOR", "value": "METS23_WAT"},
            {"label": "AMASIA", "value": "AMAS23_WAT"},   
            ], value='None')
        ], width=6),

        dbc.Col([
            html.Label("Select another WAT parameter (optional):"),
            dcc.Dropdown(id='wat2-dropdown', options=[
            {"label": "None", "value": "None"},
            {"label": "ARTASHAT", "value": "ARTA23_WAT"},
            {"label": "KARCHAKHPYUR", "value": "KARC23_WAT"},
            {"label": "ASHOTSK", "value": "ASHO23_WAT"},
            {"label": "IJEVAN", "value": "IJEV23_WAT"},
            {"label": "NOYEMBERYAN", "value": "NOEM23_WAT"},
            {"label": "SHIRAKAMUT", "value": "SHIR23_WAT"},
            {"label": "GORIS", "value": "GORS23_WAT"},
            {"label": "KUCHAK", "value": "KUCH23_WAT"},
            {"label": "DZORAKHBYUR", "value": "DZOR23_WAT"},
            {"label": "EGHEGNADZOR", "value": "EKHG23_WAT"},
            {"label": "SEVAN", "value": "SEVN23_WAT"},
            {"label": "METSAMOR", "value": "METS23_WAT"},
            {"label": "AMASIA", "value": "AMAS23_WAT"},   
            ], value='None')
        ], width=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Select RAD parameter:"),
            dcc.Dropdown(id='rad-dropdown', options=[
            {'label': 'None', 'value': 'None'},
            {'label': 'PARAKAR', 'value': 'PARA23_RAD'},
            {'label': 'AZATAN', 'value': 'AZAT23_RAD'},
            {'label': 'ARTIK', 'value': 'ARTK23_RAD'},
            {'label': 'BAVRA', 'value': 'BAVR23_RAD'},
            {'label': 'VANADZOR', 'value': 'VANA23_RAD'},
            {'label': 'KOGHB', 'value': 'KOXB23_RAD'},
            {'label': 'STEPANAVAN', 'value': 'STEP23_RAD'},
            {'label': 'SHIRAKAMUT', 'value': 'SHIR23_RAD'},
            {'label': 'GORIS', 'value': 'GORS23_RAD'},
            {'label': 'SISIAN', 'value': 'SISN23_RAD'},
            {'label': 'KADJARAN', 'value': 'KADJ23_RAD'},
            {'label': 'ARUCH', 'value': 'ARUC23_RAD'},
            {'label': 'JERMUK', 'value': 'JERM23_RAD'},
            {'label': 'NOEMBERYAN', 'value': 'NOEM23_RAD'},
            {'label': 'EGHEGNADZOR', 'value': 'EKHG23_RAD'},
            {'label': 'VARDENIS', 'value': 'VARD23_RAD'},
            {'label': 'KARCHAGHBYUR', 'value': 'KARC23_RAD'},
            {'label': 'METSAMOR', 'value': 'METS23_RAD'},
            ], value='None')
        ], width=6),

        dbc.Col([
            html.Label("Select MAG parameter:"),
            dcc.Dropdown(id='mag-dropdown', options=[
            {'label': 'None', 'value': 'None'},
            {"label": "HOVIT", "value": "HOVT23_MAG"},
            {"label": "ARUCH", "value": "ARUC23_MAG"},
            {"label": "GARNI", "value": "GARN23_MAG"},
            {"label": "EGHEGNADZOR", "value": "EKHG23_MAG"},
            {"label": "KARCHAGHBYUR", "value": "KARC23_MAG"},
            {"label": "BAVRA", "value": "BAVR23_MAG"},
            {"label": "JERMUK", "value": "JERM23_MAG"},
            ], value='None')
        ], width=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Button('Calculate Correlation', id='calculate-btn', n_clicks=0, color="primary", className="mt-3")
        ], width=12, className="text-center")
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Div(id='correlation-output')
        ], width=12, className="text-center mb-3")
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='correlation-graph')
        ], width=12)
    ])
])

# Callback function for the button click
@app.callback(
    Output('correlation-output', 'children'),
    Output('correlation-graph', 'figure'),
    Input('calculate-btn', 'n_clicks'),
    Input('wat-dropdown', 'value'),
    Input('wat2-dropdown', 'value'),
    Input('rad-dropdown', 'value'),
    Input('mag-dropdown', 'value')
)
def update_output(n_clicks, wat_value, wat2_value, rad_value, mag_value):
    if n_clicks == 0:
        return dash.no_update, dash.no_update

    # Load the selected datasets based on dropdown values
    if wat_value != 'None':
        data_1 = pd.read_csv(f'{DATA_DIR}{wat_value}.csv')
        data1_type = wat_value.split('_')[0]
    elif rad_value != 'None':
        data_1 = pd.read_csv(f'{DATA_DIR}{rad_value}.csv')
        data1_type = rad_value.split('_')[0]
    elif mag_value != 'None':
        data_1 = pd.read_csv(f'{DATA_DIR}{mag_value}.csv')
        data1_type = mag_value.split('_')[0]
    else:
        return "Please select at least one parameter.", dash.no_update

    # Determine the second dataset for correlation
    if wat2_value != 'None':
        data_2 = pd.read_csv(f'{DATA_DIR}{wat2_value}.csv')
        data2_type = wat2_value.split('_')[0]
    elif rad_value != 'None' and data1_type != rad_value.split('_')[0]:
        data_2 = pd.read_csv(f'{DATA_DIR}{rad_value}.csv')
        data2_type = rad_value.split('_')[0]
    elif mag_value != 'None' and data1_type != mag_value.split('_')[0]:
        data_2 = pd.read_csv(f'{DATA_DIR}{mag_value}.csv')
        data2_type = mag_value.split('_')[0]
    else:
        return "Please select two different parameters to correlate.", dash.no_update

    # Calculate correlation
    correlation_value = data_1['value'].corr(data_2['value'])

    # Generate the graph
    trace1 = go.Scatter(x=data_1['date'], y=data_1['value'], mode='lines', name=data1_type)
    trace2 = go.Scatter(x=data_2['date'], y=data_2['value'], mode='lines', name=data2_type)
    layout = go.Layout(title=f'Data Visualization for Year 2023', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    figure = {'data': [trace1, trace2], 'layout': layout}

    return f'Correlation Value: {correlation_value}', figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
