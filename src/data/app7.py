import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime

# Load your data
def load_parameter_data(location, analysis, parameter=None):
    dfs = []
    for year in range(21, 24):  # for years 2021, 2022, 2023
        if analysis == 'GEO':
            filename = f"C:/Users/THOM/Desktop/myflaskapp/{location}{year}_{parameter}_.csv"
        else:
            filename = f"C:/Users/THOM/Desktop/myflaskapp/{location}{year}_{analysis}.csv"
        try:
            df = pd.read_csv(filename)
            df['date'] = pd.to_datetime(df['date'])
            df['datetime'] = pd.to_datetime(df['date'].dt.date.astype(str) + ' ' + df['hour'])
            df['month_day'] = df['datetime'].apply(lambda x: x.replace(year=2000))
            df['year'] = df['datetime'].dt.year
            dfs.append(df)
        except Exception as e:
            print(f"Error while processing file {filename}: {e}")
    return pd.concat(dfs) if dfs else pd.DataFrame()

# Create a Dash app
app = Dash(__name__, external_stylesheets=[
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
])

# Define the layout
app.layout = html.Div(className="container-fluid", style={'font-family': 'Roboto'}, children=[
    html.Div(className="row", children=[
        html.Div(className="col-3", children=[
            html.Div(className="card", children=[
                html.H4("Controls", className="card-header"),
                html.Div(className="card-body", children=[
                    html.P("Select analysis type:", className="card-text"),
                    dcc.Dropdown(id='analysis-type', options=[
                        {'label': 'UNDERGROUND WATER LEVEL', 'value': 'WAT'},
                        {'label': 'RADON GAS ANALYSIS', 'value': 'RAD'},
                        {'label': 'MAGNETIC FIELD ANALYSIS', 'value': 'MAG'},
                        {'label': 'GEOCHEMICAL ANALYSIS', 'value': 'GEO'}
                    ], value='WAT', clearable=False, className="my-3"),
                    html.P("Select location:", className="card-text", id="location-text"),
                    dcc.Dropdown(id='location', clearable=False, className="my-3"),
                    html.P("Select geochemical parameter:", className="card-text", id="geo-param-text"),
                    dcc.Dropdown(id='geo-parameters', clearable=False, className="my-3"),
                    html.P("Select frequency:", className="card-text"),
                    dcc.RadioItems(
                        id='frequency',
                        options=[
                            {'label': 'All', 'value': 1},
                            {'label': 'Every 2 days', 'value': 2},
                            {'label': 'Every 3 days', 'value': 3},
                            {'label': 'Every 5 days', 'value': 5}
                        ],
                        value=1,
                        labelStyle={'display': 'block'},
                        className="my-3"
                    ),
                    html.Button('Toggle Continuous/Yearly', id='graph-type', n_clicks=0, className="btn btn-primary"),
                ])
            ])
        ]),
        html.Div(className="col-9", children=[
            html.Div(className="card", children=[
                html.H4("REGIONAL SURVEY FOR SEISMIC PROTECTION", className="card-header"),
                html.Div(className="card-body", children=[
                    dcc.Graph(id='live-update-graph', config={'responsive': True}),
                    html.Hr(),
                ])
            ])
        ])
    ])
])

@app.callback(
    Output("location", "options"),
    Output("location", "value"),
    Input("analysis-type", "value")
)
def set_cities_options(selected_analysis):
    locations = []
    default_location = None

    if selected_analysis == 'GEO':
        locations = [
            {"label": "ARARAT", "value": "ARAR"},
            {"label": "KARCHAGHBYUR", "value": "KARC"},
            {"label": "SURENAVAN", "value": "SURN"},
            {"label": "TSOVAGYUGH", "value": "TSOV"},
            {"label": "ACHURIK", "value": "ACHU"},
            {"label": "SARATOVKA", "value": "SART"},
            {"label": "KADJARAN", "value": "KADJ"},
            {"label": "STEPANAKERT", "value": "STIP"},
        ]
        default_location = 'ARAR'

    # Add conditions for other types of analysis here...

    return locations, default_location

@app.callback(
    Output("geo-parameters", "options"),
    Output("geo-parameters", "value"),
    [Input("location", "value"),
     Input("analysis-type", "value")]
)
def set_geo_parameters(selected_location, selected_analysis):
    parameters = []
    default_parameter = None

    twelve_parameters = [
        {'label': 'CA', 'value': 'CA'},
        {'label': 'CL', 'value': 'CL'},
        {'label': 'EH', 'value': 'EH'},
        {'label': 'HCO3', 'value': 'HCO3'},
        {'label': 'HE', 'value': 'HE'},
        {'label': 'K', 'value': 'K'},
        {'label': 'MG', 'value': 'MG'},
        {'label': 'NA', 'value': 'NA'},
        {'label': 'NH4', 'value': 'NH4'},
        {'label': 'NO2', 'value': 'NO2'},
        {'label': 'PH', 'value': 'PH'},
        {'label': 'SO4', 'value': 'SO4'},
    ]

    eight_parameters = [
        {'label': 'CA', 'value': 'CA'},
        {'label': 'CL', 'value': 'CL'},
        {'label': 'MG', 'value': 'MG'},
        {'label': 'HCO3', 'value': 'HCO3'},
        {'label': 'SO4', 'value': 'SO4'},
        {'label': 'NAK', 'value': 'NAK'},
        {'label': 'PH', 'value': 'PH'},
        {'label': 'T', 'value': 'T'},
    ]

    seven_parameters = [
        {'label': 'CA', 'value': 'CA'},
        {'label': 'CL', 'value': 'CL'},
        {'label': 'HCO3', 'value': 'HCO3'},
        {'label': 'MG', 'value': 'MG'},
        {'label': 'SO4', 'value': 'SO4'},
        {'label': 'PH', 'value': 'PH'},
        {'label': 'HE', 'value': 'HE'},
    ]

    nine_parameters = [
        {'label': 'CA', 'value': 'CA'},
        {'label': 'CL', 'value': 'CL'},
        {'label': 'HCO3', 'value': 'HCO3'},
        {'label': 'MG', 'value': 'MG'},
        {'label': 'NH4', 'value': 'NH4'},
        {'label': 'NO2', 'value': 'NO2'},
        {'label': 'NO3', 'value': 'NO3'},
        {'label': 'PH', 'value': 'PH'},
        {'label': 'SO4', 'value': 'SO4'},
    ]

    if selected_analysis == 'GEO':
        if selected_location == 'ARAR':
            parameters = twelve_parameters
        elif selected_location == 'KARC':
            parameters = twelve_parameters
        elif selected_location == 'SURN':
            parameters = twelve_parameters
        elif selected_location == 'TSOV':
            parameters = twelve_parameters
        elif selected_location == 'ACHU':
            parameters = eight_parameters
        elif selected_location == 'SART':
            parameters = eight_parameters
        elif selected_location == 'KADJ':
            parameters = seven_parameters
        elif selected_location == 'STIP':
            parameters = nine_parameters

        default_parameter = 'CA'

    return parameters, default_parameter

@app.callback(Output('live-update-graph', 'figure'),
              [Input('analysis-type', 'value'),
               Input('location', 'value'),
               Input('geo-parameters', 'value'),
               Input('frequency', 'value'),
               Input('graph-type', 'n_clicks')])
def update_graph_live(analysis, location, parameter, frequency, n_clicks):
    # Load the updated data
    df = load_parameter_data(location, analysis, parameter)

    # Create a Plotly figure
    fig = go.Figure()

    # Define the colors for the lines based on view type
    colors_continuous = ['#117733', '#322288', '#882225']
    colors_yearly = ['#117733', '#322288', '#882225']

    if n_clicks % 2 == 0:  # Continuous View
        df = df.iloc[::frequency, :]
        for year, group in df.groupby('year'):
            color_index = (year - 2021) % len(colors_continuous)  # Calculate the color index based on the year
            fig.add_trace(go.Scatter(
                x=group['month_day'],
                y=group['value'],
                mode='lines',
                name=f'{location} {year}',
                line=dict(color=colors_continuous[color_index], width=2),  # Assign color to each line
                hovertemplate='%{x}<br>%{y}<br>%{text}',
                text=group['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            ))

            average_value = group['value'].mean()
            x1 = df['month_day'].max()  # Use the maximum date as the end point

            fig.add_shape(type="line",
                          x0=group['month_day'].min(), y0=average_value,
                          x1=x1, y1=average_value,
                          line=dict(color='red', dash="dash", width=1),
                          name=f'Average for {location} {year}')
    else:  # Yearly View
        df = df.iloc[::frequency, :]

        for i, year in enumerate(df['year'].unique()):
            color_index = (year - 2021) % len(colors_yearly)  # Calculate the color index based on the year
            year_data = df[df['year'] == year]
            fig.add_trace(go.Scatter(
                x=year_data['datetime'],
                y=year_data['value'],
                mode='lines',
                name=f'{location} {year}',
                line=dict(color=colors_yearly[color_index], width=1),  # Assign color to each line
                hovertemplate='%{x}<br>%{y}<br>%{text}',
                text=year_data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            ))

            average_value = year_data['value'].mean()
            x1 = df['datetime'].max()  # Use the maximum date as the end point

            fig.add_shape(type="line",
                          x0=year_data['datetime'].min(), y0=average_value,
                          x1=x1, y1=average_value,
                          line=dict(color='red', dash="dash", width=1),
                          name=f'Average for {location} {year}')

    fig.update_layout(
        autosize=False,
        width=1200,
        height=800,
        title={"text": f"{location.upper()} {analysis} ANALYSIS", "font": {"size": 24, 'family': 'Roboto'}},
        font=dict(size=18, family='Roboto'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black')
    )
    fig.update_xaxes(tickformat="%m-%d")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
