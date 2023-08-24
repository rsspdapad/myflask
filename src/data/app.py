# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
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
app = Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'])

# Define the layout
app.layout = html.Div(children=[
    html.Div(className="row", children=[
        html.Div(className="col-3", children=[
            html.H4("Controls"),
            html.P("Select analysis type:"),
            dcc.Dropdown(id='analysis-type', options=[
                {'label': 'UNDERGROUND WATER LEVEL', 'value': 'WAT'},
                {'label': 'RADON GAS ANALYSIS', 'value': 'RAD'}
            ], value='WAT', clearable=False),
            html.P("Select location:"),
            dcc.Dropdown(id='location', value='AZAT', clearable=False),
            html.P("Select frequency:"),
            dcc.RadioItems(
                id='frequency',
                options=[
                    {'label': 'All', 'value': 1},
                    {'label': 'Every 2 days', 'value': 2},
                    {'label': 'Every 3 days', 'value': 3},
                    {'label': 'Every 5 days', 'value': 5}
                ],
                value=1,
                labelStyle={'display': 'block'}  # changed from inline-block to block for better visibility in sidebar
            ),
        ]),
        html.Div(className="col-9", children=[
            html.H4("Graph"),
            dcc.Graph(id='live-update-graph', config={'responsive': True}),
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
        return [{"label": "PARAKAR", "value": "PARA"}], "PARA"
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

# Define callback to update graph
@app.callback(Output('live-update-graph', 'figure'),
              [Input('analysis-type', 'value'),
               Input('location', 'value'),
               Input('frequency', 'value')])
def update_graph_live(analysis, location, frequency):
    print(f"Updating graph for {analysis} and {location} with frequency {frequency}")  # print debug information

    # Define file names based on selection
    files = [f"C:/Users/THOM/Desktop/myflaskapp/{location}21_{analysis}.csv",
             f"C:/Users/THOM/Desktop/myflaskapp/{location}22_{analysis}.csv",
             f"C:/Users/THOM/Desktop/myflaskapp/{location}23_{analysis}.csv"]
    
    # Load the updated data
    dataframes = load_data(files)

    # Create a Plotly figure
    fig = go.Figure()

    colors = ['blue', 'orange', 'green']

    file_names = [f'{location}2021{analysis}', f'{location}2022{analysis}', f'{location}2023{analysis}']

    for i, df in dataframes.items():
        df = df.iloc[::frequency, :]  # Select every nth row based on frequency
        for year, group in df.groupby('year'):
            fig.add_trace(go.Scatter(
                x=group['month_day'], 
                y=group['value'], 
                mode='lines',
                hovertemplate = 'Date: %{x}<br>Hour: '+ group['hour'] +'<br>Value: %{y}', # add hover template here
                name=f'{file_names[i]}', 
                line=dict(color=colors[i], width=2.5)  # increased line width
            ))

            # Calculate median and add a line at the median value
            median_value = group['value'].median()
            x1 = datetime.strptime("12/31/2000", "%m/%d/%Y")  # end of the year for year 2000

            fig.add_shape(type="line",
                          x0=group['month_day'].min(), y0=median_value,
                          x1=x1, y1=median_value,
                          line=dict(color='red', dash="dash", width=2),  # increased line width
                          name=f'Median for {file_names[i]}')

    fig.update_layout(autosize=False, width=1200, height=800,
                      title={"text": f"{location.upper()} {analysis} ANALYSIS", "font": {"size": 24}},  # increased title size
                      font=dict(size=18),  # increased general font size
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # repositioned legend
                      plot_bgcolor='lightgrey', paper_bgcolor='lightgrey')  # set background color to light grey
    fig.update_xaxes(tickformat="%m-%d")  # Display both month and day numbers on x-axis

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
