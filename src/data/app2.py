import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import traceback

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
app.layout = html.Div(className="container-fluid", children=[
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

# Define callback to update graph
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

    if n_clicks % 2 == 0:
        colors_continuous = ['#003f5c', '#115f9a', '#991f17']
        for i, df in dataframes.items():
            df = df.iloc[::frequency, :]
            for year, group in df.groupby('year'):
                color_index = year - 2021  # Calculate the color index based on the year
                fig.add_trace(go.Scatter(
                    x=group['month_day'],
                    y=group['value'],
                    mode='lines',
                    name=f'{location} {year}',
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
                              name=f'Average for {location} {year}')
    else:
        colors_yearly = ['#003f5c', '#115f9a', '#991f17']
        df_concat = pd.concat(dataframes.values()).sort_values(by='datetime')
        df_concat = df_concat.iloc[::frequency, :]

        for i, year in enumerate(df_concat['year'].unique()):
            color_index = year - 2021  # Calculate the color index based on the year
            year_data = df_concat[df_concat['year'] == year]
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
            x1 = df_concat['datetime'].max()  # Use the maximum date as the end point

            fig.add_shape(type="line",
                          x0=year_data['datetime'].min(), y0=average_value,
                          x1=x1, y1=average_value,
                          line=dict(color='red', dash="dash", width=1),
                          name=f'Average for {location} {year}')

    fig.update_layout(
        autosize=False,
        width=1200,
        height=800,
        title={"text": f"{location.upper()} {analysis} ANALYSIS", "font": {"size": 24}},
        font=dict(size=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='lightgray',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    fig.update_xaxes(tickformat="%m-%d")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
