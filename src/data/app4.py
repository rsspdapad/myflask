import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime

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
                        {'label': 'RADON GAS ANALYSIS', 'value': 'RAD'}
                    ], value='WAT', clearable=False, className="my-3"),
                    html.P("Select location:", className="card-text"),
                    dcc.Dropdown(id='location', value='AZAT', clearable=False, className="my-3"),
                    html.P("Select frequency:", className="card-text"),
                    dcc.RadioItems(
                        id='frequency',
                        options=[
                            {'label': 'All', 'value': 1},
                            {'label': 'Every 1 day', 'value': 1},
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
    if selected_analysis == 'RAD':
        return [
            {'label': 'UNDER PARAKAR', 'value': 'PARA'},
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
            {'label': 'STEPANAKERT', 'value': 'STIP'},
            {'label': 'MARTAKERT', 'value': 'MARD'}
        ], "PARA"
    else:
        locations = [
            {"label": "AZATAN", "value": "AZAT"},
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
        return locations, "AZAT"

def get_average_trace(df, location, year):
    average_value = df['value'].mean()
    x1 = df['month_day'].max()  # Use the maximum date as the end point
    return go.Scatter(
        x=df['month_day'],
        y=df['value'],
        mode='lines',
        name=f'{location} {year}',
        line=dict(width=2),
        hovertemplate='%{x}<br>%{y}<br>%{text}',
        text=df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    ), go.Scatter(
        x=[df['month_day'].min(), x1],
        y=[average_value, average_value],
        mode='lines',
        name=f'Average for {location} {year}',
        line=dict(color='red', dash="dash", width=1),
        hoverinfo='skip'
    )

@app.callback(Output('live-update-graph', 'figure'),
              [Input('analysis-type', 'value'),
               Input('location', 'value'),
               Input('frequency', 'value'),
               Input('graph-type', 'n_clicks')])
def update_graph_live(analysis, location, frequency, n_clicks):
    # Define file names based on selection
    files = [f"C:/Users/THOM/Desktop/myflaskapp/{location}21_{analysis}.csv",
             f"C:/Users/THOM/Desktop/myflaskapp/{location}22_{analysis}.csv",
             f"C:/Users/THOM/Desktop/myflaskapp/{location}23_{analysis}.csv"]

    # Load the updated data
    dataframes = load_data(files)

    # Create a Plotly figure
    fig = go.Figure()

    # Define the colors for the lines based on view type
    colors_continuous = ['#117733', '#322288', '#882225']
    colors_yearly = ['#117733', '#322288', '#882225']

    if frequency == 1:  # Every 1 day (show all data points)
        if n_clicks % 2 == 0:  # Continuous View
            for year, group in pd.concat(dataframes.values()).sort_values(by='datetime').groupby('year'):
                traces = get_average_trace(group, location, year)
                fig.add_traces(traces)
        else:  # Yearly View
            all_data = pd.concat(dataframes.values()).sort_values(by='datetime')
            for year in all_data['year'].unique():
                year_data = all_data[all_data['year'] == year]
                traces = get_average_trace(year_data, location, year)
                fig.add_traces(traces)
    else:  # For other frequencies, we will filter data points
        if n_clicks % 2 == 0:  # Continuous View
            all_data = pd.concat(dataframes.values()).sort_values(by='datetime')
            data_to_plot = all_data.iloc[::frequency, :]
            for year, group in data_to_plot.groupby('year'):
                traces = get_average_trace(group, location, year)
                fig.add_traces(traces)
        else:  # Yearly View
            df_concat = pd.concat(dataframes.values()).sort_values(by='datetime')
            df_concat = df_concat.iloc[::frequency, :]
            for year in df_concat['year'].unique():
                year_data = df_concat[df_concat['year'] == year]
                traces = get_average_trace(year_data, location, year)
                fig.add_traces(traces)

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
