import pathlib
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime
import os






# Declare server for Heroku deployment. Needed for Procfile.
server = app.server




# Load your data
def load_data(files):
    dataframes = {}
    for i, file in enumerate(files):
        df = pd.read_csv(file)
        try:
            df['date'] = pd.to_datetime(df['date'])
            df['datetime'] = pd.to_datetime(df['date'].dt.date.astype(str) + ' ' + df['hour'])
            df['month_day'] = df['datetime'].apply(lambda x: x.replace(year=2000))
            df['year'] = df['datetime'].dt.year
        except Exception as e:
            print(f"Error while processing file {file}: {e}")
        dataframes[i] = df
    return dataframes

# Create a Dash app
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
                html.H4("CONTROLS", className="card-header"),
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
                    html.P("Select parameter:", className="card-text", id="parameter-text", style={'display': 'none'}),
                    dcc.Dropdown(id='geo-parameters', clearable=False, className="my-3", style={'display': 'none'}),
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
                html.Div(className="card-header", style={'text-align': 'center'}, children=[
                    html.H4("REGIONAL SURVEY FOR SEISMIC PROTECTION")
                ]),
                html.Div(className="card-body", children=[
                    dcc.Graph(id='live-update-graph', config={'responsive': True}),
                    html.Hr(),
                ])
            ])
        ])
    ])
])


parameter_file_extensions = {
    "CA": "CA_",
    "CL": "CL_",
    "EH": "EH_",
    "HCO": "HCO",
    "HE": "HE_",
    "K": "K__",
    "MG": "MG_",
    "NA": "NA_",
    "NH4": "NH4",
    "NO2": "NO2",
    "NO3": "NO3",
    "PH": "PH_",
    "SO4": "SO4",
    "NAK": "NAK",
    "T": "T__",
    "F": "F__",
}

@app.callback(
    Output("location", "options"),
    Output("location", "value"),
    Input("analysis-type", "value")
)
def set_cities_options(selected_analysis):
    locations = []
    default_location = None

    if selected_analysis == 'RAD':
        locations = [
            {'label': 'PARAKAR', 'value': 'PARA'},
            {'label': 'AZATAN', 'value': 'AZAT'},
            {'label': 'ARTIK', 'value': 'ARTK'},
            {'label': 'BAVRA', 'value': 'BAVR'},
            {'label': 'VANADZOR', 'value': 'VANA'},
            {'label': 'KOGHB', 'value': 'KOXB'},
            {'label': 'STEPANAVAN', 'value': 'STEP'},
            {'label': 'SHIRAKAMUT', 'value': 'SHIR'},
            {'label': 'GORIS', 'value': 'GORS'},
            {'label': 'SISIAN', 'value': 'SISN'},
            {'label': 'KADJARAN', 'value': 'KADJ'},
            {'label': 'ARUCH', 'value': 'ARUC'},
            {'label': 'JERMUK', 'value': 'JERM'},
            {'label': 'NOEMBERYAN', 'value': 'NOEM'},
            {'label': 'EGHEGNADZOR', 'value': 'EKHG'},
            {'label': 'VARDENIS', 'value': 'VARD'},
            {'label': 'KARCHAGHBYUR', 'value': 'KARC'},
            {'label': 'METSAMOR', 'value': 'METS'},
        ]
        default_location = 'PARA'
    elif selected_analysis == 'WAT':
        locations = [
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
        ]
        default_location = 'ARTA'
    elif selected_analysis == 'MAG':  # Add locations for Magnetic Field Analysis
        locations = [
            {"label": "HOVIT", "value": "HOVT"},
            {"label": "ARUCH", "value": "ARUC"},
            {"label": "GARNI", "value": "GARN"},
            {"label": "EGHEGNADZOR", "value": "EKHG"},
            {"label": "KARCHAGHBYUR", "value": "KARC"},
            {"label": "BAVRA", "value": "BAVR"},
            {"label": "JERMUK", "value": "JERM"},
        ]
        default_location = "HOVT"
    elif selected_analysis == 'GEO':  # Add locations for Geochemical Analysis
        locations = [
            {"label": "ARARAT", "value": "ARAR"},
            {"label": "KARCHAGHBYUR", "value": "KARC"},
            {"label": "SURENAVAN", "value": "SURN"},
            {"label": "TSOVAGYUGH", "value": "TSOV"},
            {"label": "AKHURIK", "value": "ACHU"},
            {"label": "SARATOVKA", "value": "SART"},  # Add "SARATOVKA SART" location
            {"label": "KADJARAN", "value": "KADJ"},
            {"label": "STEPANAKERT", "value": "STIP"},  # Add "STEPANAKERT STIP" location
            # Add other locations for GEOCHEMICAL ANALYSIS here...
        ]
        default_location = "ARAR"

    return locations, default_location

@app.callback(
    Output("geo-parameters", "options"),
    Output("geo-parameters", "value"),
    Input("location", "value"),
    Input("analysis-type", "value")
)
def set_parameters_options(selected_location, selected_analysis):
    if selected_analysis == 'GEO':
        # Determine the available parameters based on the selected location
        if selected_location in ['ACHU', 'SART']:
            parameters = [
                {"label": "CA", "value": "CA"},
                {"label": "CL", "value": "CL"},
                {"label": "MG", "value": "MG"},
                {"label": "HCO3", "value": "HCO"},
                {"label": "SO4", "value": "SO4"},
                {"label": "NAK", "value": "NAK"},
                {"label": "PH", "value": "PH"},
                {"label": "T", "value": "T"},
            ]
        elif selected_location == 'KADJ':  # For KADJARAN
            parameters = [
                {"label": "CA", "value": "CA"},
                {"label": "CL", "value": "CL"},
                {"label": "HCO3", "value": "HCO"},
                {"label": "MG", "value": "MG"},
                {"label": "SO4", "value": "SO4"},
                {"label": "PH", "value": "PH"},
                {"label": "HE", "value": "HE"},
            ]
        elif selected_location == 'STIP':  # For STEAPANAKERT STIP
            parameters = [
                {"label": "CA", "value": "CA"},
                {"label": "CL", "value": "CL"},
                {"label": "F", "value": "F"},
                {"label": "HCO3", "value": "HCO"},
                {"label": "MG", "value": "MG"},
                {"label": "NH4", "value": "NH4"},
                {"label": "NO2", "value": "NO2"},
                {"label": "NO3", "value": "NO3"},
                {"label": "PH", "value": "PH"},
                {"label": "SO4", "value": "SO4"},
            ]
        else:
            # For other locations, include all the parameters
            parameters = [
                {"label": "CA", "value": "CA"},
                {"label": "CL", "value": "CL"},
                {"label": "EH", "value": "EH"},
                {"label": "HCO3", "value": "HCO"},
                {"label": "HE", "value": "HE"},
                {"label": "K", "value": "K"},
                {"label": "MG", "value": "MG"},
                {"label": "NA", "value": "NA"},
                {"label": "NH4", "value": "NH4"},
                {"label": "NO2", "value": "NO2"},
                {"label": "PH", "value": "PH"},
                {"label": "SO4", "value": "SO4"},
            ]
        default_parameter = parameters[0]['value']  # Set the default parameter based on the selected location
    else:
        parameters = []
        default_parameter = None

    return parameters, default_parameter

@app.callback(
    Output("geo-parameters", "style"),
    Output("parameter-text", "style"),
    Input("analysis-type", "value")
)
def toggle_parameter_dropdown(selected_analysis):
    if selected_analysis == 'GEO':
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

@app.callback(Output('live-update-graph', 'figure'),
              [Input('analysis-type', 'value'),
               Input('location', 'value'),
               Input('geo-parameters', 'value'),
               Input('frequency', 'value'),
               Input('graph-type', 'n_clicks')])
               
               
def update_graph_live(analysis, location, parameter, frequency, n_clicks):
    base_path = Path(__file__).parent / "data"  # Pointing to the "data" directory inside "src"
    
    if analysis == 'GEO':
        file_extension = parameter_file_extensions[parameter]
        file_names = [base_path / f"{location}{year}_{file_extension}.csv" for year in range(21, 31)]
    else:
        file_names = [base_path / f"{location}{year}_{analysis}.csv" for year in range(21, 31)]

    # Only keep file names for files that actually exist
    files = [file for file in file_names if os.path.isfile(file)]

    # Load the updated data
    dataframes = load_data(files)

    # Create a Plotly figure
    fig = go.Figure()

    # Define the colors for the lines based on view type
    colors_continuous = ['#117733', '#322288', '#882225']
    colors_yearly = ['#117733', '#322288', '#882225']

    if n_clicks % 2 == 0:  # Continuous View
        for i, df in dataframes.items():
            df = df.iloc[::frequency, :]
            for year, group in df.groupby('year'):
                color_index = (year - 2021) % len(colors_continuous)  # Calculate the color index based on the year
                fig.add_trace(go.Scatter(
                    x=group['month_day'],
                    y=group['value'],
                    mode='lines',
                    name=f'{location} {parameter} {year} ANALYSIS' if analysis == 'GEO' else f'{location} {year}',  # Modified graph title
                    line=dict(color=colors_continuous[color_index], width=1),  # Assign color to each line
                    hovertemplate='%{x}<br>%{y}<br>%{text}',
                    text=group['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
                ))

                average_value = group['value'].mean()
                x1 = df['month_day'].max()  # Use the maximum date as the end point

                fig.add_shape(type="line",
                              x0=group['month_day'].min(), y0=average_value,
                              x1=x1, y1=average_value,
                              line=dict(color='red', dash="dash", width=1),
                              name=f'Average for {location} {parameter} {year} ANALYSIS' if analysis == 'GEO' else f'Average for {location} {year}'  # Modified average line label
                              )
    else:  # Yearly View
        df_concat = pd.concat(dataframes.values()).sort_values(by='datetime')
        df_concat = df_concat.iloc[::frequency, :]

        for i, year in enumerate(df_concat['year'].unique()):
            color_index = (year - 2021) % len(colors_yearly)  # Calculate the color index based on the year
            year_data = df_concat[df_concat['year'] == year]
            fig.add_trace(go.Scatter(
                x=year_data['datetime'],
                y=year_data['value'],
                mode='lines',
                name=f'{location} {parameter} {year} ANALYSIS' if analysis == 'GEO' else f'{location} {year}',  # Modified graph title
                line=dict(color=colors_yearly[color_index], width=1),  # Assign color to each line
                hovertemplate='%{x}<br>%{y}<br>%{text}',
                text=year_data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            ))

            average_value = year_data['value'].mean()
            x1 = df_concat['datetime'].max()  # Use the maximum date as the end point

            fig.add_shape(type="line",
                          x0=year_data['datetime'].min(), y0=average_value,
                          x1=x1, y1=average_value,
                          line=dict(color='red', dash="dash", width=1),
                          name=f'Average for {location} {parameter} {year} ANALYSIS' if analysis == 'GEO' else f'Average for {location} {year}'  # Modified average line label
                          )

    fig.update_layout(
        autosize=False,
        width=1200,
        height=800,
        title={"text": f"{location.upper()} {parameter} ANALYSIS" if analysis == 'GEO' else f"{location.upper()} {analysis} ANALYSIS", 'x': 0.5, 'xanchor': 'center'},
        xaxis=dict(title="Date", tickformat="%m-%d"),  # Show months and days
        yaxis=dict(title="H/m" if analysis == 'WAT' else "C,imp/min" if analysis == 'RAD' else "E-2mg-e/l" if analysis == 'GEO' else "n/Tl" if analysis == 'MAG' else "Value"),  # Update the y-axis title based on the analysis type
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=90, b=50),
        hoverlabel=dict(font=dict(family="Roboto", size=12))
       )
    

    # Add the text "REGIONAL SURVEY FOR SEISMIC PROTECTION" at the bottom right corner of the graph
    fig.add_annotation(
        go.layout.Annotation(
            x=1,
            y=0,
            xref="paper",
            yref="paper",
            text="REGIONAL SURVEY FOR SEISMIC PROTECTION",
            showarrow=False,
            font=dict(size=10),
            align="right"
        )
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=False, port=port)
